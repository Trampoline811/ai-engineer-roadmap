# D2 — L2 上下文：记忆 + 知识（RAG）

> 日期：2026-10-12（周一） ｜ 覆盖层：L2 上下文（知识 · 记忆）
> 今日面试锚（A）：① "你凭什么决定记什么 / 忘什么？" ② "向量库 ≠ RAG（检索增强生成，Retrieval-Augmented Generation）——完整管线是什么？" ③ "RAG / 记忆 / 长上下文 三者边界"
> 主阅读（提纯版）：`00-我的深度整合专题\Agent面试5日冲刺\提纯精读\P2-记忆实现对照提纯.md`（837 行，全读）
> ＋复用已有资产：`00-我的深度整合专题\Agent记忆深度解析\Agent_Memory_Deep_Dive.md`、`00-我的深度整合专题\RAG评估深度解析\RAG_Evaluation_Deep_Dive.md`（只复习不重造）
> ＋`99-My idea\AI Agent 学习指南\01.longterm memory.md`（mem0 详解，965 行，作者详解级证据）

---

## 本日文件核验（逐路径实测）

| 路径 | 状态 | 行数/大小 |
|---|:--:|---|
| `00-我的深度整合专题\Agent面试5日冲刺\提纯精读\P2-记忆实现对照提纯.md` | ✅ 已就绪 | 837 |
| `03-memory\04_three_factor_scoring.ipynb` | ✅ | 16.3 KB（纯 stdlib，可离线） |
| `03-memory\02_long_term_memory.ipynb` | ✅ | 34.4 KB（mock 向量可离线） |
| `03-memory\01-windowed_memory.ipynb` / `03_summary_memory.ipynb` | ✅ | 13.3 KB / 26.9 KB |
| `06-harnes\learn-claude-code\s09_memory\README.md` / `06-harnes\learn-claude-code\s09_memory\code.py` | ✅ | 280 / 655 |
| `06-harnes\learn-claude-code\s08_context_compact\README.md` / `06-harnes\learn-claude-code\s08_context_compact\code.py` | ✅ | 306 / 524 |
| `06-harnes\learn-claude-code\s03_permission\README.md` | ✅ | 232（D1 已读，口述卡壳时回看） |
| `06-harnes\learn-claude-code\s10_system_prompt\README.md` | ✅ | 254（D1 已读，口述卡壳时回看） |
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

## 时间盒（压缩版，约 7h，13:00 起跑）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 13:00-13:20 | 主动回忆 | 闭卷口述 D1 三问，答案在 `day1-loop-harness.md` 的晚间复盘一节 | 3 答记录 |
| 13:20-15:00 | 记忆概念 | `提纯精读\P2-记忆实现对照提纯.md`（837 行）概念层与实现层；源文件只在标 `↳深挖` 处回查 | 三因子公式能口述 |
| 15:00-16:00 | 跑 notebook | `03-memory\04_three_factor_scoring.ipynb`（纯 stdlib）+ `03-memory\02_long_term_memory.ipynb`（mock 向量） | 说得出两本各验证了什么 |
| 16:00-16:25 | 写码挑战② | 闭卷手写三因子打分（见下，25 分钟） | 差异点笔记 |
| 16:25-17:30 | 记忆对照表 | 8 个内核问题 × 8 套实现，填产出区 ① | 对照表成稿 |
| 19:30-20:30 | RAG 主线 | `02-RAG\01-simple_rag\README.md`（176）+ `02-RAG\03-high_level_RAG\README.md`（64）；跑通 `02-RAG\06 Agentic RAG\code\agentic_rag_demo.py --mock`（200 行） | RAG 十步管线卡 |
| 20:30-21:30 | 整合 | 十步管线卡 + 边界卡成稿 + 面试卡 8 问口述 | 本文件产出区 ②③④ |

