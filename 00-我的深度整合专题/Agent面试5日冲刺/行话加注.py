# -*- coding: utf-8 -*-
"""行话加注：按每篇文档自己的中英对照术语表，回填「正文首次出现」的就地中文注释。

规则（对应《专题创作指南.md》语言风格 #4）：
    · 正文第一次出现某英文行话 → 写成「词（中文）」，中文取术语表的中文列
    · 只注首次；表头、对比表单元格里也注；附录术语表本身不注（那是词条）
    · 代码块 / 标题 / 目录 / 路径引用 / 反引号里的代码名一律不注

用法：python 行话加注.py           # 试跑，只打印计划
      python 行话加注.py --apply   # 真改
"""
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APPLY = "--apply" in sys.argv

TARGETS = [
    r"循环工程深度解析\Loop_Engineering_Deep_Dive.md",
    r"推理与路由深度解析\Model_Route_Deep_Dive.md",
    r"运行时选型深度解析\Runtime_Five_Way_Deep_Dive.md",
    r"观测与评测深度解析\Observability_Eval_Deep_Dive.md",
    r"Agent记忆深度解析\Agent_Memory_Deep_Dive.md",
    r"RAG评估深度解析\RAG_Evaluation_Deep_Dive.md",
    r"Agent面试5日冲刺\运行时选型-LangGraph-vs-Hermes.md",
]

CJK = re.compile(r"[\u4e00-\u9fff]")
GLOSS_AFTER = re.compile(r"^[\sA-Za-z0-9\-/+.]{0,24}[（(][^）)]{0,90}[）)]")


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
    """返回 (entries, rows)；entries=[(term, zh)]，rows=术语表行号集合（这些行不加注）"""
    entries, rows = [], set()
    i = 0
    while i < len(lines):
        l = lines[i]
        has_en = ("英文" in l) or ("English" in l)
        has_zh = ("中文" in l) or ("Chinese" in l)
        if l.strip().startswith("|") and has_en and has_zh:
            pos_en = min([p for p in [l.find("英文"), l.find("English")] if p >= 0] or [10 ** 6])
            pos_zh = min([p for p in [l.find("中文"), l.find("Chinese")] if p >= 0] or [10 ** 6])
            en_idx = 0 if pos_en < pos_zh else 1
            zh_idx = 1 - en_idx
            j = i + 1
            if j < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[j]):
                rows.add(j)
                j += 1
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.add(j)
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                if len(cells) > max(en_idx, zh_idx):
                    term = re.sub(r"\*+", "", cells[en_idx]).strip()
                    zh = re.sub(r"\*+", "", cells[zh_idx]).strip()
                    if re.search(r"[A-Za-z]", term) and CJK.search(zh):
                        entries.append((term, zh))
                j += 1
            i = j
            continue
        i += 1
    return entries, rows


def body_range(lines):
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
    return [p for p in parts if len(p) >= 3]


def short_gloss(zh):
    s = zh.strip()
    for sep in ["；", "，", "（", "(", "：", ":"]:
        if sep in s:
            s = s.split(sep)[0]
    s = s.strip(" /")
    return s if len(s) <= 18 else s[:18]


# 多词合并行（术语表里一行写了几个词）必须逐词指定注释，否则会把整行的中文硬套给单个词。
# 键 = 该行的英文原词 + "|" + 具体某个写法
OVERRIDE = {
    "prompt / context / harness / loop engineering|prompt": "提示词层",
    "prompt / context / harness / loop engineering|context": "上下文层",
    "prompt / context / harness / loop engineering|harness": "外壳层",
    "prompt / context / harness / loop engineering|loop engineering": "循环层",
    "Retry / Backoff|retry": "重试",
    "Retry / Backoff|backoff": "退避",
    "Span / SpanKind|span": "跨度",
    "Span / SpanKind|spankind": "跨度类型",
    "Billing / Ledger|billing": "计费",
    "Billing / Ledger|ledger": "账本",
    "Whitelist / Schema|whitelist": "白名单",
    "Whitelist / Schema|schema": "结构校验",
    "Grounding / Citation|grounding": "有据",
    "Grounding / Citation|citation": "引用",
    "SFT / PPO / GRPO|sft": "监督微调",
    "SFT / PPO / GRPO|ppo": "强化学习优化",
    "SFT / PPO / GRPO|grpo": "省显存的 PPO 变体",
    "n_expert / top-k|n_expert": "专家个数",
    "n_expert / top-k|top-k": "取前 k 个",
    "FLOPs / QPS|flops": "浮点运算量",
    "FLOPs / QPS|qps": "每秒查询数",
    "degraded / static-template|degraded": "降级态",
    "degraded / static-template|static-template": "静态模板兜底",
    "compaction / compression|compaction": "历史压缩",
    "compaction / compression|compression": "历史压缩",
    "Consistency / Robustness / Calibration|consistency": "一致性",
    "Consistency / Robustness / Calibration|robustness": "鲁棒性",
    "Consistency / Robustness / Calibration|calibration": "校准",
    "Judge / LLM-as-judge|judge": "裁判模型",
    "Judge / LLM-as-judge|llm-as-judge": "裁判模型",
    "P50 / P90 / P99|p50": "50 分位延迟",
    "P50 / P90 / P99|p90": "90 分位延迟",
    "P50 / P90 / P99|p99": "99 分位延迟",
    "Baseline / Regression|baseline": "基线",
    "Baseline / Regression|regression": "回归",
    "state.db / JSONL|jsonl": "行式日志",
    "state.db / JSONL|state.db": "状态库",
    "Windowed / Sliding Window Memory|windowed": "滑动窗口记忆",
    "Summary Memory / Running Summary|running summary": "摘要记忆",
    "Summary Memory / Running Summary|summary memory": "摘要记忆",
    "PASS / FAIL|fail": "不通过",
    "PASS / FAIL|pass": "通过",
    "Incremental / Refine Summary|incremental": "增量摘要",
    "Reflexion / Strategic Memory|reflexion": "反思记忆",
    "Capability vs Reliability|reliability": "可靠度",
    "Three-factor Scoring|three-factor scoring": "三因子打分",
    "Hard Stop|hard stop": "硬停机",
    "Checkable Goal|checkable goal": "可验收目标",
    "Maker–Checker|maker–checker": "做—验分离",
    "Separate Checker|separate checker": "独立验收人",
}


