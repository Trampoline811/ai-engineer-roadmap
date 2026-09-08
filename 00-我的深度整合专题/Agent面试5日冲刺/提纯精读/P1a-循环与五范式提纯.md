# P1a 循环与推理范式（提纯版）

> 生成日期：2026-09-07 ｜ 用途：Agent 面试冲刺 D1 精读主文档
> 阅读法：先 §5 五分钟速查卡 → §1 概念层 → §2/§3 按需回看 → §4 面试卡自测（先自答再看答案）；标 `↳深挖` 的点面试前回源。

### 📍 本页定位与蒸馏溯源（必读，先回答"我在哪、从哪来、为什么这样提纯"）

- **在整体计划中的位置**：5 日冲刺 **D1「循环与 Harness」** 的主阅读之一（另一篇 `P1b-Harness生命周期提纯.md` 讲循环的工程外壳）。主轴位置 = "一条用户消息的一生"第一层：**循环内核（M 中之 M）**。D1 读法：先本页建立"循环是什么、范式怎么演进"，再读 P1b 建立"循环的工程外壳"，最后动笔画"生命周期总图 v1"。
- **被蒸馏文档（共 12 个源路径，与 §0 表逐行一一对应）**——主干明细（每个 1 行，讲它讲什么；逐项"提炼点↔↳深挖"见下方 §0 表）：
  - `09-loop-engineering/01.context-looop-engineering.md`：四层演进总纲——Prompt→Context→Harness→Loop 每层补上一层的什么缺口（NASA 三问佐证）+ 长期维护的六组件。
  - `09-loop-engineering/02.loop-engineering.md`：Loop 怎么搭——定义、"Loop=Cron+决策体"、ReAct→AutoGPT→纪律型谱系、独立 Verification、烧钱护栏、Orchestration Tax。
  - `09-loop-engineering/03.loop-engineering.md`：Loop 何时用——Trigger/Action/Stop 三件套、Goal+Verification 两柱、三种形态与"别急着上舰队"。
  - `01-Agent/README.md`：六套课程总纲——五范式一句话定位、演进树、建议讲课顺序、统一工具集约定。
  - `01-Agent/00-llm_function_call/llm_function_call.py` + `llm_function_call.ipynb`：原生 Function Calling 最小演示——tools JSON Schema → 模型返回 `tool_calls` → 本地执行 → `role=tool` 回填。
  - `01-Agent/00-llm_function_call/prompt.ipynb`：裸对话 API 基线（system prompt + thinking/reasoning），作为"无工具"对照形态。
  - `01-Agent/01-small-llm-function-call-project/README.md`：FC 工程化小项目——注册中心 `TOOL_HANDLERS`+`TOOLS`、两轮 LLM 消息编排、3 步加工具。
  - `01-Agent/02-Agent_react/Readme.md` + `agent/` 全套代码：手写 Action 文本协议的最小 ReAct——`loop.py` 55 行主循环真身（伪代码在 §2.1）。
  - `01-Agent/02-Plan-and-Execute/Readme.md`：Planner+Executor 双层循环——显式 3–7 步规划、`state` 逐步执行、失败整体重规划、单步复用 ReAct。
  - `01-Agent/03-Reﬂexion/Readme.md`：反思范式——Action→Evaluator(规则优先 LLM 兜底)→Reflector 写策略记忆→跨 Trial 复用，含裁剪参数与运行示例。
  - `01-Agent/04-LATS/Readme.md`：树搜索范式——LATS/MCTS 四步（Select/Expand/Simulate/Backprop）、UCB 公式与 budget 参数、与 ReAct/Beam 对比。
  - `01-Agent/05-Multi-Agent-Crew/Readme.md`：多角色协作概念演示——researcher/writer/reviewer 共享 `thread` 黑板、rounds×order、无状态 LLM 靠全量重发。
- **蒸馏理由与方法（约 120 字）**：作者把"循环"拆成 09-loop 三篇理论 + 01-Agent 六套工程；散读会反复撞见同一内核——每套课程其实都是"在循环上加一层机制"。蒸馏 = 先通读全部，抽出演进主线（一次调用→Agent 回合→多步任务），再把六套范式按"比上一个多解决什么"排成一条演进链，每套只保留它在循环上的**改动点**；代码只提纯 ReAct 主循环（55 行），其余范式只记 delta，最后把散落在讲义与 README 里的停止/预算参数收敛成一张速查卡。知其然（每套机制讲什么），也知其所以然（课程为何按此顺序排、范式如何纵向/横向叠加）。

---

## 0 定位与源文件清单

本专题把「循环工程（Loop Engineering）三文」与「01-Agent 六套课程工程」筛选提纯成一份文档：概念层讲清「从一次 LLM 调用到一条自我驱动 Loop」的主线；
实现层给出一套可复述的 ReAct 代码结构 + 五种范式各自在循环上的改动点；
工程层总结停止条件 / 验证 / 成本护栏等生产要点。
仓库内 RAG 课程（外部知识获取）只在概念上与 Agent 对比（见 `01-Agent/README.md` 末节），Harness（`06-harnes/`）与记忆（`08-hermes-agent/`）仅被引用，不展开。

