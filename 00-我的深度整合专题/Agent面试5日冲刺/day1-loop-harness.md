# D1 — 总纲 + L4a 运行时内核（循环与 Harness）

> **日期：2026-09-18（周五）** ｜ 起跑时间较晚（今天从 **13:30** 开始），按下方"下午起跑版"时间盒执行
> **今日面试锚（A）**：① 讲清**六层栈**每一层（这是本期最重要的面试资产）② 讲"**一条用户消息在 agent 里的一生**"③ **手写/口述一次 ReAct 循环**
> **覆盖层**：总纲（L1-L6 全览）+ **L4a 循环与 Harness 内核**
> **主阅读（提纯版）**：`00-我的深度整合专题\循环工程深度解析\Loop_Engineering_Deep_Dive.md`（今日新建，含 📍溯源节）；
> 源文三份按需深挖：`09-loop-engineering\` 下 01/02/03

---

## 📎 本日文件核验（逐路径实测，2026-09-18）

| 路径 | 状态 | 行数/大小 | 备注 |
|---|:--:|---|---|
| `00-我的深度整合专题\Agent面试5日冲刺\README.md` | ✅ | 250+ | v2 六层栈版总纲 |
| `00-我的深度整合专题\循环工程深度解析\Loop_Engineering_Deep_Dive.md` | 🆕 今日生成 | 420-620 | 三文蒸馏；若打开时还没生成，先读源文 01 |
| `09-loop-engineering\01.context-looop-engineering.md` | ✅ | 484 | ⚠️ 文件名拼写 **looop**（三个 o） |
| `09-loop-engineering\02.loop-engineering.md` | ✅ | 445 | |
| `09-loop-engineering\03.loop-engineering.md` | ✅ | 424 | |
| `01-Agent\02-Agent_react\Readme.md` | ✅ | 154 | |
| `01-Agent\02-Agent_react\agent\loop.py` | ✅ | **55** | 写码挑战①的对照物 |
| `01-Agent\02-Agent_react\agent\types.py` | ✅ | 9 | 消息/工具调用类型 |
| `01-Agent\02-Agent_react\agent\tools\` | ✅ | 4 文件（24/36/12/6 行） | 注册表 + 3 个工具 |
| `06-harnes\learn-claude-code\s01_agent_loop\README.md` / `06-harnes\learn-claude-code\s01_agent_loop\code.py` | ✅ | 207 / 137 | 最小循环 |
| `06-harnes\learn-claude-code\s02_tool_use\README.md` / `06-harnes\learn-claude-code\s02_tool_use\code.py` | ✅ | 222 / 190 | 工具分发 |
| `06-harnes\learn-claude-code\s10_system_prompt\README.md` | ✅ | 254 | **顺延到 D2 晨 30min** |
| `06-harnes\learn-claude-code\s03_permission\README.md` | ✅ | 232 | **顺延到 D2 晨 30min** |
| `01-Agent\02-Plan-and-Execute\Readme.md` | ✅ | 363 | |
| `01-Agent\03-Reﬂexion\Readme.md` | ✅ | 187 | ⚠️ 目录名含连字 **ﬂ**（U+FB02），复制原路径 |
| `01-Agent\04-LATS\Readme.md` | ✅ | 242 | |
| `01-Agent\05-Multi-Agent-Crew\Readme.md` | ✅ | 149 | |
| `01-Agent\01-small-llm-function-call-project\README.md` | ✅ | 171 | function calling 变体 |
| `00-大纲\Agent教学大纲.md` | ✅ | 44 | **已核验存在**（v1 曾误判不存在）；仅作作者序对照 |

---

## ⏱ 时间盒（下午起跑版，≈7.5h 有效学习，含休息）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 13:30-14:00 | **启动·总纲** | 通读 `README.md` v2 的 §1 六层栈总图 + §3 五日总览；**手抄六层表**（层名 + 候选工具 + 本仓库实证目录） | 六层栈总纲表（骨架） |
| 14:00-15:40 | **概念 M**（L4a） | `循环工程深度解析\Loop_Engineering_Deep_Dive.md` 全读；三文冲突节重点看；源文只在专题的 ↳ 标记处回读 | 四层演进（Prompt→Context→Harness→Loop）能口述 |
| 15:40-16:30 | **对照 D** | `01-Agent\02-Agent_react\Readme.md` + `01-Agent\02-Agent_react\agent\loop.py`（55 行，**逐行读懂**）+ `01-Agent\02-Agent_react\agent\types.py` + `01-Agent\02-Agent_react\agent\tools\__init__.py` | 真实 loop 的结构笔记 |
| 16:30-17:15 | **写码挑战①** | **闭卷**（见下） | 差异点笔记 |
| 17:15-17:30 | 休息 | 离开电脑 | |
| 17:30-19:00 | **机制 M**（L4a） | `06-harnes\learn-claude-code\s01_agent_loop\`（README + code.py）+ `06-harnes\learn-claude-code\s02_tool_use\`（README.md 222 行 + code.py 190 行） | 循环 + 工具分发机制笔记 |
| 19:00-20:00 | 晚饭 | 硬休 | |
| 20:00-21:15 | **范式收口**（L4a） | `01-Agent` 其余 README 快读：`00-llm_function_call`/`01-small-llm-function-call-project`、`02-Plan-and-Execute`、`03-Reﬂexion`、`04-LATS`、`05-Multi-Agent-Crew` | **五范式对比表**成稿 |
| 21:15-22:15 | **整合 A** | 补全六层栈总纲表（先填 **L4 行**：LangGraph ⊻ Hermes 二选一）+ 画**生命周期总图 v1** + 面试卡 7 问自答 + 录 3 问口述 | 本文件"今日产出区" |
| 顺延 D2 晨 30min | 补读 | `s03_permission` + `s10_system_prompt` 快读（权限四决策 + 组装原则） | 并入 D2 卡片 |

---

## ⚔️ 写码挑战①（16:30-17:15，45min，闭卷）

读完 `01-Agent\02-Agent_react\agent\loop.py` 后**合上电脑**，用 Python 伪代码重写最小 ReAct 循环（10-20 行），必须覆盖 7 件事：

```
while 循环 ｜ messages 累积 ｜ LLM 调用 ｜ 解析 tool_call ｜ 执行 tool ｜ tool_result 回填 ｜ 无 tool_call 时返回
```

允许回忆函数名，**不许抄结构**。写完开电脑对照，把**差异点写进笔记**——差异 = 你漏掉的机制（通常是**停止条件 / 最大轮数 / 错误处理 / tool_call 与 tool_result 的配对**）。

> 卡住时找 AI **只提示不代写**：可以问"我漏了哪一类机制"，不要问"给我代码"。

---

## 🎴 面试卡（今日自答，答案晚间口述给 AI）

1. **六层栈**逐层是什么？每层"你选了什么 + 为什么不选另一个"？（**今日主菜**）
2. 一条用户消息从进入系统到返回，经历了哪些阶段？（说出 harness：组装、循环、工具、权限、回填、停止）
3. 手写 ReAct 循环；停止条件怎么定（最大轮数 / 无 tool_call / 超时 / 预算）？
4. harness 和 agent 框架的区别？为什么需要 harness（权限、工具、可观测、回滚）？
5. 五范式演进：function calling → ReAct → Plan-and-Execute → Reflexion → LATS，各自解决什么问题？面试场景怎么选？
6. 工具调用协议有几种？（原生 tools JSON vs 注册中心 vs 手写 Action 文本协议）各自 trade-off？
7. **L4 为什么必须讲成"同层二选一"**？把它讲成上下两层会导致什么工程错误？

---

## 🌙 晚间复盘 3 问（明早 D2 开场口述，不看笔记）

1. 用 **≤5 步**讲"一条消息的一生"。
2. harness 与"直接 while 调 LLM"差在哪**三处**？
3. 五范式各用一句话说"它比上一个多解决了什么"。

---

## 今日产出区（填在这里）

### ① 六层栈总纲表（今日先填 L4 行，其余打钩）

| 层 | 我选什么 | 为什么不选另一个 | 本仓库实证文件 | 一句话面试答法 |
|:--:|---|---|---|---|
| L6 界面 | | | `11-langgraph\02-Agentic-Chatbot-using-LangGraph\frontend\hitl.py`、`12-hermes-agent-small\waku\gateway\` | |
| L5 观测 | | | `08-hermes-agent\03-eval`、`12-hermes-agent-small\waku\ops\` | |
| **L4 运行时** | | | `11-langgraph` / `08-hermes-agent` / `12-...`(waku) / `13-pi-agent` / `14-deepseek-harness` | |
| L3 动作 | | | `06-harnes\learn-claude-code\s02_tool_use\README.md`、`08-hermes-agent\hermes-study\tools\registry.py` | |
| L2 上下文 | | | `02-RAG`、`03-memory`、`08-hermes-agent\07-mem-provider\README.md` | |
| L1 推理 | | | `05-model-route`、`07-llm_from_scrach` | |

### ② 生命周期总图 v1（ASCII 或手绘拍照）

```
（待填：入口 → 组装 → 循环{LLM→工具→回填} → 停止 → 状态写入 → 观测）
```

### ③ 五范式对比表

| 范式 | 一句话机制 | 解决什么 | 代价/局限 | 出处（路径+行数） |
|---|---|---|---|---|
| function calling | 模型原生输出结构化工具参数 | 单步工具调用可靠解析 | 只单步，无多轮推理 | `01-Agent\00-llm_function_call.py`(334) / `01-small-llm-function-call-project`(171) |
| ReAct | 思考-行动-观察循环 | 多步推理 + 工具结合 | 无规划、可能绕圈 | `01-Agent\02-Agent_react`(Readme 154 / loop.py 55) |
| Plan-and-Execute | 先出计划再逐步执行 | 长任务结构分解 | 计划过期、无法自适应 | `01-Agent\02-Plan-and-Execute`(363) |
| Reflexion | 失败后自我批判再试 | 从错误中迭代 | 额外 LLM 开销 | `01-Agent\03-Reﬂexion`(187) |
| LATS | 树搜索 + 反思打分 | 复杂决策空间探索 | 成本高 | `01-Agent\04-LATS`(242) |
| Multi-Agent-Crew | 多角色分工协作 | 并行 / 专长 | 编排复杂度 | `01-Agent\05-Multi-Agent-Crew`(149) |

### ④ 面试卡答案 / 口述记录

（待填）