def _norm_key(s):
    """归一化查表键：统一空白与全角斜杠、去掉零宽字符、转小写。
    起因：覆盖表里混入过不可见字符，导致 dict[*] 精确查找失效（2026-09-18 踩坑）。"""
    s = s.replace("\u200b", "").replace("\ufeff", "").replace("\xa0", " ")
    s = s.replace("／", "/").replace("｜", "|")
    s = re.sub(r"\s+", " ", s).strip()
    return s.lower()


_OVERRIDE_NORM = {_norm_key(k): v for k, v in OVERRIDE.items()}


def gloss_for(term, alt, zh):
    return _OVERRIDE_NORM.get(_norm_key(term + "|" + alt)) or short_gloss(zh)


summary = []
for rel in TARGETS:
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        print("缺文件：", rel)
        continue
    lines = open(p, encoding="utf-8").read().split("\n")
    mask = code_mask(lines)
    lo, hi = body_range(lines)
    entries, rows = parse_glossary(lines)
    used = set()
    edits = []
    for term, zh in entries:
        for alt in alternates(term):
            g = gloss_for(term, alt, zh)
            pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(alt) + r"(?![A-Za-z0-9])", re.I)
            for i in range(lo, hi):
                if mask[i] or i in rows or i in used:
                    continue
                raw = lines[i]
                if raw.lstrip().startswith("#") or "](#" in raw:
                    continue
                bt = [(x.start(), x.end()) for x in re.finditer(r"`[^`]*`", raw)]
                line = re.sub(r"`[^`]*`", lambda m: "\u0000" * len(m.group(0)), raw)
                m = pat.search(line)
                if not m:
                    continue
                if any(a <= m.start() < b for a, b in bt):
                    continue
                ctx = line[max(0, m.start() - 34): m.end() + 34]
                if re.search(r"[\\]|\.md|\.py|\.json|\.jsonl|\.ts", ctx):
                    continue
                if raw.strip().startswith("|"):
                    if pat.search(raw.strip().strip("|").split("|")[0]):
                        continue
                after = line[m.end(): m.end() + 120]
                mm = GLOSS_AFTER.match(after)
                if mm and CJK.search(mm.group(0)):
                    break                     # 已加注，换下一个术语
                edits.append((i, m.start(), m.end(), g, alt))
                used.add(i)
                break
    print("=" * 78)
    print("%s | 术语表 %d 条 → 计划加注 %d 处" % (os.path.basename(rel), len(entries), len(edits)))
    for i, a, b, g, alt in sorted(edits):
        print("   L%-5d %s（%s）" % (i + 1, lines[i][a:b], g))
    if APPLY and edits:
        per = {}
        for i, a, b, g, alt in edits:
            per.setdefault(i, []).append((a, b, g))
        for i, items in per.items():
            line = lines[i]
            for a, b, g in sorted(items, key=lambda t: -t[0]):
                line = line[:b] + "（" + g + "）" + line[b:]
            lines[i] = line
        open(p, "w", encoding="utf-8").write("\n".join(lines))
        print("   ✅ 已写入")
    summary.append((os.path.basename(rel), len(entries), len(edits)))

print("=" * 78)
for n, e, k in summary:
    print("  %-46s 术语表 %-4d 加注 %-4d" % (n, e, k))
print("APPLY =", APPLY)