| 源路径（相对仓库根） | 本文提炼点 | ↳深挖? |
|---|---|---|
| `09-loop-engineering/01.context-looop-engineering.md`（484 行） | 四层演进、NASA 三层对照、六组件、世界杯用例 | ↳「为什么需要 harness」回读 §3–§6 |
| `09-loop-engineering/02.loop-engineering.md`（445 行） | Loop 定义、Cron 之辩、ReAct→AutoGPT→纪律型 Loop 谱系、Verification、Orchestration Tax、花费上限 | ↳「怎么防烧钱/自嗨」回读 §5–§8 |
| `09-loop-engineering/03.loop-engineering.md`（424 行） | Trigger/Action/Stop 三件套、Goal+Verification 两柱、Reason→Act→Observe、三种形态 | 已收进 §1.3/§3，可不回 |
| `01-Agent/README.md`（77 行） | 五范式定位、演进树、共用工具集约定 | 已收进 §1.2，可不回 |
| `01-Agent/00-llm_function_call/llm_function_call.py` + `llm_function_call.ipynb` | 原生 Function Calling 协议（tools JSON Schema / tool_calls / role=tool 序列） | 已收进 §2.2 ① |
| `01-Agent/00-llm_function_call/prompt.ipynb` | 裸对话 API 形态（system prompt + thinking/reasoning） | 概念参考，可不回 |
| `01-Agent/01-small-llm-function-call-project/README.md` | 注册中心（`TOOL_HANDLERS`+`TOOLS`）、两轮 LLM 编排 | 已收进 §2.2 ② |
| `01-Agent/02-Agent_react/Readme.md` + `agent/loop.py types.py prompt.py config.py tools/ llm/` | 手写 Action 文本协议的最小 ReAct；55 行主循环是 §2.1 伪代码真身 | ↳白板写 ReAct 前必回 `loop.py`+`prompt.py` |
| `01-Agent/02-Plan-and-Execute/Readme.md` | Planner+Executor、state、失败重规划、单步内嵌 ReAct(max_steps=4) | 已收进 §2.3，细节可回 |
| `01-Agent/03-Reﬂexion/Readme.md`（⚠️目录名含连字 ﬂ=U+FB02） | Action→Eval→Reflect→Retry、Evaluator 规则优先 LLM 兜底、reflections 策略记忆裁剪 | ↳「反思怎么做才不冗余」回读 |
| `01-Agent/04-LATS/Readme.md` | LATS/MCTS 四步、UCB 公式、预算参数 | ↳「树搜索成本与工程难点」回读 |
| `01-Agent/05-Multi-Agent-Crew/Readme.md` | thread 共享黑板、角色隔离、rounds×order 双循环 | 已收进 §1.2/§2.3，可不回 |

> 技术事实一律以源文件为准；源文件未见的内容标注「仓库内未见」，不编造。

---

## 1 概念层：从一次调用到一次推理

### 1.1 演进主线：一次 LLM 调用 → 一次 Agent 回合 → 一个多步任务

统一类比（面试开场白）：
**一次 LLM 调用** = 把问题递给聪明但健忘的员工，他答完就忘；
**一次 Agent 回合** = 允许他边查资料（调工具）边回答，查到的每条都摊在桌上；
**一个多步任务 / Loop** = 把他升级成项目组——先做计划、做完自检、错了重来、跨天还记得做到哪。
这条主线是本专题的坐标轴。

**第一档：一次 LLM 调用（无状态）**。
形态：`chat.completions.create(messages=[...])` 一问一答。
证据：`01-Agent/00-llm_function_call/prompt.ipynb`（裸对话：system+user 两条即返回，无工具、无循环）；
`05-Multi-Agent-Crew` 的 Readme 点破本质——「无状态 LLM：每次调用是独立 API，上下文靠 thread 传递」。

**第二档：一次 Agent 回合（多轮调用 + 工具）**。
在调用外加循环：模型输出意图 → 执行器调工具 → 结果（Observation）塞回上下文 → 再调模型，直到出现终止信号（Final Answer / 不再调工具）。
这是 ReAct 与原生 Function Calling 的运行时形态；
上下文随轮次增长——这是后面所有工程问题的起点。

**第三档：一个多步任务（状态 + 验证 + 调度）**。
单回合扛不住时（§1.3 的 Context 缺口），需外置任务列表与状态、显式验证门、以及决定「下一轮是否开启、开启什么」的调度层。
`01-Agent/README.md` 的五范式演进树正是这条主线的课程化表达：

```
ReAct（基础循环）
  ├── Plan-and-Execute（加显式规划层：先出计划书再逐步执行）
  ├── Reflexion（加评估与反思层：做错了把教训带进下一轮）
  └── LATS（加树搜索：不只走一条路，探索多条再择优）
Multi-Agent-Crew（横向扩展：多个角色协作，可与上面纵向叠加）
```

**面试怎么说**：不要背定义，用「无状态调用 → 上下文里叠工具结果 → 状态外置 + 验证 + 调度」三档递进，再落到实证——「我读过的 ReAct 实现，每轮把 (thought, action, input, observation) 四元组追加进 history 再发回模型」。

### 1.2 五范式对比表（课程主线）

表列：范式（仓库目录）｜一句话机制｜比上一个多解决了什么｜主要代价｜出处文件。
顺序即课程顺序：ReAct 起手逐层加东西；
Function Calling 是最底层能力。

