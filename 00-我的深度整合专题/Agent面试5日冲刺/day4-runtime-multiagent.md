# D4 — L4b 运行时选型（LangGraph ⊻ Hermes）+ 协同层

> **日期：2026-09-21（周一）** ｜ 覆盖层：**L4 运行时（选型与实现对照）＋ 协同层**
> **今日面试锚（A）**：① "**LangGraph 和 Hermes 是同一层的两条路，默认二选一，不叠两套循环**"（含视频 26:13 作者当场自纠这个案例）② "多智能体 vs 单 agent 多工具，什么信号才该拆？" ③ "五个 runtime 的实现对照我会讲"
> **主阅读（提纯版）**：`运行时选型-LangGraph-vs-Hermes.md`（199 行，选哪个）＋`00-我的深度整合专题\运行时选型深度解析\Runtime_Five_Way_Deep_Dive.md`（今日新增，**它们内部怎么实现**）

---

## 📎 本日文件核验（逐路径实测）

| 路径 | 状态 | 行数/大小 |
|---|:--:|---|
| `00-我的深度整合专题\Agent面试5日冲刺\运行时选型-LangGraph-vs-Hermes.md` | ✅ | 199 |
| `00-我的深度整合专题\运行时选型深度解析\Runtime_Five_Way_Deep_Dive.md` | 🆕 今日生成 | 420–620 |
| `11-langgraph\02-Agentic-Chatbot-using-LangGraph\README.md` | ✅ | 357（**最贴本机环境，可试跑**） |
| `11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\graph.py` | ✅ | 80 |
| `11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\threads.py` | ✅ | 10 |
| `11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\rag.py` / `11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\llm.py` | ✅ | 92 / 106 |
| `11-langgraph\02-Agentic-Chatbot-using-LangGraph\frontend\hitl.py` / `11-langgraph\02-Agentic-Chatbot-using-LangGraph\frontend\chat.py` / `11-langgraph\02-Agentic-Chatbot-using-LangGraph\frontend\session.py` | ✅ | 183 / 207 / 70 |
| `11-langgraph\01-project-Complete-Agentic-AI-Course\README.md` | ✅ | 269 |
| `11-langgraph\01-project-Complete-Agentic-AI-Course\03-LangChain-Multi-Agent-Research-System\README.md` | ✅ | 336 |
| `11-langgraph\03-project-TripMate-AI-A-Multi-Agent-Travel-Planner-with-LangGraph\README.md` | ✅ | 417（3 把 key，不必跑） |
| `08-hermes-agent\09-lang-serial-not\README.md` | ✅ | 352（"Hermes 用了 LangGraph 吗？没有"的实证） |
| `08-hermes-agent\01-arch.md` / `04-arch.md` | ✅ | 657 / 1151（04 选读分层节） |
| `08-hermes-agent\02-run-agent\README.md` | ✅ | 248 |
| `08-hermes-agent\02-run-agent\notes\1_agent_loop.md` / `4_run_conversation_callflow.md` | ✅ | 120 / 367 |
| `08-hermes-agent\02-run-agent\hermes_src\agent\conversation_loop.py` | ✅ | **5355（真源码，在主循环函数段读）** |
| `08-hermes-agent\hermes-study\run_agent.py` | ✅ | 6055（只读函数清单） |
| `12-hermes-agent-small\README.md` / `12-hermes-agent-small\learn_guide.md` / `12-hermes-agent-small\docs\architecture.md` | ✅ | 267 / 608 / 102 |
| `12-hermes-agent-small\waku\loop\agent.py` | ✅ | 113（最小 loop） |
| `12-hermes-agent-small\waku\runtime\session.py` | ✅ | 128 |
| `13-pi-agent\00-learn-guide.md` / `13-pi-agent\01-arch.md` / `13-pi-agent\02-agent-loop.md` | ✅ | 345 / 1039 / 598 |
| `13-pi-agent\03-events.md` / `06-HITL.md` | ✅ | 300 / 182 |
| `14-deepseek-harness\01.arch.md` | ✅ | 296 |
| `04-multiagent\multi-agent-arch\README.md` | ✅ | 136 |
| `04-multiagent\multi-agent-arch\01.1_monolithic_agent.ipynb` … `01.7_graceful_degradation.ipynb` | ✅ | 7 个模式 notebook 全在 |
| `04-multiagent\01-single_vs_multi.py` / `03-phase_state_machine.py` / `04-langgraph_style.py` | ✅ | 102 / 92 / 97 |
| `04-multiagent\09-task_routing.py` / `08-collaboration_patterns.py` | ✅ | 106 / 125 |

> ⚠️ hermes 完整仓库不在本机：`hermes_src` 是**摘录**，`hermes-study` 是**剪枝副本**——只读，不 import、不打断点。
> ✅ 可试跑：`11-langgraph\02-Agentic-Chatbot-using-LangGraph`（DeepSeek key + 本地 BGE）、`12-hermes-agent-small`（uv + 一把 key）。跑不通不影响今日目标。

---

