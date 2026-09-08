# D4 — 多智能体 + 框架 + runtime 源码对照

> 日期：____ ｜ 今日面试锚（A）：
> 📖 主阅读（提纯版）：先读 `提纯精读\P4-多智能体与框架提纯.md`，源文件按需深挖**"多智能体 vs 单 agent 多工具？框架怎么选？LangGraph 状态怎么管？"**
> 主轴位置：协同层 + 跨 runtime 对照（总图第四层，同时回照 D1 的 loop）

## 时间盒（≈8.5h 有效学习）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 08:30-09:00 | 主动回忆 | 口述 D3 复盘 3 问 | 3 答记录 |
| 09:00-10:30 | 模式 M | `04-multiagent\multi-agent-arch\README.md` + `01_multi_agent_arch_demo.ipynb` 讲义 + 01.1-01.4（monolithic/pipeline/hub-and-spoke/blackboard）；`02_hierarchical_multi_agent_demo.full.ipynb`（Supervisor/HITL）——mock 无 API 可读 | 编排模式表 |
| 10:30-12:30 | 选型 M | `multi_agent_frameworks_实战.ipynb`（索引）+ `06_agentic_rag_与框架对比.ipynb`（讲义）+ `04_autogen_实战` / `05_crewai_实战`（无 key 只读讲义） | 框架对比初稿 |
| 13:30-16:00 | 实战 D | `11-langgraph\02-Agentic-Chatbot-using-LangGraph\README.md` + `backend\graph.py`、`threads.py`、`rag.py`、`llm.py` 精读；配 .env（DeepSeek key + BGE 本地）试跑 | 见**写码挑战④** |
| 16:00-16:45 | 补缺 | LangGraph Store/checkpointer 深化（对照 threads.py）；`01-project-Complete-Agentic-AI-Course` 中 LangGraph 概念章按需取；TripMate（03 项目）看结构（3 把 key，不必跑） | checkpoint/Store 笔记 |
| 17:00-18:45 | 源码对照 | hermes：`08-hermes-agent\02-run-agent\notes\`（1_agent_loop 等，以目录内为准）+ `hermes-study\run_agent.py` 结构（run_conversation 是 forwarder，真 while 在 agent/conversation_loop.py——本机剪枝无此文件，知道即可）→ waku：`12-hermes-agent-small\waku\loop\agent.py`（~95 行）+ `waku\memory\` → pi：`13-pi-agent\00-learn-guide.md` + `01-arch.md`（Core/Interactive）+ `04-sessions.md`（会话树） | runtime 对照 |
| 20:00-21:30 | 整合 | **框架选型矩阵终版** + 挂总图 + 面试卡 + 口述 | 本文件产出区 |

> 有余力：waku 可用 `uv` + 一把 key 本地跑（Windows 支持，dashboard 端口 7777），跑通即"可讲项目"候选。跑不通不影响今日目标。

## 写码挑战④（60min）

先读懂 `backend\graph.py`，再加一个 2-node 最小流（例如在最终回答前加一个"reflect/校验节点"），跑通或至少写出 diff。这是 5 天里唯一一次"真改真跑"，卡住就退回"写出伪代码 + 说明加在哪"。

## 面试卡（今日自答，次日回填）

1. 多智能体 vs 单 agent 多工具：什么信号说明你需要拆多 agent？（状态隔离/专长/并行/权限）
2. 编排模式：Pipeline / Hub-Spoke / Blackboard / Supervisor(HITL) 各适用什么场景？
3. 框架选型：手写 harness vs LangGraph vs CrewAI vs AutoGen——从 循环控制/记忆/调试/生态 四维答。
4. subagent 与 tool 的区别？（工具=确定性函数；subagent=独立上下文循环）什么时候用 subagent？
5. LangGraph：StateGraph 的节点/边/状态协议；checkpointer + thread_id 怎么实现会话恢复；Store 存什么？
6. HITL 为什么在金融/审批场景是刚需？（你可用银行背景加分）
7. hermes/waku/pi 三个 runtime 的循环实现有什么共性？（都在做：组装上下文→循环→工具→持久化）

## 晚间复盘 3 问（明早 D5 开场口述）

1. 选型矩阵四维各一句话——你推荐中小企业用什么、为什么？
2. 手画 LangGraph chatbot 的状态流（节点/边/threads）。
3. subagent vs tool 的例子各一个。

## 今日产出区

### 编排模式表
（待填：模式/一句话/适用/代价/出处）

### 框架选型矩阵终版

| 维度 | 手写 harness | LangGraph | CrewAI | AutoGen |
|---|---|---|---|---|
| 循环控制（谁拥有 loop） | | | | |
| 记忆/状态 | | | | |
| 调试/可观测 | | | | |
| 生态/上手 | | | | |
| 适用场景一句话 | | | | |

### runtime 对照（hermes / waku / pi）
（待填：循环在哪个文件 / 记忆怎么管 / 会话怎么存）

### 面试卡答案 / 口述记录
（待填）