| 范式 | 一句话机制 | 比上一个多解决什么 | 主要代价 | 仓库出处 |
|---|---|---|---|---|
| Function Calling（`00-llm_function_call/`、`01-small-llm-function-call-project/`） | JSON Schema 声明工具，模型返回结构化 `tool_calls`，本地执行后以 `role=tool` 回填 | 让模型能按协议调用外部函数（前置能力，非完整 Agent） | 仅工具往返，无推理步、无自主多轮规划 | `llm_function_call.ipynb`、`01-.../README.md` |
| ReAct（`02-Agent_react/`） | 每轮 Thought→Action→(Observation)→…→Final Answer，推理与行动交替 | 把「想一步做一步」显式化，可解释、可随时改工具 | 步数多则 token/延迟高；贪心单链易短视 | `agent/loop.py`（55 行主循环） |
| Plan-and-Execute（`02-Plan-and-Execute/`） | Planner 先全局拆 3–7 步，Executor 逐步执行并汇总，失败可整体重规划 | 治 ReAct「走一步看一步」的短视，产出可审计计划书 | 灵活性下降；计划错了全局重来 | `Readme.md`（planner 主循环图） |
| Reflexion（`03-Reﬂexion/`） | Action→Evaluator（规则/LLM 打分）→失败则 Reflector 写反思入策略记忆→带反思重试 | 治「重试不带教训」：跨尝试复用反思 | 每轮多 1–2 次 LLM 调用；反思需裁剪防膨胀 | `Readme.md` 伪代码、evaluator/reflector |
| LATS / MCTS（`04-LATS/`） | 决策当树搜索：UCB 选节点→LLM 扩 k 个候选→scorer 估分→回传更新价值 | 治「一条路走到黑」：多方案探索后按节点价值择优 | 成本显著更高（多分枝+多次 score+树预算） | `Readme.md` MCTS 四步、UCB 公式 |
| Multi-Agent-Crew（`05-Multi-Agent-Crew/`） | 多角色轮流读同一条 `thread` 并追加；rounds 外环 × order 内环 | 横向分工+共享黑板：研究→撰写→审稿可迭代 | thread 全量重发（上下文成本线性涨）；无并行/无工具仅为概念 | `Readme.md` thread 成长、roles.py |

选型一句话（源自 `01-Agent/README.md` 五范式对比表 + `02-Plan-and-Execute/Readme.md` 对比表）：路径不确定、频繁与环境交互 → ReAct；
任务可分解、要可审计计划书 → Plan-and-Execute；
可验证且易犯格式/约束错 → Reflexion；
决策点多、可打分、要多方案对比 → LATS；
内容生产/流水线协作 → Multi-Agent。

**面试怎么说**：把演进树背成因果链——「ReAct 是最小完整循环；
往上每加一层都补上一层的缺口：规划补短视、反思补教训复用、树搜索补路径单一、多角色补单脑容量」——比单背「五种范式」高一个量级。

### 1.3 09-loop 三文骨架：Prompt→Context→Harness→Loop 四层演进

核心命题（`09-loop-engineering/01.context-looop-engineering.md`）：**工程范式不断叠「环」；每层不取代下一层，而是上一层留下结构性缺口时，把环往外再长一层。**

| 层级 | 解决什么 | 谁发起下一轮 | 留下的缺口 |
|---|---|---|---|
| Prompt Engineering | 用自然语言约束角色/行为 | 人类一次提问 | 上下文大多空着 |
| Context Engineering | 让 Agent 自主调工具装填上下文（文件/MCP/搜索） | Agent 调工具直到足够 | 长任务会 choke、摘要会泄漏 |
| Harness Engineering | 长任务不靠上下文硬扛：外置拆任务、管 Runtime | 外部系统管理任务与运行时 | 仍要人不断发起下一轮 |
| Loop Engineering | 减少人类持续催促 | 调度与状态驱动下一轮 | ——（最外层） |

**上下文膨胀发生在哪（面试关键）**：① Context 层每次工具结果都写回窗口，任务超过约 **5–10 分钟**，所需上下文常超出窗口；
② 靠「快满了就自己总结」会**泄漏**——每轮摘要都丢细节；
③ 这两条正是 Harness 存在的理由：**在 context 之外**管理任务列表与 runtime，而不是把整条流水线硬塞进模型窗口。

NASA 三层对照（强烈建议背，三问对齐三层）：闭卷推理「地球月亮间塞多少芝士汉堡」→ Prompt；
「NASA 最近有什么发现」要检索装填 → Context；
「把整个 NASA 官网 clone 下来」超长多步 → Harness。

**Loop 的本质**（`02.loop-engineering.md` 开头）：你不再不停 prompt coding agent，你设计**会去 prompt agent 的 loop**——职责上移：人定义目标与停机条件，orchestrator 按状态持续发起下一轮。
「Prompting 没有死，只是搬到了最开始（种子）」。

Loop 谱系（`02` 文 §2，时间线答题利器）：while 里塞模型 → ReAct(2022，Agent 范式成型) → AutoGPT(2023，目标驱动自我 prompt，**常空转烧 token 几乎不交付**) → **纪律型 Loop（今）**：固定指令 + 每轮重置上下文 + **独立检查说停才停**（Claude Code / Codex 主流形态）。

Loop ≠ Cron（`02` 文 §3）：Cron = 定时触发 → 跑固定脚本 → 结束；
Loop = 触发 → 读当前状态 → 模型决定下一步 → 执行 → 检查 → 再决定是否继续。
一句话：**Loop = Cron + decision maker in the body**。