压缩掉四个整篇读的段落，内容已由 P2 覆盖：hermes 源码（`08-hermes-agent\02-memory.md` 651 + `08-hermes-agent\01-memory\README.md` 109 + `08-hermes-agent\07-mem-provider\README.md` 119 + excerpts 7 个接线点）、waku 记忆层（`12-hermes-agent-small\waku\memory\` 的 169 + 55 + 75）、pi 会话树（`13-pi-agent\04-sessions.md` 195 + `13-pi-agent\05-compaction.md` 231）、LangGraph 检查点（`11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\threads.py` 10）。这些文件只在填对照表遇到疑问时按需回查，不再整篇读。

> ⚠️ `02-RAG\03-high_level_RAG\04-graph_rag进阶`（Neo4j）跑不了（Docker 未启动）→ 只读概念。
> ⚠️ mem0 是「作者详解级」证据（`99-My idea\AI Agent 学习指南\01.longterm memory.md`，无源码）；`dsh-memory-evolve` 是「源码级」生产实证。标注不能混。

---

## 写码挑战②（25 分钟，不查 notebook）

手写三因子打分函数（Python，10–15 行），必须包含：

```text
relevance  的 min-max 批内归一化（限定在同批候选集内部，不做全库归一化）
recency    的指数衰减 exp(-decay × hours)
importance 的加权合成
```

写完与 `03-memory\04_three_factor_scoring.ipynb` 对照，差异写进笔记。卡住只问「我漏了哪一步」，不要要代码。

---

## 面试卡（今日自答，晚间口述）

1. 记忆三因子 relevance（相关性）/ recency（近期性）/ importance（重要性）各是什么公式？为什么"凭什么决定记什么"要用它答？
2. min-max 为什么必须批内归一化，而不能对整库做？（提示：候选集每轮都在变）
3. "memory 比 RAG 多两个因子"——怎么解释（写入准入 与 检索排序）？
4. 分层记忆：什么进上下文、什么持久化、什么淘汰？举一个生产系统（`dsh-memory-evolve` 六轨）为例。
5. s08 上下文压缩四层怎么做？与"摘要记忆"什么关系？
6. LangGraph 的 checkpointer（检查点器）与 thread_id（线程标识）和记忆系统是同一件事吗？边界在哪（会话恢复 与 长期知识）？
7. hermes `mem-provider` 的生命周期（initialize / prefetch / sync_turn / shutdown）里，prefetch（预热召回）为什么放在 turn 前？
8. 向量库 ≠ RAG：完整十步管线是什么？为什么"先查解析，再调检索"？

---

## 晚间复盘 3 问（10-13 开场口述）

1. 三因子公式完整背出，并解释"批内 min-max"的理由。
2. 一条消息的一生里，记忆出现在哪 3 个节点？
3. RAG 与记忆都往上下文塞东西，区别用一句话 + 一个例子讲清。

---

## 今日产出区

### ① 记忆对照表（内核问题 × 实现）

★ 最后两列已预填：`dsh-memory-evolve` = 源码级生产实证（`~/.dsh/profiles/web/node_modules/dsh-memory-evolve/lib/store.js` 等，导览见 `prep0-plugin-memory-arch.md`）；mem0 = 作者详解级。

| 内核问题 | 03-memory | harness（外壳工程） s09 | hermes（四层 + provider（提供方）） | waku（四层 + gate（检索闸门）） | pi（会话树） | LangGraph（checkpoint（检查点）） | mem0（作者详解级） | dsh-memory-evolve（源码级） |
|---|---|---|---|---|---|---|---|---|
| 什么进上下文 | | | | | | | | 全局 MEMORY/USER + 本项目 KEY（按 git 分支过滤）；daily/project 永不注入、工具按需读 |
| 什么持久化 | | | | | | | | 纯 md：USER/MEMORY.md + `projects\<hash>\{KEY,MEMORY,TODOS}.md` + daily + SUGGESTIONS.jsonl |
| 什么淘汰 | | | | | | | | ArchiveStore → `*-archive.md` 冷存储，可"移回主记忆" |
| 跨会话恢复 | | | | | | | | 快照注入（live read + 变更检测）；KEY 摘要 ≤80 字 + `[mem-id]` expand |
| provider（提供方）抽象 | | | | | | | | 宿主内六轨直管；可选 git 同步 ≈ hermes external provider 层 |
| 防投毒/一致性 | | | | | | | | 威胁扫描 + subagent 禁写全局轨 + 目录锁 + tmp-rename 原子写 |
| 人确认 HITL（人在回路） | | | | | | | | KEY/全局/技能创建 → SuggestionQueue → 记忆 Tab 采纳 |
| 写入触发时机 | | | | | | | | 每轮收尾一次批量写（daily + project） |

### ② RAG 十步管线卡

```text
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
