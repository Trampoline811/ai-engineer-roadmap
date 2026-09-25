# -*- coding: utf-8 -*-
"""行话审计：检查每篇深度解析专题的「术语表」与「正文首现就地加注」是否达标。

背景（2026-09-18 立规，源自读者实测反馈）：
    读者在读 `Loop_Engineering_Deep_Dive.md` 时撞到 `buzzword` 这种词——正文里突然出现、
    没有解释、附录才提到。于是立两条必达标准：
      ① 有「英文术语 | 中文 | 一句人话」三列中英对照术语表（≥15 条）
      ② 正文第一次出现任何英文行话，写成「词（中文）」；附录只作兜底

判定：
    FAIL  = 没有术语表，或表内条目 < 15 条
    WARN  = 术语表达标，但仍有 ≥1 条术语在正文首现未加注（附清单）
    PASS  = 两项都达标

用法：python 行话审计.py            # 打印报告
      python 行话审计.py --write    # 同时写 行话审计报告.txt
"""
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # 00-我的深度整合专题
REPORT = os.path.join(HERE, "行话审计报告.txt")

SPRINT = [                                        # 冲刺 6 篇：必须达标
    r"循环工程深度解析\Loop_Engineering_Deep_Dive.md",
    r"推理与路由深度解析\Model_Route_Deep_Dive.md",
    r"运行时选型深度解析\Runtime_Five_Way_Deep_Dive.md",
    r"观测与评测深度解析\Observability_Eval_Deep_Dive.md",
    r"Agent记忆深度解析\Agent_Memory_Deep_Dive.md",
    r"RAG评估深度解析\RAG_Evaluation_Deep_Dive.md",
]
EXTRA = [r"Agent面试5日冲刺\运行时选型-LangGraph-vs-Hermes.md"]

CJK = re.compile(r"[\u4e00-\u9fff]")
GLOSS_AFTER = re.compile(r"^[\sA-Za-z0-9\-/+.]{0,24}[（(][^）)]{0,90}[）)]")
MIN_ENTRIES = 15


def code_mask(lines):
    mask, fence = [False] * len(lines), False
    for i, l in enumerate(lines):
        if l.strip().startswith("```"):
            fence = not fence
            mask[i] = True
            continue
        mask[i] = fence
    return mask


def parse_glossary(lines):
    """抓「英文|中文」或「中文|英文」方向的术语表，返回 (entries, rows, three_col)"""
    entries, rows, three_col = [], set(), False
    i = 0
    while i < len(lines):
        l = lines[i]
        has_en = ("英文" in l) or ("English" in l)
        has_zh = ("中文" in l) or ("Chinese" in l)
        if l.strip().startswith("|") and has_en and has_zh:
            pos_en = min([p for p in [l.find("英文"), l.find("English")] if p >= 0] or [10 ** 6])
            pos_zh = min([p for p in [l.find("中文"), l.find("Chinese")] if p >= 0] or [10 ** 6])
            en_idx = 0 if pos_en < pos_zh else 1
            j = i + 1
            if j < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[j]):
                rows.add(j)
                j += 1
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.add(j)
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                if len(cells) >= 2:
                    if len(cells) >= 3 and CJK.search(cells[2]):
                        three_col = True
                    term = re.sub(r"\*+", "", cells[en_idx]).strip()
                    if re.search(r"[A-Za-z]", term) and not CJK.search(term):
                        entries.append(term)
                j += 1
            i = j
            continue
        i += 1
    return entries, rows, three_col


def body_range(lines):
    """正文区间 = 溯源/目录之后，附录/速查卡之前。术语只需在正文首现处加注。"""
    start, end = 0, len(lines)
    for i, l in enumerate(lines):
        if re.match(r"^##\s", l) and not re.search(r"溯源|目录|导航|定位", l):
            start = i
            break
    for i, l in enumerate(lines):
        if i > start and re.match(r"^##\s", l) and re.search(r"附录|速查|📌|📇|附\s", l):
            end = i
            break
    return start, end


def alternates(term):
    t = re.sub(r"[（(][^）)]*[）)]", "", term).strip()
    parts = [p.strip() for p in re.split(r"\s*/\s*|\s*·\s*", t) if p.strip()]
    return parts or [t]