最小工作单元（`03` 文 §4）：**Reason → Act → Observe → 达 Done？** Observe 可以是跑测试 / 截图 / 浏览器检查，取决于任务。

六组件（`01.context` 文 §9，Addy Osmani）：**Automations**（定时发现与分诊，没有它只是跑过一次不是 loop）、**Worktrees**（并行隔离工作树）、**Skills**（SKILL.md 固化约定）、**Plugins & Connectors**（MCP/Issue/API 接真实工具链）、**Sub-agents**（Maker–Checker：做的人 ≠ 验的人）、**Memory / State**（磁盘持久化「已做/下一步」）。
文中强调：**Memory/State 最不起眼，却是跨 run 能复合而不是重置的关键**——「模型会忘，仓库与文件不会」。

三种 Loop 形态（`03` 文 §5，工程选型用）：**Solo Loop**（默认首选，验证闭环即可；
风险=自评偏差）→ **Maker–Checker**（需独立打分/主观任务客观化）→ **Manager + Helpers**（可拆并行子任务；
成本与理解鸿沟放大）。

**面试怎么说**：四层讲成「能力边界外扩史」而非名词堆叠；
被问「要不要给产品上 loop」就搬 `03` 文先问两问——① Done 是什么？② 如何检查？——再加一句「**Loop 的上限 = Done Check 的上限**」（Abbey Road 硬顶 8 轮仍可能不像，说明验证方式决定天花板）。

---

## 2 实现层：代码结构提纯

### 2.1 `02-Agent_react/agent/` 模块切分与最小 ReAct 伪代码

仓库里最干净、可完整复述的实现。
模块切分（依赖方向自上而下）：

| 文件 | 职责 | 关键签名/常量（源码事实） |
|---|---|---|
| `agent/loop.py` | ReAct 主循环（全文仅 55 行） | `react_loop(question, tools, llm, max_steps=6) -> str` |
| `agent/prompt.py` | 拼每轮 prompt + 解析模型输出 | `build_prompt(question, history, tools)`；`parse_action(text) -> (action, action_input)` |
| `agent/types.py` | 工具类型 | `Tool = dataclass(name, description, run: Callable[[str], str])` |
| `agent/tools/__init__.py` | 工具注册 | `build_default_tools() -> Dict[str, Tool]`（calculator / get_current_time / word_count） |
| `agent/tools/calculator.py` | 安全计算器 | `ast` 白名单求值（+ - * / // % 与乘方、括号），不是 eval |
| `agent/config.py` | 环境变量 | `load_env()` 从项目根读 `.env`（python-dotenv 可选） |
| `agent/llm/deepseek.py` | LLM 接入 | `create_deepseek_llm() -> Callable[[str], str]`，temperature=0 |
| `main.py` | 入口 | 组装 tools + llm，跑一次示例问题 |

关键类型即「Agent 的记忆模型」（`loop.py` 第 7 行）：`history: List[Tuple[thought, action, action_input, observation]]`——每轮把「想、做、输入、观察到」四元组追加进列表，下一轮原样拼回 prompt。
这就是循环内记忆的全部机制。

**最小 ReAct 伪代码（提炼自 `agent/loop.py`，面试可白板默写）**

```python
def react_loop(question, tools, llm, max_steps=6):
    history = []                    # [(thought, action, input, observation)]
    for step in 1..max_steps:
        prompt = build_prompt(question, history, tools)
        #   = 格式模板 + 工具清单 + 工具描述 + Question + 历史四行回放
        out = llm(prompt)           # 一次无状态调用
        action, action_input = parse_action(out)   # 行匹配 "Action:" / "Action Input:"

        if action in tools:                          # 合法工具 → 先执行
            obs = tools[action].run(action_input)    # 忽略同条回复里的 Final Answer
            history.append((thought, action, action_input, obs))
            continue                                 # 回环再来一轮

        if "Final Answer:" in out:                   # 终止信号
            return out.split("Final Answer:", 1)[1].strip()

        # 非法 Action：把错误当 Observation 写回 history（错误可见、可自愈）
        history.append(("", action, action_input,
                        "ERROR: invalid Action. Must be one of ..."))
    return "Failed: max steps exceeded."             # 硬顶兜底
```

**这份代码暗藏的三个实现决策（面试都值得展开）**：

1. **停止条件 = 文本信号 + 步数硬顶**：正常出口 = 检测到 `Final Answer:`；
     异常出口 = `max_steps`（默认 6）耗尽返回失败串。
     两步互不依赖、缺一不可。
2. **工具协议 = 手写 Action 文本协议**（§2.2 变体③）：模型被要求输出 `Thought:` / `Action:` / `Action Input:` 文本行，靠 `prompt.py::parse_action` 逐行字符串解析——不依赖模型原生 function calling，通吃能读写的模型；
     代价：格式错就解析错、参数无类型。
3. **出错不中断，错误进上下文**：非法 Action 时把 `ERROR: invalid Action. Must be one of [tools]` 当作一条 Observation 记入 history 再循环，让模型看到自己的错误并自纠而非抛异常——这是「LLM 循环」与「传统程序循环」气质差异的典型样本。

`prompt.py::build_prompt` 的格式纪律（它在替解析器打工）：`"You solve tasks with tools. Use EXACTLY this format each turn"` + 每轮只准输出一个回合（Thought+Action+Action Input **或** Thought+Final Answer）+ 历史以四行回放。
结论：**解析器有多简单，prompt 的格式纪律就有多硬。**

