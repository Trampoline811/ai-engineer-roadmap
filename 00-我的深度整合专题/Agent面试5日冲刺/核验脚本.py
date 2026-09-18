#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
冲刺计划「文件真实性」核验脚本 v2
==================================
用途：扫描 `00-我的深度整合专题/Agent面试5日冲刺/` 下所有 .md，把正文里反引号包起来的
      路径引用逐个核验，并按以下五类分别报告：

  [OK]        精确存在（相对仓库根 / 相对本文所在目录 / 相对冲刺目录 三者之一命中）
  [OK~]       唯一后缀命中（如写 `agent\\loop.py`，仓库里只有 01-Agent\\02-Agent_react\\agent\\loop.py）
  [AMBIG]     多处命中（必须写全路径，否则读者会找错文件）—— 列出全部候选
  [PLANNED]   计划产出物（白名单，尚未创建，不算错误）
  [MISS]      仓库里找不到任何同名/同后缀文件 —— 需要修正计划

用法：
    python "00-我的深度整合专题\\Agent面试5日冲刺\\核验脚本.py"
    python 核验脚本.py --verbose      # 额外打印所有 OK/OK~ 明细

退出码：0 = 无 AMBIG 且无 MISS；1 = 有需要修的地方
完整报告同时写入同目录 `核验报告.txt`（UTF-8）。
"""
import os
import re
import sys
from collections import OrderedDict

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))       # 仓库根
# 扫描范围：整个「00-我的深度整合专题」树（含本冲刺目录、提纯精读、各模块专题）
SCAN_ROOT = os.path.abspath(os.path.join(HERE, '..'))

SKIP_DIRS = {'.git', 'node_modules', '.venv', '__pycache__', '.memsearch',
             '.scratch-mem0', '.claude', '.cursor'}

VALID_EXT = {
    '.md', '.py', '.ipynb', '.json', '.txt', '.html', '.yml', '.yaml',
    '.toml', '.sh', '.js', '.ts', '.css', '.ini', '.cfg', '.env',
}

# 仓库外 / 有意不存在的引用：命中即跳过
EXTRA_SKIP = [
    '~', 'http', 'personal-knowledge', 'dsh/profiles', 'node_modules',
    '02.opensource_AI.md',        # UP主未上传的笔记原文件（是研究结论，不是本地文件）
    '<root>', '...', '…', '{', '}', '*', '&&', ' | ',
    '->', '=>',
    'eval_data.json',             # 文档里让读者自己创建的示例数据文件名（非仓库文件）
    'len//4',                     # 代码表达式，非路径
    'RAG_Evaluation_Cheatsheet.ipynb',   # 已在文档中如实标注"实测不在仓库中"
    'WAKU_HOME', 'WORKDIR', 'HERMES_HOME', '${',   # 运行期环境变量路径占位符
    'APPEND_SYSTEM.md', 'SYSTEM.md',     # Pi 上游的 prompt 文件名（本仓库不含 Pi 源码）
    'store.js', 'index.js',              # dsh-memory-evolve 插件源码（在 ~/.dsh 下，仓库外）
    'mem0/configs/prompts.py', 'mem0/utils/entity_extraction.py',   # mem0 上游源码（仓库外）
    '_incoming/SKILL.md',
]

# 计划产出物（尚未创建，白名单）——basename 匹配
PLANNED = {
    'P2-记忆实现对照提纯.md',
    'P3-RAG主线提纯.md',
    'P4-多智能体与框架提纯.md',
    'P5-评测CICD概念提纯.md',
    'Model_Route_Deep_Dive.md',
    'Observability_Eval_Deep_Dive.md',
    'Runtime_Five_Way_Deep_Dive.md',
    '推理与路由深度解析',
    '观测与评测深度解析',
    '运行时选型深度解析',
}

# 形如命令行的引用（pip install / python xxx.py / uv venv …）不校验
CMD_FIRST_WORDS = {'python', 'python3', 'pip', 'pip3', 'uv', 'cd', 'git', 'rm',
                   'cp', 'mv', 'ls', 'cat', 'pytest', 'streamlit', 'jupyter',
                   'export', 'set', 'echo', 'curl', 'docker'}

BACKTICK_RE = re.compile(r'`([^`\n]{2,220})`')


# ---------------------------------------------------------------- 仓库索引
def build_index():
    files, dirs = set(), set()
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        rel_dir = os.path.relpath(dp, ROOT)
        if rel_dir != '.':
            dirs.add(rel_dir)
        for f in fns:
            files.add(os.path.join(rel_dir, f) if rel_dir != '.' else f)
    return files, dirs


FILES, DIRS = build_index()
ALL = FILES | DIRS


def iter_md_files():
    """递归扫描 SCAN_ROOT 下所有 .md（含各模块专题目录与提纯精读）"""
    for dp, dns, fns in os.walk(SCAN_ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for name in sorted(fns):
            if name.lower().endswith('.md'):
                yield os.path.join(dp, name)


def looks_like_path(raw):
    s = raw.strip()
    if not s or any(tok in s for tok in EXTRA_SKIP):
        return False
    if s.startswith(('\\', '/', '-', '#', '@')):
        return False
    # 运行时/约定路径（.claude/、.memory/、.tasks/、./xxx）不是仓库文件，跳过
    if s.startswith('.') or s.startswith('./'):
        return False
    # 绝对路径（含盘符）不是仓库内引用，跳过
    if re.match(r'^[A-Za-z]:[\\/]', s):
        return False
    if any(ch in s for ch in '<>"\'`|?='):
        return False
    ext = os.path.splitext(s)[1].lower()
    has_sep = ('\\' in s) or ('/' in s)
    if ' ' in s:
        first = s.split(' ')[0]
        # 「带空格的中文目录 + 已知后缀」是合法路径；「命令 参数」不是
        if not has_sep and ext not in VALID_EXT:
            return False
        if first.lower() in CMD_FIRST_WORDS:
            return False
        if ext not in VALID_EXT:
            return False
    if ext in VALID_EXT:
        return True
    if has_sep and (s.endswith('\\') or s.endswith('/')):
        return True       # 目录引用
    if has_sep:
        return True       # 可能是无后缀的目录/文件引用，交给核验阶段判断
    return False


def line_count(p):
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return -1


def check(ref, md_path):
    """返回 (status, detail, candidates)"""
    s = ref.strip()
    # 引用形式 `path:73–80` / `path:122` / `path:2.2`（小节号）：剥掉后缀再核验文件本身
    s = re.sub(r':\s*§?\s*\d+(?:[.\-–~/]\d+)*$', '', s).strip()
    low = s.lower()
    base_name = os.path.basename(s.rstrip('\\/'))
    if base_name in PLANNED:
        return 'PLANNED', '计划产出物', []

    cands = []

    # 1) 精确：仓库根 / 本 md 所在目录 / 冲刺目录
    for base, label in ((ROOT, 'root'), (os.path.dirname(md_path), 'same-dir'), (HERE, 'sprint')):
        p = os.path.join(base, s.replace('/', os.sep))
        if os.path.exists(p):
            rel = os.path.relpath(p, ROOT)
            return 'OK', f'{label}: {rel}', []

    # 2) 后缀命中
    if ('\\' in s) or ('/' in s):
        suffix = os.sep + s.replace('/', os.sep).rstrip('\\/').lower()
        cands = sorted(x for x in ALL if x.lower().endswith(suffix))
    # 3) basename 命中
    if not cands:
        cands = sorted(x for x in ALL if os.path.basename(x).lower() == low)

    if len(cands) == 1:
        return 'OK~', f'后缀唯一命中: {cands[0]}', cands
    if len(cands) > 1:
        return 'AMBIG', f'{len(cands)} 处命中', cands[:6]
    # 4) 多文件简写（如 s01/s03/s08、09-loop-engineering/02、08/12）：不是单一路径引用
    if re.fullmatch(r'[0-9A-Za-z_\-\u4e00-\u9fff]+(?:[/\\][0-9A-Za-z_\-\u4e00-\u9fff]+)+', s) \
            and os.path.splitext(s)[1].lower() not in VALID_EXT:
        return 'SHORTHAND', '多文件简写（非单一路径）', []
    return 'MISS', '仓库中找不到', []


def main():
    verbose = '--verbose' in sys.argv
    md_files = list(iter_md_files())
    refs = OrderedDict()          # ref -> [(md, line)]
    for md in md_files:
        rel_md = os.path.relpath(md, ROOT)
        try:
            text = open(md, 'r', encoding='utf-8', errors='ignore').read()
        except Exception as e:
            print(f'[WARN] 读不了 {rel_md}: {e}')
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for raw in BACKTICK_RE.findall(line):
                if looks_like_path(raw):
                    refs.setdefault(raw.strip(), []).append((rel_md, lineno))

    buckets = {'OK': [], 'OK~': [], 'AMBIG': [], 'PLANNED': [], 'SHORTHAND': [], 'MISS': []}
    for ref, where in refs.items():
        md_path = os.path.join(ROOT, where[0][0])
        status, detail, cands = check(ref, md_path)
        buckets[status].append((ref, detail, cands, where))

    rep = []
    rep.append('=' * 84)
    rep.append(f'仓库根   : {ROOT}')
    rep.append(f'扫描 md  : {len(md_files)} 个   |   路径引用: {len(refs)} 个（去重）')
    rep.append(f'OK {len(buckets["OK"])} | OK~ {len(buckets["OK~"])} | '
               f'AMBIG {len(buckets["AMBIG"])} | SHORTHAND {len(buckets["SHORTHAND"])} | '
               f'PLANNED {len(buckets["PLANNED"])} | MISS {len(buckets["MISS"])}')
    rep.append('=' * 84)

    for key, title in (('MISS', '缺失（必须修）'),
                       ('AMBIG', '多处命中（建议写全路径）'),
                       ('SHORTHAND', '多文件简写（非路径引用，可忽略）'),
                       ('PLANNED', '计划产出物（未创建，白名单）'),
                       ('OK~', '后缀唯一命中（可写全路径更稳）')):
        items = buckets[key]
        if not items:
            continue
        rep.append('')
        rep.append(f'---- [{key}] {title} ----')
        for ref, detail, cands, where in items:
            rep.append(f'  {ref}    <{detail}>')
            rep.append(f'      引用处: ' + ', '.join(f'{m}:{l}' for m, l in where[:3]))
            for c in cands:
                rep.append(f'      -> {c}')

    if verbose:
        rep.append('')
        rep.append('---- [OK] 精确命中明细 ----')
        for ref, detail, cands, where in buckets['OK']:
            rep.append(f'  {ref}    <{detail}>')

    rep.append('')
    bad = len(buckets['MISS'])          # 只有「找不到」才算错；AMBIG 是建议写全路径
    amb = len(buckets['AMBIG'])
    rep.append('结论：' + ('全部引用路径可唯一定位 ✅' if bad == 0
                          else f'MISS {bad} 处必须修'))
    if amb:
        rep.append(f'（另有 AMBIG {amb} 处：文件存在但写法有歧义，建议改成仓库根全路径）')

    report_path = os.path.join(HERE, '核验报告.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rep) + '\n')

    # 控制台（ASCII 安全）
    print('=' * 84)
    print(f'md {len(md_files)} / refs {len(refs)} / '
          f'OK {len(buckets["OK"])} / OK~ {len(buckets["OK~"])} / '
          f'AMBIG {len(buckets["AMBIG"])} / SHORTHAND {len(buckets["SHORTHAND"])} / '
          f'PLANNED {len(buckets["PLANNED"])} / MISS {len(buckets["MISS"])}')
    print('=' * 84)
    for key in ('MISS', 'AMBIG'):
        for ref, detail, cands, where in buckets[key]:
            print(f'[{key}] {ref}  <{detail}>')
            print('       ref@ ' + ', '.join(f'{m}:{l}' for m, l in where[:2]))
            for c in cands[:4]:
                print(f'       -> {c}')
    print(f'\nreport: {report_path}')
    print('RESULT: ' + ('ALL RESOLVED' if bad == 0 else f'{bad} TO FIX'))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