## ⏱ 时间盒（≈8.5h）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 08:30-09:00 | **主动回忆** | 口述 D3 三问（不看笔记） | 3 答记录 |
| 09:00-10:30 | **选型 M** | `运行时选型-LangGraph-vs-Hermes.md` 全读 → 再读 `Runtime_Five_Way_Deep_Dive.md` 的"五方对照表"与"同一个循环，五种写法" | 选型口径定型（能主动提 26:13 自纠） |
| 10:30-12:30 | **LangGraph D** | `11-langgraph\02-Agentic-Chatbot-using-LangGraph\README.md` → `11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\graph.py`（StateGraph 节点/边）→ `11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\threads.py`（checkpointer/thread_id）→ `backend\rag.py` → `11-langgraph\02-Agentic-Chatbot-using-LangGraph\frontend\hitl.py`（人审怎么接）；配 `.env`（DeepSeek key + 本地 BGE）试跑 | LangGraph 机制笔记 + 见写码挑战④ |
| 14:00-15:30 | **Hermes 源码 M** | `08-hermes-agent\09-lang-serial-not\README.md`（为什么它不用 LangGraph）→ `08-hermes-agent\02-run-agent\notes\1_agent_loop.md` + `4_run_conversation_callflow.md` → `08-hermes-agent\02-run-agent\hermes_src\agent\conversation_loop.py`（**只读主循环与停止条件段**） | hermes loop 与迭代预算笔记 |
| 15:30-16:30 | **五方补齐** | waku：`12-hermes-agent-small\waku\loop\agent.py`（113 行）+ `12-hermes-agent-small\docs\architecture.md`；pi：`13-pi-agent\02-agent-loop.md` + `13-pi-agent\03-events.md` + `13-pi-agent\06-HITL.md`；DSH：`14-deepseek-harness\01.arch.md`（tool vs skill / code vs config 话术） | runtime 五方对照填空 |
| 16:30-17:30 | **协同层 M** | `04-multiagent\multi-agent-arch\README.md` + 模式 notebook 讲义（`01.1`–`01.7`：monolithic / pipeline / hub-and-spoke / blackboard / 幂等 / 可观测 / 优雅降级）+ `04-multiagent\01-single_vs_multi.py`、`09-task_routing.py`、`10-conflict_resolution.py` | 编排模式表 + "该不该拆"判据 |
| 17:30-18:45 | ⚔️ **写码挑战④** | 见下（这次是**真改**） | diff 或伪代码 + 说明 |
| 20:00-21:30 | **整合 A** | **框架选型矩阵终版** + runtime 五方对照成稿 + 回填六层栈总纲表 **L4 行** + 面试卡 7 问 | 本文件产出区 |

---

## ⚔️ 写码挑战④（60min，5 天里唯一一次"真改"）

读懂 `11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\graph.py`（80 行）后，**加一个 2 节点最小流**（例如在最终回答前插一个"reflect / 校验节点"），跑通或至少写出 diff。

- 卡住就退回"写出伪代码 + 说明加在哪两个节点之间、边怎么连、state 加什么字段"，**并说明为什么这样改不会破坏 checkpointer 的会话恢复**。
- 这一步的面试价值：能说出"我在 LangGraph 上真加过节点，知道 state 变更要过 reducer"。

---

## 🎴 面试卡（今日自答，晚间口述）

1. **为什么 L4 必须讲成"同层二选一"**？把它讲成上下两层会导致什么工程后果？
2. LangGraph 与 Hermes 的本质差别？（编排库 vs 成品 harness；你还要写什么）
3. "harness 五大件"是什么？（循环 / 状态 / 工具 / 停机 / 人审）在两边分别由谁提供？
4. LangGraph：StateGraph 的节点/边/状态协议；checkpointer + thread_id 怎么实现会话恢复；Store 存什么？
5. HITL 为什么在金融/审批场景是刚需？（**你可以用银行策略流程背景加分**）人审后重放为什么要幂等键？
6. 多智能体 vs 单 agent 多工具：什么信号说明你**该拆**（状态隔离 / 专长 / 并行 / 权限）？
7. subagent 与 tool 的区别？（工具=确定性函数；subagent=独立上下文循环）什么时候用 subagent？

---

## 🌙 晚间复盘 3 问（明早 D5 开场口述）

1. 选型矩阵四维各一句话——中小企业你推荐什么、为什么？
2. 手画 LangGraph chatbot 的状态流（节点 / 边 / thread_id / HITL 中断点）。
3. 五个 runtime 的 loop 分别在哪个文件？说出来（这是"我真读过源码"的硬证据）。

---

## 今日产出区

### ① 框架选型矩阵终版

| 维度 | 手写 harness | LangGraph | Hermes | waku(小 harness) | CrewAI/AutoGen |
|---|---|---|---|---|---|
| 循环控制（谁拥有 loop） | | | | | |
| 状态/记忆 | | | | | |
| 人审 HITL | | | | | |
| 调试/可观测 | | | | | |
| 生态/上手 | | | | | |
| 本机可跑性 | | | | | |
| 适用场景一句话 | | | | | |

### ② runtime 五方对照（loop 出处是硬指标）

| runtime | loop 在哪个文件（全路径+行数） | 状态/会话怎么存 | 工具注册 | HITL | 记忆 | 能跑吗 |
|---|---|---|---|---|---|---|
| LangGraph | | | | | | |
| Hermes | | | | | | |
| waku | | | | | | |
| pi | | | | | | |
| DSH | | | | | | |

### ③ 编排模式表

| 模式 | 一句话 | 适用 | 代价 | 出处 |
|---|---|---|---|---|
| monolithic（单 agent 多工具） | | | | `04-multiagent\multi-agent-arch\01.1_monolithic_agent.ipynb` |
| pipeline | | | | `04-multiagent\multi-agent-arch\01.2_pipeline_mode.ipynb` |
| hub-and-spoke | | | | `04-multiagent\multi-agent-arch\01.3_hub_and_spoke.ipynb` |
| blackboard | | | | `04-multiagent\multi-agent-arch\01.4_blackboard_mode.ipynb` |
| Supervisor / HITL | | | | `04-multiagent\multi-agent-arch\02_hierarchical_multi_agent_demo.full.ipynb` |

### ④ 面试卡答案 / 口述记录

（待填）