### 2.2 工具协议三变体（在仓库何处出现）

| 变体 | 机制 | 仓库出处 | 优劣 |
|---|---|---|---|
| ① 原生 tools JSON（Function Calling） | API 层注册 `tools=[{type:"function", function:{name, description, parameters(JSON Schema)}}]`；模型返回 `message.tool_calls[0].function.arguments`（JSON 串）；本地执行后按顺序追加 `role=assistant`(含 tool_calls) 再追加 `role=tool`(须带 `tool_call_id`)，再发下一轮 | `00-llm_function_call/llm_function_call.py`（get_weather 示例，含 `json.loads(tool.function.arguments)` 与消息回填）；`01-small-llm-function-call-project/README.md` 时序图 | 参数结构化、免文本解析、可并行；但绑定支持该协议的模型与 SDK |
| ② 注册中心 | `tools/__init__.py` 集中导出 `TOOL_HANDLERS`（name→函数）+ `TOOLS`（name→Schema）；新增工具 = 加文件 + 注册，agent / llm / main 零改动 | `01-small-llm-function-call-project/README.md`（目录结构 + 「扩展」小节：3 步加工具） | 工程解耦最好，「工具即插件」思想雏形；是①的工程化封装 |
| ③ 手写 Action 文本协议 | 模型自己吐 `Action: 工具名` / `Action Input: 参数` 文本；`parse_action` 行匹配解析；工具 `run(input: str) -> str` 全字符串进出 | `02-Agent_react/agent/prompt.py` + `loop.py`；`04-LATS` 的候选动作 `Action: tool[input]` 同族 | 零协议依赖、可读可审计、易演示；解析脆弱、参数无类型、复杂入参表达力差 |

面试要点：①②是「模型原生协议驱动」，③是「把协议搬进 prompt 自己解析」——理解这条分水岭，就能解释「为什么有的 Agent 框架必须配特定模型，而手写 ReAct 可以接任何模型」。

### 2.3 Reflexion / Plan-and-Execute / LATS 的循环改动点（各一段）

**Plan-and-Execute：把「一步一循环」改成「两层循环 + 显式状态」**（出处 `02-Plan-and-Execute/Readme.md`）。
外层 `plan_and_execute(task, llm, tools, max_replans=2)`：Planner 一次 LLM 把任务拆成 3–7 个编号步骤（`_parse_steps` 去空行/去 `- ` 前缀），`state = {}` 显式记录；
内层 `for step: execute_step(step, state)` 把「只完成这一步 + 上一步结果」拼成 question，交给复用的 ReAct 循环执行（`react_loop(max_steps=4)`），产出写 `state['step_i']`。
失败分支：某步抛异常 → 拼 `replan_prompt`（Task / Failed step / Error → 要新计划）让 LLM 出新计划整体重来；
全部成功则一次 LLM 汇总 `state` 出 Final Result。
改动点一句话：**单链循环外包了一层「计划→分步→汇总」，多出的是 `state` 字典与失败重规划分支，底层 ReAct 原样复用不改。**

**Reflexion：在循环上装「评估器 + 反思器」两个新角色**（出处 `03-Reﬂexion/Readme.md`；
目录名含连字 ﬂ=U+FB02）。
入口 `reflect_until_success()`，默认 `max_trials=3`。
每个 Trial：① `Action(task, reflections, tools)` 内部仍是 ReAct（calculator/word_count），但 prompt 注入历史反思；
② `Evaluator(task, output)` 先走 `_rule_check` 规则校验，规则判不了才用 LLM 输出 `Success / Score / Feedback`——原则 = **规则优先、LLM 兜底**；
③ 失败则 `Reflector(feedback)` 让 LLM 把失败写成一条改进策略，`trim_reflections` 限制 = 默认 5 条 / 单条 400 字 / 合并相似项；
④ `reflections` 入策略记忆，下一 Trial 的 Action 读入。
仓库演示很有说服力：Trial 1 明明调了 word_count 但 Final Answer 措辞不符规则（规则只检查最终文本，不查工具调用记录）→ 失败；
Trial 2 带反思「必须使用 word_count 并按格式输出」→ 通过。
改动点一句话：**循环多了外部打分者（Evaluator）与跨尝试携带的策略记忆（reflections），并暴露验收粒度陷阱——规则只查最终文本时，工具用了但没写进答案也算错。**

**LATS：把线性单链换成「一棵树 + 价值回传」**（出处 `04-LATS/Readme.md`）。
节点=状态，边=候选动作；
`lats_mcts()` 在预算内循环 MCTS 四步：**Select** 从根沿 UCB 走到叶/未访问子节点；
**Expand** LLM 生成 k 条候选 `Action: tool[input]`（`expand_candidates(state, llm, k=3)`）；
**Simulate** `scorer(state, action)` 估分（启发式或接 LLM）；
**Backpropagate** 回报累加到路径各节点 `visits` / `total_value`。
示例参数：`budget=6`、`branch_k=3`、`max_depth=3`、UCB 的 `C=1.4`；
`visits=0` 时 UCB=∞，未访问节点必先被选；
预算耗尽后沿 visits 最多的子节点走到底，依次执行得 Final State。

UCB 公式（Readme 原文，面试可默写）：
```
UCB(node) = total_value/visits  +  C × √(ln(parent.visits + 1) / visits)
              ↑ 利用项（已知质量）     ↑ 探索项（越少访问越高）
```

