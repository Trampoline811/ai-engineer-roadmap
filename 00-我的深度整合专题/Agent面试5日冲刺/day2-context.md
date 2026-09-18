# D2 — L2 上下文：记忆 + 知识（RAG）

> **日期：2026-09-19（周六）** ｜ 覆盖层：**L2 上下文（知识 · 记忆）**
> **今日面试锚（A）**：① "你凭什么决定记什么 / 忘什么？" ② "向量库 ≠ RAG——完整管线是什么？" ③ "RAG / 记忆 / 长上下文 三者边界"
> **主阅读（提纯版）**：`00-我的深度整合专题\Agent面试5日冲刺\提纯精读\P2-记忆实现对照提纯.md`（今日新增）
> ＋复用已有资产：`00-我的深度整合专题\Agent记忆深度解析\Agent_Memory_Deep_Dive.md`、`00-我的深度整合专题\RAG评估深度解析\RAG_Evaluation_Deep_Dive.md`（**只复习不重造**）
> ＋`99-My idea\AI Agent 学习指南\01.longterm memory.md`（mem0 详解，965 行，作者详解级证据）

---

## 📎 本日文件核验（逐路径实测）

| 路径 | 状态 | 行数/大小 |
|---|:--:|---|
| `00-我的深度整合专题\Agent面试5日冲刺\提纯精读\P2-记忆实现对照提纯.md` | 🆕 今日生成 | 320–480 |
| `03-memory\04_three_factor_scoring.ipynb` | ✅ | 16.3 KB（**纯 stdlib，可离线**） |
| `03-memory\02_long_term_memory.ipynb` | ✅ | 34.4 KB（mock 向量可离线） |
| `03-memory\01-windowed_memory.ipynb` / `03_summary_memory.ipynb` | ✅ | 13.3 KB / 26.9 KB |
| `06-harnes\learn-claude-code\s09_memory\README.md` / `06-harnes\learn-claude-code\s09_memory\code.py` | ✅ | 280 / 655 |
| `06-harnes\learn-claude-code\s08_context_compact\README.md` / `06-harnes\learn-claude-code\s08_context_compact\code.py` | ✅ | 306 / 524 |
| `06-harnes\learn-claude-code\s03_permission\README.md` | ✅ | 232（**D1 顺延补读**） |
| `06-harnes\learn-claude-code\s10_system_prompt\README.md` | ✅ | 254（**D1 顺延补读**） |
| `08-hermes-agent\01-arch.md` / `08-hermes-agent\02-memory.md` | ✅ | 657 / 651 |
| `08-hermes-agent\01-memory\README.md` | ✅ | 109 |
| `08-hermes-agent\07-mem-provider\README.md` | ✅ | 119 |
| `08-hermes-agent\07-mem-provider\hermes_src\notes\02_memory_manager.md` | ✅ | 341 |
| `08-hermes-agent\07-mem-provider\hermes_src\excerpts\` | ✅ | 7 个接线点（17–74 行） |
| `12-hermes-agent-small\waku\memory\__init__.py` | ✅ | 169 |
| `12-hermes-agent-small\waku\memory\retrieval_gate.py` / `consolidation.py` | ✅ | 55 / 75 |
| `13-pi-agent\04-sessions.md` / `13-pi-agent\05-compaction.md` | ✅ | 195 / 231 |
| `11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\threads.py` | ✅ | 10 |
| `99-My idea\AI Agent 学习指南\01.longterm memory.md` | ✅ | 965 |
| `02-RAG\01-simple_rag\README.md` / `02-RAG\02-RAG_basic\README.md` | ✅ | 176 / 34 |
| `02-RAG\03-high_level_RAG\README.md` | ✅ | 64 |
| `02-RAG\04_RAG_Evaluation\lesson1_rag_evaluation\README.md` | ✅ | 78 |
| `02-RAG\04_RAG_Evaluation\lesson2_rag_metrics\README.md` | ✅ | 150（＋`diagnostic_report.html`） |
| `02-RAG\06 Agentic RAG\code\agentic_rag_demo.py` | ✅ | 200（`--mock` 可离线） |

---

## ⏱ 时间盒（≈8.5h）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 08:30-09:30 | **主动回忆 + 补读** | 口述 D1 三问（不看笔记）；补读 `06-harnes\learn-claude-code\s03_permission\README.md` + `s10_system_prompt\README.md` | 3 答记录 + 权限四决策/组装原则进总图 |
| 09:30-11:00 | **记忆概念 M** | `提纯精读\P2-记忆实现对照提纯.md` 概念层 + 实现层；**跑** `03-memory\04_three_factor_scoring.ipynb`、`03-memory\02_long_term_memory.ipynb` | 三因子公式能背 + 见写码挑战② |
| 11:00-12:30 | **hermes 源码 M** | `08-hermes-agent\02-memory.md` + `01-memory\README.md` + `07-mem-provider\README.md`；**逐个读** `08-hermes-agent\07-mem-provider\hermes_src\excerpts\`（7 个接线点） | provider 生命周期四钩子笔记 |
| 14:00-15:30 | **对照 D** | waku：`12-hermes-agent-small\waku\memory\__init__.py` + `12-hermes-agent-small\waku\memory\retrieval_gate.py` + `12-hermes-agent-small\waku\memory\consolidation.py`；pi：`13-pi-agent\04-sessions.md` + `13-pi-agent\05-compaction.md`；LangGraph：`11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\threads.py` | 三种 runtime 的记忆差异 |
| 15:30-16:15 | ⚔️ **写码挑战②** | 闭卷手写三因子打分（见下） | 差异点笔记 |
| 16:15-17:15 | **RAG 主线 M** | `02-RAG\01-simple_rag\README.md`（最小闭环）+ `02-RAG\02-RAG_basic\README.md`（12 个知识点）→ **RAG 十步管线卡** | 十步管线卡 |
| 17:15-18:45 | **RAG 进阶 + 评测复习** | `02-RAG\03-high_level_RAG\README.md`（五范式）+ `02-RAG\06 Agentic RAG\code\agentic_rag_demo.py` 精读并 `--mock` 跑通；`02-RAG\04_RAG_Evaluation\lesson1_rag_evaluation\README.md` + `02-RAG\04_RAG_Evaluation\lesson2_rag_metrics\README.md` 复习 | Agentic RAG 三幕结构 + 四指标口述 |
| 20:00-21:30 | **整合 A** | **记忆对照表成稿**（模板见产出区）+ RAG 十步管线卡 + **RAG/记忆/长上下文边界卡** + 面试卡 8 问 | 本文件产出区 |

> ⚠️ `02-RAG\03-high_level_RAG\04-graph_rag进阶`（Neo4j）**跑不了**（Docker 未启动）→ 只读概念。
> ⚠️ mem0 是"**作者详解级**"证据（`99-My idea\AI Agent 学习指南\01.longterm memory.md`，无源码）；`dsh-memory-evolve` 是"**源码级**"生产实证。标注不能混。

---

## ⚔️ 写码挑战②（45min，不查 notebook）

手写三因子打分函数（Python，10–15 行），必须包含：

```text
relevance  的 min-max 批内归一化（不是全局归一化）
recency    的指数衰减 exp(-decay × hours)
importance 的加权合成
```

写完与 `03-memory\04_three_factor_scoring.ipynb` 对照，差异写进笔记。**卡住只问"我漏了哪一步"，不要要代码。**

---

## 🎴 面试卡（今日自答，晚间口述给 AI）

1. 记忆三因子（relevance / recency / importance）各是什么公式？为什么"凭什么决定记什么"要用它答？
2. min-max 为什么必须**批内**归一化而不是全局？（提示：候选集每轮都在变）
3. "memory 比 RAG 多两个因子"——怎么解释（**写入准入** vs **检索排序**）？
4. 分层记忆：什么进上下文、什么持久化、什么淘汰？举一个生产系统（`dsh-memory-evolve` 六轨）为例。
5. s08 上下文压缩四层怎么做？与"摘要记忆"什么关系？
6. LangGraph checkpointer/thread_id 与记忆系统是同一件事吗？边界在哪（**会话恢复 vs 长期知识**）？
7. hermes `mem-provider` 的生命周期（initialize / prefetch / sync_turn / shutdown）里，**prefetch 为什么放在 turn 前**？
8. **向量库 ≠ RAG**：完整十步管线是什么？为什么"先查解析，再调检索"？

---

## 🌙 晚间复盘 3 问（明早 D3 开场口述）

1. 三因子公式完整背出，并解释"批内 min-max"的理由。
2. 一条消息的一生里，**记忆出现在哪 3 个节点**？
3. RAG 与记忆都往上下文塞东西，区别用一句话 + 一个例子讲清。

---

## 今日产出区

### ① 记忆对照表（内核问题 × 实现）

★ 最后两列已预填：`dsh-memory-evolve` = 源码级生产实证（`~/.dsh/profiles/web/node_modules/dsh-memory-evolve/lib/store.js` 等，导览见 `prep0-plugin-memory-arch.md`）；mem0 = 作者详解级。

| 内核问题 | 03-memory | harness s09 | hermes(四层+provider) | waku(四层+gate) | pi(会话树) | LangGraph(checkpoint) | mem0（作者详解级） | dsh-memory-evolve（源码级） |
|---|---|---|---|---|---|---|---|---|
| 什么进上下文 | | | | | | | | 全局 MEMORY/USER + 本项目 KEY（按 git 分支过滤）；**daily/project 永不注入**、工具按需读 |
| 什么持久化 | | | | | | | | 纯 md：USER/MEMORY.md + `projects\<hash>\{KEY,MEMORY,TODOS}.md` + daily + SUGGESTIONS.jsonl |
| 什么淘汰 | | | | | | | | ArchiveStore → `*-archive.md` 冷存储，可"移回主记忆" |
| 跨会话恢复 | | | | | | | | 快照注入（live read + 变更检测）；KEY 摘要 ≤80 字 + `[mem-id]` expand |
| provider 抽象 | | | | | | | | 宿主内六轨直管；可选 git 同步 ≈ hermes external provider 层 |
| 防投毒/一致性 | | | | | | | | 威胁扫描 + subagent 禁写全局轨 + 目录锁 + tmp-rename 原子写 |
| 人确认 HITL | | | | | | | | KEY/全局/技能创建 → SuggestionQueue → 记忆 Tab 采纳 |
| 写入触发时机 | | | | | | | | 每轮收尾一次批量写（daily + project） |

### ② RAG 十步管线卡

```
1 接入源 → 2 解析 → 3 保住有用结构 → 4 切分 → 5 向量化 → 6 入库 → 7 召回 → 8 混合检索 → 9 重排 → 10 放进模型上下文
（待填：每步的失败模式 + 本仓库对应文件）
```

### ③ RAG / 记忆 / 长上下文 边界卡

| 维度 | RAG（知识） | 记忆 | 长上下文 |
|---|---|---|---|
| 来源 | | | |
| 更新频率 | | | |
| 评测方式 | | | |
| 成本 | | | |
| 典型失败 | | | |

### ④ 面试卡答案 / 口述记录

（待填）
