# 我的深度整合专题

本目录包含基于原始课程的深度整合文档，采用**概念层→计算层→工程层**三层递进结构。

## 📚 内容目录

### 1. RAG评估深度解析

**核心文档：**
- `RAG_Evaluation_Deep_Dive.md` (2,861行) - 完整的RAG评估体系
- `RAG_Evaluation_Cheatsheet.ipynb`（原记载 768 行）- ⚠️ **2026-09-18 实测：该文件不在仓库中**，速查内容与实战代码目前内嵌在 `RAG_Evaluation_Deep_Dive.md` 里；引用时不要声称已有此 notebook

**配套Notebooks：**
- `01_context_precision_recall.ipynb` - Context Precision & Recall 完整实现
- `02_faithfulness_llm_judge.ipynb` - Faithfulness LLM-as-Judge 流程
- `02_retrieval_ranking_metrics.ipynb` - 排序指标（HitRate/MRR/NDCG）
- `03_answer_relevancy_mrr.ipynb` - Answer Relevancy 语义相似度
- `04_diagnostic_pipeline.ipynb` - 四象限诊断流水线

**特色内容：**
- ✅ 四象限诊断框架（Context vs Answer × Retrieval vs Generation）
- ✅ Binary vs Weighted 公式对比
- ✅ RAGAS 框架完整解析
- ✅ 生产化避坑清单（12条）
- ✅ 面试卡片（概念/计算/工程三层）

**整合来源：**
- B站 AI 模型开发教程 Phase 3 RAG Evaluation 模块
- `02-RAG/04_RAG_Evaluation/` 课程笔记
- `99-My idea/` 设计思路

---

### 2. Agent记忆深度解析

**核心文档：**
- `Agent_Memory_Deep_Dive.md` (1,509行) - Agent记忆完整体系

**配套Notebooks：**
- `01-windowed_memory.ipynb` - 滑动窗口记忆实现
- `02_long_term_memory.ipynb` - 长期记忆（向量检索）
- `03_summary_memory.ipynb` - 摘要记忆（Running Summary）
- `04_three_factor_scoring.ipynb` - 三因子打分排序

**特色内容：**
- ✅ 从"金鱼"到持久智能的演进路径
- ✅ Write/Read/Reconcile/Forget 闭环机制
- ✅ 记忆巩固：从情节到语义（分段摘要 + Observer/Reflector）
- ✅ 记忆系统诊断与优化（Context Rot + 静默失败）
- ✅ 12条避坑清单（含记忆投毒）
- ✅ 面试卡片（概念/计算/工程三层）

**整合来源：**
- `03-memory/` 课程四篇核心 notebook
- `99-My idea/` 设计笔记
- `06-harnes/` 工程实践

---

### 3. 循环工程深度解析（L4a · D1）