仓库运行实例（21+21 + 统计字符数）：根 → C1 calculator[21+21](低分) / C2 word_count[42](最高分) / C3 get_current_time[](最低分)；
C2 因 score 最高被反复光顾、visits 累积最多 → 被选中。
结论：`lats_one_step`（只看一步）与 `lats_mcts`（树搜索）此例找到同一条最优路径，但多步复杂任务中树搜索能找回单步贪心错过的更优路径。

Readme 自带的面试 Q6 答案（可直接引用）：成本 = 多分枝 expand + 多次 score/模拟 + 树迭代预算；
收益 = 更系统探索，适合决策点多、可打分、需先提多假设再验证的任务（规划 puzzle、多方案代码修复）；
工程难点 = 分支爆炸、评估器设计、延迟 → 靠 `max_depth` 剪枝、缓存、启发式 scorer 缓解。
改动点一句话：**循环里「下一步选什么」不再交给贪心模型，而是交给树搜索的价值函数（UCB）；模型退化为候选生成器（Expand）与打分器（Simulate）。**

**Multi-Agent-Crew：水平复制角色 + 共享黑板**（出处 `05-Multi-Agent-Crew/Readme.md`）。
无工具、无并行，纯概念演示（工程可换 CrewAI / AutoGen）。
`run_crew(task, roles, rounds, order)`：thread = 共享黑板，每角色输出 `+=` 追加、全员可见；
rounds = 外循环，order = 内循环角色顺序；
角色隔离 = 每角色只有自己的 system prompt 不同（researcher 输出条目 / writer 输出段落 / reviewer 输出批注）。
迭代改进实例：Round 1 reviewer 提「补全称」，Round 2 writer 即采纳。
工程要点：无状态 LLM 的「记忆」全靠 thread 全量重发，**thread 越长每轮成本越高**——这是所有黑板式多 Agent 的第一成本约束。

**面试怎么说（实现层总收口）**：五范式不是五套代码，是**同一个 ReAct 内核 + 不同位置插入的不同机制**——Plan 插在外层管顺序与重试、Reflexion 插在出口做评估与记忆、LATS 把选择器换成 UCB 树搜索、Crew 水平复制角色共享黑板。
「内核 + 插槽」的讲法最能证明你读过代码。

---

## 3 工程层：避坑 + 生产要点

（全部可溯源到 09-loop 三文或 01-Agent 各 Readme / 代码）

1. **停止条件是 loop 的第一公民，不是可选项**。
     正常停止 = 客观验证通过（单测/规则打分/Evaluator Success）或模型终止信号（Final Answer / 不再调工具）；
     硬顶 = 步数/时间/花费三选一以上。
     仓库参数实证：ReAct `max_steps=6`；
     Plan 单步 `max_steps=4`；
     Reflexion `max_trials=3`；
     LATS `budget=6 / max_depth=3`；
     Abbey Road 硬顶 8 轮。
     金句（`01.context` 文）：**没有验证的 loop，等于无人值守地犯错**。

2. **验证门必须独立（Maker–Checker）**。
     `02.loop-engineering.md`：写代码的与打分的不能是同一个；
     六组件中 Sub-agents 即此意；
     `03` 文三形态从 Solo（自评偏差）升到 Maker–Checker 为此；
     Reflexion 的 Evaluator（规则优先、LLM 兜底）是「验证工程化」的最小实现。

3. **格式纪律决定解析器存活率**。
     prompt 要求每轮只输出一个回合、不得同时给 Final Answer 与 Action；
     `loop.py` 仍防御处理——Action 合法就先执行工具、忽略同条回复里的 Final Answer；
     `parse_action` 只解析第一轮 Thought/Action，遇 `Final Answer:` 即截断。
     生产启示：永远假设 LLM 不守规矩，解析器做最宽容假设、循环做防御分支。

4. **错误处理：自愈 vs 重规划，按错的性质选**。
     `loop.py` 路线 = 把 ERROR 喂回上下文让模型自纠（局部错，适合工具调用失败）；
     `02-Plan-and-Execute` 路线 = 执行器抛异常触发整体重规划（结构性错，适合计划失误）。
     两者并存才是完整容错：局部错自愈、结构性错重来。

5. **工具本身要安全**。
     `calculator.py` 用 `ast` 白名单手写求值器而非 `eval`；
     Agent 工具暴露给模型后就是攻击面，白名单/沙箱/只读是底线。
     更重的沙箱方案（子进程隔离等）仓库内未见，面试可主动补这一层。

6. **成本护栏三件套**（`02` 文 §8 + `03` 文 §8）：进度停滞时的停止判断、硬性花费上限 hard spending limit、最长时长上限。
     经验区间（`03` 文）：单次有用 30 分钟–数小时；
     过夜 4–8 小时；
     很少需要数天长跑；
     **12 小时以上无推进的 loop 不值得保留**。
     LATS 类多候选范式成本更高，budget 与剪枝须前置。

7. **Orchestration Tax（并行天花板是人）**。
     工具可并行 N 个 Agent，但真实吞吐 ≈ min(工具并行, **你的评审带宽**)；
     更危险的不是「失败得很吵」而是「成功得很安静」——几百个 commit 后你跟不上系统在做什么；
     两种结局（A 在理解上跑更快 / B 回避理解只收结果）责任都在人。
     吹「开了几百个 Agent 就当交付」是 `03` 文点名禁止的幻想。