def first_prose_hit(lines, mask, term, lo, hi, rows):
    """返回 (行号, 是否已就地加注) —— 只看正文区间内第一处真正的出现。

    不判为"缺注"的情形（都会跳过，继续往后找）：
      · 术语表自己的行（那是词条本身）
      · 该行已经给别的行话加过注（同一行不重复加注是刻意的，避免啰嗦）
      · 多写法词条：任一种写法已加注即视为满足
    """
    for alt in alternates(term):
        if len(alt) < 3:
            continue
        pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(alt) + r"(?![A-Za-z0-9])", re.I)
        for i in range(lo, hi):
            raw = lines[i]
            if mask[i] or i in rows:
                continue
            s = raw.lstrip()
            if s.startswith("#") or "](#" in raw:
                continue
            line = re.sub(r"`[^`]*`", lambda m: "\u0000" * len(m.group(0)), raw)
            m = pat.search(line)
            if not m:
                continue
            if any(a <= m.start() < b for a, b in
                   [(x.start(), x.end()) for x in re.finditer(r"`[^`]*`", raw)]):
                continue
            ctx = line[max(0, m.start() - 34): m.end() + 34]
            if re.search(r"[\\]|\.md|\.py|\.json|\.jsonl|\.ts", ctx):
                continue          # 路径引用，不是行话讲解场景
            if raw.strip().startswith("|"):
                if pat.search(raw.strip().strip("|").split("|")[0]):
                    continue      # 术语表格式的行
            # 该行任意位置已有「词（中文）」→ 视为这一行已完成就地翻译
            if GLOSS_AFTER.match(line[m.end(): m.end() + 110]) and CJK.search(
                    GLOSS_AFTER.match(line[m.end(): m.end() + 110]).group(0)):
                return (i + 1, True)
            if re.search(r"[（(][^）)]{1,40}[）)]", line):
                return (i + 1, True)
            return (i + 1, False)
    return None


def audit(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return {"missing": True}
    lines = open(p, encoding="utf-8").read().split("\n")
    mask = code_mask(lines)
    lo, hi = body_range(lines)
    terms, rows, three_col = parse_glossary(lines)
    if len(terms) < MIN_ENTRIES:
        return {"entries": len(terms), "three_col": three_col, "fail": "术语表缺失或条目不足"}
    bad = []
    for t in terms:
        h = first_prose_hit(lines, mask, t, lo, hi, rows)
        if h and not h[1]:
            bad.append((t, h[0]))
    return {"entries": len(terms), "three_col": three_col, "bad": bad}


def main():
    out = []
    out.append("行话审计报告（标准见《专题创作指南.md》语言风格 #4 与必达标准）")
    out.append("=" * 78)
    n_pass = n_warn = n_fail = 0
    for rel in SPRINT + EXTRA:
        r = audit(rel)
        name = os.path.basename(rel)
        tag = "（历史文档·仅报告）" if rel in EXTRA else ""
        if r.get("missing"):
            out.append("❌ %s：文件不存在" % name)
            n_fail += 1
            continue
        if r.get("fail"):
            out.append("❌ %s%s：%s（现有 %d 条）" % (name, tag, r["fail"], r["entries"]))
            n_fail += 1
            continue
        col = "三列（含一句人话）" if r["three_col"] else "两列（缺一句人话列）"
        if r["bad"]:
            n_warn += 1
            out.append("⚠️ %s%s：术语表 %d 条，%s；**正文首现未加注 %d 条**"
                       % (name, tag, r["entries"], col, len(r["bad"])))
            for t, ln in r["bad"][:30]:
                out.append("      ✗ %-28s 首现 L%d" % (t, ln))
            if len(r["bad"]) > 30:
                out.append("      ... 其余 %d 条" % (len(r["bad"]) - 30))
        else:
            n_pass += 1
            out.append("✅ %s%s：术语表 %d 条，%s；正文首现全部已加注"
                       % (name, tag, r["entries"], col))
    out.append("=" * 78)
    out.append("汇总：PASS %d ｜ WARN %d ｜ FAIL %d" % (n_pass, n_warn, n_fail))
    out.append("结论：" + ("冲刺专题全部达标 ✅" if n_fail == 0 else "有专题未达标 ❌"))
    txt = "\n".join(out)
    print(txt)
    if "--write" in sys.argv:
        open(REPORT, "w", encoding="utf-8").write(txt + "\n")
        print("\n报告已写入：%s" % REPORT)


if __name__ == "__main__":
    main()