**核心文档：**
- `循环工程深度解析\Loop_Engineering_Deep_Dive.md`（567 行）- `09-loop-engineering\` 三文（484+445+424）蒸馏

**特色内容：**
- ✅ 三文关系图（01 合法性/横切配方 → 02 护栏与真相 → 03 落地形态）——三文是**递进且互为前提**，不是并列
- ✅ 四层演进：Prompt → Context → Harness → Loop
- ✅ 三文冲突与我的判断（术语不同、结论一致：独立验证是 Loop 可信的核心）
- ✅ 避坑清单 + 5 分钟速查卡 + 每层面试卡

---

### 4. 推理与路由深度解析（L1 · D3）

**核心文档：**
- `推理与路由深度解析\Model_Route_Deep_Dive.md`（623 行）- `05-model-route\` 11 个模块 + `07-llm_from_scrach` 概念

**特色内容：**
- ✅ 路由/回退/熔断/缓存/计费/治理 11 个模块的机制与伪代码
- ✅ KV cache / MoE / GRPO 的"面试够用"解释
- ✅ 成本治理三段式（before / during / after）+ 选型决策树

---

### 5. 运行时选型深度解析（L4 · D4）

**核心文档：**
- `Agent面试5日冲刺\运行时选型-LangGraph-vs-Hermes.md`（312 行）- **选哪个**：同层二选一、Hermes 是什么、语言门槛、D4 入门路径
- `运行时选型深度解析\Runtime_Five_Way_Deep_Dive.md`（616 行）- **内部怎么实现**：五方对照 + "同一个循环，五种写法"

**特色内容：**
- ✅ LangGraph / Hermes / waku / pi / DSH 五方横向对照（loop 出处到文件中行）
- ✅ 为什么"编排库 + 成品 harness 被叠成两层"会导致 harness 重复建设（含作者 26:13 当场自纠的案例）
- ✅ 多智能体：什么信号才该拆

---

### 6. 观测与评测深度解析（L5 · D5）

**核心文档：**
- `观测与评测深度解析\Observability_Eval_Deep_Dive.md`（546 行）

**特色内容：**
- ✅ 失败归因链（RAG→解析→记忆→mem0→工具→loop→模型→微调）
- ✅ hermes invariants + trace RCA 与 waku tracing/judge/release_gate 两套实现对照
- ✅ 评测进 CI：数据集 → 门禁阈值 → 回归 → trace 可观测
- ✅ LLM-as-judge 三类偏差与缓解；护栏库 ≠ 安全策略

---

### 7. Agent 面试 5 日冲刺（计划与日卡 · 2026-09）

**入口：** `Agent面试5日冲刺\README.md`（**六层栈 v2 总纲**）

| 文件 | 内容 |
|---|---|
| `Agent面试5日冲刺\README.md` | 六层栈 L1-L6 总图、层×天映射、全仓覆盖矩阵、文件核验机制、决策记录 |
| `Agent面试5日冲刺\day1-loop-harness.md` | D1（9/18）总纲 + L4a 循环与 Harness |
| `Agent面试5日冲刺\day2-context.md` | D2（9/19）L2 上下文：记忆 + 知识 |
| `Agent面试5日冲刺\day3-inference-tools.md` | D3（9/20）L1 推理 + L3 动作 |
| `Agent面试5日冲刺\day4-runtime-multiagent.md` | D4（9/21）L4b 运行时选型 + 协同 |
| `Agent面试5日冲刺\day5-observability-closeout.md` | D5（9/22）L5 观测 + L6 界面 + 收口 |
| `Agent面试5日冲刺\核验脚本.py` | **路径真实性核验**：扫描全部 md 的反引号路径，报告 OK/OK~/AMBIG/PLANNED/MISS |
| `Agent面试5日冲刺\提纯精读\README-index.md` | P 文档与模块专题的索引与规范 |

---

## 🎯 与原课程的关系

这些深度整合文档**不是替代**原课程，而是**补充和深化**：

| 层次 | 原课程 | 深度整合专题 |
|------|--------|--------------|
| **入门** | ✅ 快速上手，代码实战 | - |
| **理解** | ✅ 核心概念讲解 | ✅ 三层递进（概念→计算→工程）|
| **深化** | - | ✅ 因果链分析、指标对比、决策树 |
| **生产化** | - | ✅ 诊断框架、避坑清单、持续评估 |
| **面试** | - | ✅ 面试卡片、超精炼速查 |

**互补关系：**
- 原课程：代码为主，快速实践
- 深度整合：原理为主，系统化理解

---

## 📖 推荐阅读顺序

### 学习路径 A：从零开始
1. 先读原课程基础内容（`02-RAG/`, `03-memory/`）
2. 跑通课程中的 Jupyter Notebooks
3. 再读本专题的深度整合文档，建立完整心智模型
4. 结合新增的 Hermes Agent 实践（`08-hermes-agent/`）

### 学习路径 B：面试突击
1. 直接读本专题的深度整合文档
2. 重点看「面试卡片」部分
3. 参考附录的超精炼速查卡（5分钟版）
4. 用配套 Notebooks 验证理解

### 学习路径 C：生产实践
1. 先读原课程和 Hermes Agent 源码（`08-hermes-agent/hermes-study/`）
2. 再读本专题的「第三层·工程层」
3. 重点看诊断框架、避坑清单、持续评估
4. 参考 `10-CICD/` 课程实现 CI/CD

---

## 🛠️ 技术栈与依赖

**核心技术：**
- Python 3.9+
- LangChain / LlamaIndex
- ChromaDB / Pinecone（向量数据库）
- RAGAS（评估框架）
- OpenAI API / DeepSeek API

**Notebooks 运行：**
```bash
pip install langchain openai chromadb ragas python-dotenv
jupyter notebook
```

---

## 📅 版本信息

- **整理时间**：2026-07-20
- **基于版本**：juliepy/AI-Engineer-from-scrach @ main (commit: d5dbb35)
- **文档总量**：4,370 行深度整合内容
- **最后更新**：2026-09-05（迁移到独立专题目录）

---

## 💡 为什么要做这个专题？

在学习原课程时，我发现：

1. **课程内容丰富，但缺少体系化串联** - 各个 notebook 独立，缺少整体视角
2. **实践代码很多，但原理解释不够深** - 知道怎么做，但不知道为什么
3. **面试准备困难** - 要点分散在多个文件中，难以快速复习

因此创建了这个专题，将：
- 4 篇 Memory notebooks → 整合成 1,509 行完整体系
- 6 篇 RAG Evaluation notebooks → 整合成 2,861 行评估框架
- 加入三层递进结构（概念→计算→工程）
- 提炼面试卡片和避坑清单

**目标读者：**
- AI 工程师求职者（需要系统化面试准备）
- 已有基础，想深入理解原理的学习者
- 需要在生产环境部署 Agent/RAG 的工程师

---

## 📧 反馈与改进

如果你发现：
- 概念解释不清晰
- 代码示例有误
- 希望增加某个主题

欢迎通过 GitHub Issues 反馈！

---

**Enjoy your AI Engineering journey! 🚀**