8. **种子 prompt / 规格比单轮更重要**（`02` 文 §7）。
     loop 跑在「由你的规格拼出来的 prompt」上，第一条 prompt 是你看不见的成百上千步的种子；
     模糊的规格、停机条件、测试用例 = 系统大量做错假设，长任务下是灾难级。

9. **复利的是 Skills，不是 Loop 本身**（`02` 文 §9）。
     每轮教训要写回 SKILL.md 类资产，否则每轮归零；
     Loop 负责运转，Skills 负责复利。
     呼应六组件之 Memory/State：「模型会忘，仓库与文件不会」——跨 run 持久化是复合（而非重置）的前提。

10. **日志与审计**。
      01-Agent 系列统一做 LLM request/response JSON 打印；
      `02-Plan-and-Execute/log.txt` 全程留档（Readme 教读者用三类日志标志扫 log：`>>> LLM request` / `<<< LLM response` / `Tool execution`）；
      `03` 文清单里的 Logging：事后能回答「它为什么停」。

11. **场景过滤（别跟风上舰队）**（`03` 文 §9）。
      知识工作/个人任务更适合事件触发 + Solo Loop + 强验证，不必跟风 24/7 无人值守舰队；
      更可能受益的是团队共建产品、可验证可合并的流水线任务；
      金句：别人 10 倍的方式，不等于你的方式。

**面试怎么说**：工程层问题别答「我会设 max_steps」，要答组合拳——停止 = 验证信号 + 硬顶双轨；
验证独立于执行（Maker–Checker）；
错误按性质选择自愈或重规划；
事前有花费/时长护栏、事后有日志可审计停因。
这套组合拳覆盖 90% 的「Agent 怎么防失控」追问。

---

## 4 面试卡（8 问：先自答，再看答案要点与出处）

**Q1：白板手写一个最小 ReAct 循环。**
答案要点：`for step in 1..max_steps`：拼 prompt（Question + history + 工具清单）→ 调 LLM → 解析输出；
合法 Action → 执行工具 → 把 (thought, action, input, observation) 追加进 history → continue；
出现 `Final Answer:` → 截断返回；
非法 Action → 把 ERROR 当 Observation 写回 history；
超步数 → 返回失败串。
history 即「循环内记忆」，每轮全量回放。
出处：`01-Agent/02-Agent_react/agent/loop.py`（55 行）、`prompt.py::build_prompt / parse_action`。

**Q2：Agent 的停止条件怎么定？**
答案要点：双轨——正常停止（客观验证通过 / Final Answer 信号）+ 硬顶（max_steps=6、单步 4、Reflexion 3 trials、LATS budget=6、Abbey Road 8 轮；
再加花费上限与停滞判断）。
原则：Done 尽量写成 metric = result（烤蛋糕 = 叉子插进去不带面糊）；
做不到客观就承认主观停机更弱，并加硬顶兜底。
出处：`09-loop-engineering/02` 与 `03` 文（停机条件 / 护栏 / 「两问」）；
参数实例见 §3 第 1 条。

**Q3：五种 Agent 范式怎么选型？**
答案要点：背因果链 + 场景映射——路径不确定、频繁与环境交互 → ReAct；
任务可分解、要可审计计划书 → Plan-and-Execute；
可验证任务、易犯格式/约束错 → Reflexion；
决策点多、多方案对比、可打分 → LATS；
内容生产/流水线协作 → Multi-Agent。
补演进视角：后三层分别补 ReAct 的短视、教训不复用、路径单一。
出处：`01-Agent/README.md` 五范式对比表与演进关系、`02-Plan-and-Execute/Readme.md` 对比表。

**Q4：Function Calling（原生 tools JSON）与手写 Action 文本协议的区别？**
答案要点：前者由 API/SDK 保证结构化：JSON Schema 注册 → `tool_calls` → `role=tool` 回填；
参数类型安全、天然支持并行、无需解析器；
但要求模型/SDK 支持该协议。
后者把协议搬进 prompt：模型吐 `Action:` / `Action Input:` 文本，`parse_action` 行匹配解析；
任何模型都能跑但脆弱、无类型。
工程上可加注册中心（`TOOL_HANDLERS` + `TOOLS`）解耦新增工具。
出处：`00-llm_function_call/llm_function_call.py` vs `02-Agent_react/agent/prompt.py`；
注册中心见 `01-small-llm-function-call-project/README.md`。

**Q5：为什么要 Harness？上下文膨胀发生在哪？**
答案要点：Context 工程把工具结果不断写回窗口，任务超过约 5–10 分钟上下文就会超出窗口；
「快满了自己总结」会逐轮泄漏细节。
Harness 把任务拆分/运行时/状态放到 context 之外管理，模型窗口只承载当前执行单元；
Loop 再往上把「谁发起下一轮」也外置（调度+状态+验证）。
出处：`09-loop-engineering/01.context-looop-engineering.md`（四层表、Context 局限两条）。

**Q6：Reflexion 与「让模型自己检查一遍」有何不同？**
答案要点：自检往往一次性、不持久、难评测；
Reflexion 把评估与反思显式化——独立 Evaluator（规则优先、LLM 兜底）产出可记录的分数/反馈；
Reflector 把失败写成策略文本存入 reflections 策略记忆；
跨 Trial 复用并裁剪（5 条/400 字/合并相似）。
仓库演示：Trial 1 规则只看最终文本判定失败，Trial 2 带反思即通过。
出处：`01-Agent/03-Reﬂexion/Readme.md`（Q5 对照表、运行示例）。

