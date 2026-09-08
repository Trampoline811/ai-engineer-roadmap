# D1 — 循环与 Harness（M 中之 M）

> 日期：____ ｜ 今日面试锚（A）：
> 📖 主阅读（提纯版）：先读 `提纯精读\P1a-循环与五范式提纯.md` + `P1b-Harness生命周期提纯.md`（索引见 `提纯精读\README-index.md`），源文件按需深挖（文档内 ↳ 标记处）**"请讲一条用户消息在 agent 里的一生" + "手写/口述一次 ReAct 循环"**
> 主轴位置：循环内核 + Harness 骨架（总图第一层）

## 时间盒（≈8.5h 有效学习）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 08:30-09:00 | 启动 | 通读本目录 `README.md` + 根 `Readme.md` + `00-大纲\Agent教学大纲.md` | 明确作者序 vs 我的序 |
| 09:00-11:00 | 概念 M | `09-loop-engineering\01.context-looop-engineering.md` **精读**（注意文件名拼写 looop）；`02.loop-engineering.md` / `03.loop-engineering.md` 浏览 | 四层演进口述：Prompt→Context→Harness→Loop |
| 11:00-12:30 | 机制 M | `06-harnes\learn-claude-code\s01_agent_loop\README.md` + `code.py`；`s02_tool_use\README.md` + `code.py` | 循环与工具分发机制笔记 |
| 14:00-16:00 | 对照 D | `01-Agent\02-Agent_react\Readme.md` + `agent\loop.py`、`agent\types.py`、`agent\tools\`、`main.py` | 见下方**写码挑战①** |
| 16:00-16:45 | 挂图 | `learn-claude-code\s10_system_prompt\README.md` + `s03_permission\README.md` 快读 | 组装原则 + 权限四决策，进总图 |
| 17:15-19:00 | 范式收口 | 01-Agent 其余 README 快读：`00-llm_function_call`、`02-Plan-and-Execute`、`03-Reﬂexion`（⚠️ 特殊字符，复制原路径）、`04-LATS`、`05-Multi-Agent-Crew` | **五范式对比表**（本文件下方） |
| 20:00-21:30 | 整合 A | 画**生命周期总图 v1** + 面试卡 3-5 张 + 口述自测（录音/打字给 AI） | 本文件"今日产出"区 |

## 写码挑战①（45min，闭卷）

读完 `01-Agent\02-Agent_react\agent\loop.py` 后**合上电脑**，用 Python 伪代码重写最小 ReAct 循环（10-20 行），必须覆盖：while 循环、messages 累积、LLM 调用、解析 tool_call、执行 tool、tool_result 回填、无 tool_call 时返回。允许回忆函数名，**不许抄结构**。写完与 loop.py 对照，把差异点写进笔记（差异 = 你漏掉的机制，通常是停止条件/最大轮数/错误处理）。

## 面试卡（今日先自答，答案次日回填）

1. 一条用户消息从进入系统到返回，经历了哪些阶段？（要求说出 harness 概念：组装、循环、工具、权限、回填、停止）
2. 手写 ReAct 循环；停止条件怎么定（最大轮数 / 无 tool_call / 超时）？
3. harness 和 agent 框架的区别？为什么需要 harness（权限、工具、可观测、回滚）？
4. 五范式演进：function calling → ReAct → Plan-and-Execute → Reflexion → LATS，各自解决什么问题？面试场景怎么选？
5. 工具调用协议有几种？（原生 tools JSON vs 注册中心 vs 手写 Action 文本协议）各自 trade-off？
6. system prompt 里该放什么不该放什么（s10）？权限模型的决策点在哪（s03）？
7. 09-loop 的 Prompt→Context→Harness→Loop 四层，上下文膨胀发生在哪一层？为什么 loop 要独立出来？

## 晚间复盘 3 问（明早 D2 开场口述）

1. 用 ≤5 步讲"一条消息的一生"（不看笔记）。
2. harness 与"直接 while 调 LLM"差在哪三处？
3. 五范式各用一句话说"它比上一个多解决了什么"。

## 今日产出区（填在这里）

### 生命周期总图 v1（ASCII/手绘后拍照）
（待填）

### 五范式对比表

| 范式 | 一句话机制 | 解决什么 | 代价/局限 | 出处 |
|---|---|---|---|---|
| function calling | 模型原生输出结构化工具参数 | 单步工具调用可靠解析 | 只单步，无多轮推理 | 01-Agent\00/01 |
| ReAct | 思考-行动-观察循环 | 多步推理+工具结合 | 无规划、可能绕圈 | 02-Agent_react |
| Plan-and-Execute | 先出计划再逐步执行 | 长任务结构分解 | 计划过期、无法自适应 | 02-Plan-and-Execute |
| Reflexion | 失败后自我批判再试 | 从错误中迭代 | 额外 LLM 开销 | 03-Reﬂexion |
| LATS | 树搜索 + 反思打分 | 复杂决策空间探索 | 成本高 | 04-LATS |
| Multi-Agent-Crew | 多角色分工协作 | 并行/专长 | 编排复杂度 | 05-Multi-Agent-Crew |

### 面试卡答案 / 口述记录
（待填）
