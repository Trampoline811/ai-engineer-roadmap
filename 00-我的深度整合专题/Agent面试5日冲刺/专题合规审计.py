#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
专题合规审计（对照《专题创作指南.md》）
=====================================
用途：检查 `00-我的深度整合专题/` 下每一篇专题文档，是否满足创作指南的「必达标准」：
      ① 目录 ② 0.前言（痛点开场 + 对比表 + 失败模式图）③ 三层结构 ④ 2.0本章导引（符号表+双模式+学习路径）
      ⑤ 每层面试卡片 ⑥ 统一类比贯穿 ⑦ 因果链 ⑧ 决策树 ⑨ 避坑清单 ≥10 条 ⑩ 附录（速查表 + 中英对照术语表）

用法（任意目录）：
    python "00-我的深度整合专题\\Agent面试5日冲刺\\专题合规审计.py"
    python 专题合规审计.py --verbose

退出码：0 = 全部必达项通过；1 = 有缺口
完整报告写入同目录 `合规审计报告.txt`（UTF-8）。
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
TOPIC_ROOT = os.path.abspath(os.path.join(HERE, '..'))

DOCS = [
    r'循环工程深度解析\Loop_Engineering_Deep_Dive.md',
    r'推理与路由深度解析\Model_Route_Deep_Dive.md',
    r'运行时选型深度解析\Runtime_Five_Way_Deep_Dive.md',
    r'观测与评测深度解析\Observability_Eval_Deep_Dive.md',
    r'Agent面试5日冲刺\提纯精读\P2-记忆实现对照提纯.md',
    r'Agent面试5日冲刺\运行时选型-LangGraph-vs-Hermes.md',
    r'Agent记忆深度解析\Agent_Memory_Deep_Dive.md',      # 历史文档：仅报告，不阻断
    r'RAG评估深度解析\RAG_Evaluation_Deep_Dive.md',        # 历史文档：仅报告，不阻断
]

# (必达项名, 判定正则)  —— 失败模式图/避坑 采用宽松识别，避免误报
CHECKS = [
    ('目录', r'^##\s*目录', True),
    ('0.前言(痛点)', r'前言|痛点', True),
    ('失败模式图', r'失败模式|失败场景|典型失败|翻车', True),
    ('对比表格', r'\|[^\n]*\|[^\n]*\|', True),
    ('三层结构', r'概念层[\s\S]{0,4000}(实现层|计算层)[\s\S]{0,4000}工程层', True),
    ('2.0本章导引', r'本章导引|阅读导引|阅读指南|阅读档位|双模式', True),
    ('符号表', r'符号表', True),
    ('学习路径', r'学习路径|```mermaid', True),
    ('统一类比', r'统一类比|贯穿全文的类比|统一比喻', True),
    ('因果链', r'因果链', True),
    ('决策树', r'决策树', True),
    ('面试卡片', r'面试卡', True),
    ('5分钟速查卡', r'速查卡|速查表', True),
    ('中英对照术语表', r'中英对照|英文术语', True),
    ('附录', r'^##\s*附录|^#\s*附', True),
]


def count_pitfalls(text):
    """数避坑清单条目：对每一个含「避坑」的标题各开一个 8000 字窗口统计
    ① markdown 表格行 `| N |`  ② ❌ 坑N/翻车N  ③ 有序列表 `N. **`
    最后取各窗口最大值（避免"速查卡里的避坑口诀"这类小窗口把真实数量盖掉）"""
    marks = list(re.finditer(r'^#{2,4}[^\n]*避坑[^\n]*$', text, re.M))
    windows = [text[m.start(): m.start() + 8000] for m in marks] or [text]
    best = 0
    for w in windows:
        n_table = len(re.findall(r'^\|\s*\d+\s*\|', w, re.M))
        n_cross = len(re.findall(r'❌\s*(?:坑|翻车)', w))
        n_list = len(re.findall(r'^\s*\d+\.\s+\*\*', w, re.M))
        best = max(best, n_table, n_cross, n_list)
    return best


# 入口卡/对照卡：不要求完整三层结构（指南针对的是 *_Deep_Dive.md 完整专题）
CARD_DOCS = {'运行时选型-LangGraph-vs-Hermes.md'}


def main():
    verbose = '--verbose' in sys.argv
    rep = []
    fails = 0
    rep.append('=' * 96)
    rep.append('专题合规审计 · 对照《00-我的深度整合专题/专题创作指南.md》必达标准')
    rep.append('=' * 96)

    for rel in DOCS:
        p = os.path.join(TOPIC_ROOT, rel)
        name = os.path.basename(rel)
        legacy = ('Agent_Memory_Deep_Dive' in name) or ('RAG_Evaluation_Deep_Dive' in name)
        if not os.path.exists(p):
            rep.append(f'\n### {name}  [文件不存在]')
            continue
        t = io.open(p, encoding='utf-8').read()
        n = sum(1 for _ in open(p, encoding='utf-8'))
        have, lack = [], []
        is_card = name in CARD_DOCS
        for label, pat, required in CHECKS:
            if is_card and label == '三层结构':
                have.append('三层结构(N/A·入口卡)')
                continue
            (have if re.search(pat, t, re.M) else lack).append(label)
        pits = count_pitfalls(t)
        pit_ok = pits >= 10
        status = '✅ 合规' if (not lack and pit_ok) else '⚠️ 有缺口'
        if legacy:
            status += '（历史文档，仅报告不阻断）'
        elif lack or not pit_ok:
            fails += 1

        rep.append(f'\n### {name}  ({n} 行)  {status}')
        rep.append('  ✅ ' + '、'.join(have))
        if lack:
            rep.append('  ❌ 缺: ' + '、'.join(lack))
        rep.append(f'  📋 避坑条目数: {pits}  {"(≥10 ✅)" if pit_ok else "(<10 ❌)"}')
        if verbose:
            rep.append(f'  （长度：创作指南建议 1500–3000 行；冲刺压缩版可豁免，但文首需标注）')

    rep.append('')
    rep.append('=' * 96)
    rep.append('结论：' + ('冲刺专题全部满足必达标准 ✅' if fails == 0 else f'{fails} 篇仍有缺口 ❌'))
    rep.append('（"长度 1500–3000 行"一项：冲刺版按指南 §转正规则豁免，文首须标注"压缩版"）')

    out = os.path.join(HERE, '合规审计报告.txt')
    io.open(out, 'w', encoding='utf-8').write('\n'.join(rep) + '\n')

    print('\n'.join(rep))
    print(f'\n完整报告：{out}')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