**Q7：LATS/MCTS 比单次 ReAct 多花什么成本？换来什么？（Readme 原题）**
答案要点：成本 = 多分枝 expand（LLM 每节点生成 k 候选）+ 多次 score/模拟 + 树迭代预算（budget/max_depth）；
收益 = 系统化探索、按节点价值择优，避免贪心单链「一条路走到黑」，适合决策点多、可打分的任务。
工程难点 = 分支爆炸、评估器设计、延迟，靠剪枝/缓存/启发式 scorer 缓解。
UCB = 利用项（已知价值）+ 探索项（越少访问越优先，visits=0 时 UCB=∞）。
出处：`01-Agent/04-LATS/Readme.md`（面试 Q6、UCB 公式与参数）。

**Q8：什么是 Loop Engineering？它和 Cron 什么关系？什么任务不该上 Loop？**
答案要点：定义 = 把自己从「不断 prompt 的人」替换掉，设计会替你发 prompt 的系统；
一个 Loop 只有三件事 Trigger / Action / Stop Condition；
两根柱子 = 客观 Goal + 可执行 Verification。
Cron 定时跑固定脚本；
Loop = Cron + 中间决策体（读状态 → 模型决定 → 执行 → 检查 → 再决定）。
不该上：目标模糊、无法客观验收的探索任务（幻想舰队）；
最适合：可验证、可重复、停机条件清晰的维护类工作。
出处：`09-loop-engineering/02` 文（§3 Cron 对比、§10 适合/不适合表）、`03` 文（三件套、两柱）。

---

## 5 五分钟速查卡（终极压缩）

**一张表背下全部**：

| 想表达 | 一句话锚点 |
|---|---|
| 主线 | 无状态调用 → 回合（工具结果入上下文）→ 多步任务（状态外置 + 验证 + 调度） |
| 四层演进 | Prompt 约束行为 → Context 自主装填(≈5–10min 上限/摘要泄漏) → Harness 外置任务(≠硬塞窗口) → Loop 外置「谁发起下一轮」 |
| ReAct | Thought→Action→Observation 循环，max_steps=6，history 四元组回放，Final Answer 停 |
| Plan-and-Execute | Planner 拆 3–7 步 + state 逐步执行 + 失败重规划(max_replans=2)，单步复用 ReAct(4 轮) |
| Reflexion | Action → Evaluator(规则/LLM) → 失败写 reflections(≤5 条/400 字) → 带教训重试(max_trials=3) |
| LATS | 树搜索 MCTS：Select(UCB, C=1.4)/Expand(LLM×k)/Simulate(scorer)/Backprop；budget 后沿 visits 最多走 |
| Multi-Agent | 角色共享 thread 黑板，rounds×order；无状态 LLM 靠全量重发记忆 |
| 工具协议三变体 | 原生 tools JSON（结构化，绑模型）/ 注册中心（解耦新增）/ 手写 Action 文本（通用但脆） |
| Loop 工程铁律 | 停止 = 验证 + 硬顶；验证独立（做 ≠ 打分）；错误可分自愈或重规划；花费上限 + 日志审计；复利在 Skills |
| 防吹牛三句 | Loop 上限 = Done Check 上限；吞吐上限 = 人的评审带宽（Orchestration Tax）；多数任务 Solo Loop 就够 |

**一段话版（面试开场 30 秒）**：LLM 单次调用是无状态的一问一答；
把它包进 ReAct 式循环——每轮想一步、做一步（调工具）、把观察写回上下文、直到出现 Final Answer 或步数硬顶——就得到最小 Agent；
任务再变长，就在循环外依次叠上显式计划与状态（Plan-and-Execute）、评估与反思记忆（Reflexion）、多路径树搜索（LATS）或多角色黑板（Multi-Agent）。
整套工程的统一命题，是 09-loop 三文那句话：**每一层不取代下一层，而是在上一层留下缺口（空上下文 → 长任务泄漏 → 人必须持续催促）时，把环往外再长一层；Loop 的本质是把「下一轮谁来开启」从人手里工程化出来，靠的是客观 Goal、独立 Verification、硬停与花费护栏，而跨 run 能真正复利的是外置的 Memory/State 与 Skills。**

### 附：面试前回源检查清单（↳深挖六处）

1. `01.context-looop-engineering.md` §3–§6 → 被问「为什么要 harness / 上下文膨胀」时回；
2. `02.loop-engineering.md` §5–§8 → 被问「loop 怎么防烧钱 / 防自嗨」时回；
3. `02-Agent_react/agent/loop.py` + `prompt.py` → 白板写 ReAct 前必回，逐行对照伪代码；
4. `03-Reﬂexion/Readme.md` → 被问「反思如何防冗余 / Evaluator 来源」时回；
5. `04-LATS/Readme.md` → 被问「树搜索成本与工程难点」时回；
6. 其余范式 Readme（02-Plan / 05-Crew）→ 被追问实现细节时回。

> 覆盖范围：09-loop-engineering 三篇、01-Agent/README.md、00-llm_function_call、01/02/03/04/05 五项目 Readme 及 02-Agent_react agent/ 代码。仓库内未见（需自行补充）：更重的工具沙箱方案、多 Agent 框架（CrewAI/AutoGen）的实际接入代码。



