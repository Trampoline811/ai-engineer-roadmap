# D3 — RAG 主线（岗位核心，全天）

> 日期：____ ｜ 今日面试锚（A）：
> 📖 主阅读（提纯版）：先读 `提纯精读\P3-RAG主线提纯.md` + 已有 RAG评估专题（RAG_Evaluation_Deep_Dive.md），源文件按需深挖**"高级 RAG 有哪些手段？四指标低了怎么修？RAG vs 记忆 vs 长上下文？"**
> 主轴位置：上下文注入层（总图第三层）
> 复用资产：`00-我的深度整合专题\RAG评估深度解析\RAG_Evaluation_Deep_Dive.md`（2861 行，已完备，**只复习不重造**）

## 时间盒（≈8.5h 有效学习）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 08:30-09:00 | 主动回忆 | 口述 D2 复盘 3 问 | 3 答记录 |
| 09:00-10:30 | 基线 M | `02-RAG\01-simple_rag\README.md`（最小闭环）+ `02-RAG\02-RAG_basic\README.md`（12 知识点，重点 08-12 本地可跑部分） | 最小 RAG 管线图 |
| 10:30-12:30 | 进阶 M | `02-RAG\03-high_level_RAG\README.md` + 五范式各 py 文件头；`04-graph_rag进阶` **只读概念**（Neo4j 跑不了，Docker 未启动） | 高级 RAG 手段清单 |
| 14:00-15:30 | 实操 D | `02-RAG\06 Agentic RAG\code\agentic_rag_demo.py` 精读（三幕结构：LLM⇄工具 0~N 次检索决策；先看 `ppt\agentic-rag-deck.html` 或代码头部注释确认 --mock 离线用法再跑）；`agentic_rag_example.py` 对照 | 见**写码挑战③** |
| 15:30-17:00 | 评测 D | `02-RAG\04_RAG_Evaluation\lesson1_rag_evaluation\README.md`（RAGAS）+ `lesson2_rag_metrics\README.md`（手写指标/排序/诊断门禁；lesson2 目录内 diagnostic_report.html 若在则看）；复习 RAG评估专题面试卡 | 四指标 + 四象限诊断口述 |
| 17:00-18:45 | 治理收口 | 幻觉治理线（Faithfulness→Claim/Verify→Citation，自 high_level 的 Self-RAG 等范式）→ **RAG 质量决策树** + "RAG vs 记忆 vs 长上下文"边界卡（呼应 D2） | 两张卡 |
| 20:00-21:30 | 整合 | 挂总图 + 面试卡 + 口述自测 | 本文件产出区 |

## 写码挑战③（45min）

手写 hybrid 检索 + RRF 融合伪代码（BM25 分数 + 向量分数 → RRF = Σ 1/(k+rank)，k≈60）；或闭卷默写 NDCG 公式并解释为什么排序指标对 RAG 重要。任选其一，写完对照 lesson2 或 high_level 代码。

## 面试卡（今日自答，次日回填）

1. 完整讲一遍生产 RAG 管线（分块→向量化→检索→重排→生成），每步的失败模式？
2. 高级 RAG 五范式各一句话（Query改写/混合检索/重排/上下文压缩/迭代检索等，以仓库实际内容为准）。
3. 四指标（Context Recall/Precision、Answer Relevancy、Faithfulness）低了分别怎么修？
4. 什么时候用 RAG vs 记忆 vs 长上下文？（这是"边界题"的标准答法来源）
5. Agentic RAG 和普通 RAG 的区别？什么时候检索决定值得交给 LLM？
6. 幻觉怎么治？（引用/事实校验/门禁阈值——Faithfulness≥0.8 之类）
7. 评测怎么落地到生产？（数据集→门禁→持续评估→可观测）

## 晚间复盘 3 问（明早 D4 开场口述）

1. 画一遍 RAG 决策树主干（检索差→换策略；生成差→换提示/引用）。
2. RAG vs 记忆的边界，用一句话+一个例子讲清。
3. Agentic RAG 三幕结构你记住了什么？（检索 0 次/1 次/N 次）

## 今日产出区

### RAG 质量决策树（主干 ASCII，细节待填）
```
检索差？ ── 分块/Embedding/混合检索(BM25+向量)/RRF/rerank/查询改写
生成差？ ── 引用+事实校验/提示/门禁(阈值)/人审
评测：四指标四象限定位 → 修复 → 回归
```

### RAG vs 记忆 vs 长上下文 边界卡
（待填：来源/更新频率/评测方式/成本 四个维度）

### 面试卡答案 / 口述记录
（待填）
