# Agent 面试 5 日冲刺 v2 · 六层栈版

> 目标：面试前用 5 天把本仓库从"作者的线性教学序"翻转为"**六层栈 + 一条消息的一生**"的面试冲刺序，每天 8-9h。
>
> **v2 改版说明（2026-09-18）**：主轴从"一条消息的一生"**升级为"六层栈（L1→L6）为骨架、一条消息的一生为纵轴"**。
> 起因：参考源《开源 AI Agent 从底层逻辑到落地》（B站 AI_Julie，BV1wLYy62EnS）给出了**六层栈**这套
> "最后都要落到同样层数"的落地框架，且明说"**面试时把每一层讲清楚，面试官会觉得你知识面广、架构强**"。
>
> **参考源（仓库外，只读）**：`E:\AI_resource\personal-knowledge\archives\bilibili\AI_Julie\开源AI-Agent从底层逻辑到落地_y62EnS\extracted.md`
> （1353 行，含六层栈总表、逐层选型、失败归因链、面试怎么讲；核心内容已摘录进本文件第 1 节，**不依赖外部路径也能用**）
>
> **MDA 类比（第一原则）**：面试那天 = **A**（能白板画六层栈 + 答系统设计 + 讲验证过的项目）；跑通的 demo 与亲手填的对照表 = **D**；六层的内核机制 = **M**（按需深挖，不线性刷）。
>
> **基线**：D1 = 2026-09-18（今天）→ D5 = 2026-09-22；面试在 D6 或更后；每天 8h+ 封顶 9h；动手基线 = 能读懂代码 → 每日 45-60min 写码渐进挑战。

---

## 0. 为什么把主轴换成「六层栈」

**旧主轴的短板**：`一条消息的一生` 讲的是**运行时内部**（循环→记忆→RAG→协同→评测），它回答"Agent 怎么运转"，
但回答不了面试官更常问的另一半——"**这套系统要落地，你得挨个定哪些事？**"

**六层栈补的正是这一半**：

| 对比 | 三段论（LLM + Memory + Tools） | **六层栈** |
|---|---|---|
| 回答的问题 | Agent **由什么组成** | 要落地我**得挨个定哪些事** |
| 覆盖范围 | 能力构成 | 一个可交付系统的**全部工程决策** |
| 面试效果 | 谁都知道 | "每层讲清楚 → 知识面 + 架构能力"（视频 28:05 原话） |

**多出来的三层是关键**：
- **L1 推理**不是"选个模型"，而是"开放权重还是闭源 API / 本地还是托管 / 本地引擎还是并发引擎 / 路由要不要上 / 不同任务用不同尺寸的模型"——**成本与智商的分层配置**；
- **L5 观测**是"怎么知道它坏了、坏在哪"——视频给了可执行的**8 步失败归因链**；
- **L6 界面**是"出错怎么优雅兜底、人怎么用它"。

**另一个必须记住的纠正（视频 26:13 她当场自纠）**：**LangGraph 与 Hermes 是同一层（L4）的两条路，默认二选一，
不要在一个进程里叠两套循环**——两者都已内置 harness（循环/状态/工具/停机/人审）。
把它读成"上下两层"会导致 **harness 重复建设**，这是实打实的工程错误，也是面试可引用的现成案例。
（详见 `运行时选型-LangGraph-vs-Hermes.md`）

---

## 1. 六层栈总图（本计划骨架）

```
用户 / 客户
   │
   ▼
┌────────────────────────────────────────────────────────────────┐
│ L6 界面      Open WebUI / AnythingLLM（成品）                    │  原则：界面是栈顶，
│              或自写：Chainlit / Streamlit / Gradio / React 系     │  不替系统的智力；越简单越好
├────────────────────────────────────────────────────────────────┤
│ L5 观测      Trace：Langfuse / Arize Phoenix / Braintrust        │  "没有 traces 你只是在猜"；
│              Eval：Ragas / Promptfoo / DeepEval                  │  先建 30 条真实用例；
│              护栏：NeMo Guardrails / Guardrails AI（≠安全策略）   │  失败归因链 8 步
├────────────────────────────────────────────────────────────────┤
│ L4 运行时    LangGraph（图编排库）  ⊻  Hermes（成品 harness）     │  ★同层二选一，不叠加★
│              （+ 本仓库的 waku / pi / DSH 三个同类实证）           │  它们都已含：循环/状态/工具/停机/人审
├────────────────────────────────────────────────────────────────┤
│ L3 动作      MCP（发现并调用能力）+ OpenAPI/REST + OpenTelemetry  │  工具会改世界 → 最小权限 /
│              （另见 A2A agent 间、AG-UI 接前端）；工具=Firecrawl   │  沙箱 / 人审 / 检索内容不可信
├────────────────────────────────────────────────────────────────┤
│ L2 上下文    知识 = RAG（十步管线；向量库只是第 6 步）            │  ⚠️ 向量库 ≠ RAG；
│              记忆 = Mem0（抽取事实→更新→按需召回）                │  先查解析，再调检索
├────────────────────────────────────────────────────────────────┤
│ L1 推理      开放权重（HF 找 / Artificial Analysis 看榜）         │  应用调稳定的内部接口，
│              引擎：Ollama·llama.cpp（本地）｜vLLM·SGLang（并发）  │  换模型只改配置
│              路由：LiteLLM（路由/重试/预算/回退/可观测钩子）       │  按任务分层用模型 + 兜底
└────────────────────────────────────────────────────────────────┘
```

### 1.1 每层 = 一个面试答案（本仓库实证映射）

| 层 | 笔记给的候选 | **本仓库实证（用它证明"我见过真的"）** | 面试一句话 |
|:--:|---|---|---|
| **L1** | Ollama / llama.cpp / vLLM / SGLang / LiteLLM | `05-model-route`（11 个模块：熔断重试·缓存·两级缓存·路由回退·计费对账·语义缓存·治理）；`07-llm_from_scrach`（KV cache / MoE / GRPO） | "模型选型是**成本与智商的分层配置**：固定 task 用小模型兜底，复杂推理走大模型，缺一层路由代码就会散落各处" |
| **L2** | Chroma / Qdrant / pgvector + LlamaIndex；Mem0 | `02-RAG` 全量；`03-memory` 四本；`08-hermes-agent\01-memory`+`02-memory.md`+`07-mem-provider`；`12-hermes-agent-small\waku\memory`（四层）；`13-pi-agent\04/05`；`99-My idea\AI Agent 学习指南\01.longterm memory.md`（mem0 详解）；已有 `Agent记忆深度解析` + `RAG评估深度解析` | "**知识 ≠ 记忆**：知识是可检索的外部资料，记忆是系统决定保留什么；**向量库不是 RAG**，它只是十步管线的第 6 步" |
| **L3** | MCP + OpenAPI + OTel（+A2A/AG-UI）；Firecrawl | `01-Agent`（工具协议三变体）；`06-harnes\learn-claude-code\s02/s03/s19`；`08-hermes-agent\hermes-study\tools\registry.py`（801 行）+ `08-hermes-agent\05-env\hermes_src\tools\environments\`（docker/local/ssh/daytona/modal 沙箱阶梯）；`12-hermes-agent-small\waku\tools`+`mcp_client.py`；`05-model-route\08`（schema/whitelist/executor） | "MCP 底层还是 tool call，很多 MCP server 只是坐在 REST 前面的适配器；**危险在于工具有副作用**→只读当不可信文本、改外部状态先人审、跑代码进沙箱" |
| **L4** | LangGraph **或** Hermes（二选一） | `09-loop-engineering` 三文；`06-harnes\learn-claude-code` s01-s20；`11-langgraph` 三项目；`08-hermes-agent` 九模块；`12-hermes-agent-small`(waku)；`13-pi-agent`；`14-deepseek-harness`；`01-Agent` 五范式 | "两者都已自带 harness，是**同层替代**；选型先确认互斥关系，避免两套循环，然后按'业务工作流 vs 终端里干活'选" |
| **L5** | Langfuse / Phoenix / Braintrust；Ragas / Promptfoo / DeepEval；NeMo / Guardrails AI | `08-hermes-agent\03-eval`（invariants + trace RCA）；`12-hermes-agent-small\waku\ops`+`evals`（30 个确定性测试 + judge + release_gate + dashboard）；`02-RAG\04_RAG_Evaluation`；`99-My idea\Agent eval`；`10-CICD`；已有 `RAG评估深度解析` | "失败归因链：RAG→解析→记忆→mem0→工具→loop→模型→微调；**护栏库 ≠ 安全策略**，真正的控制层是权限/沙箱/校验/密钥隔离/审计/人审" |
| **L6** | Open WebUI / AnythingLLM | `11-langgraph\02-Agentic-Chatbot-using-LangGraph\frontend`（chat 207 行 + **hitl.py 183 行**）+ `11-langgraph\03-project-TripMate-AI-A-Multi-Agent-Travel-Planner-with-LangGraph\frontend\static\script.js`；`12-hermes-agent-small\waku\gateway`（telegram / voice / cli） | "界面是栈顶，**不应替系统的智力**；越简单越好，模型/工具/记忆/检索放在干净接口后面才能换前端" |

---

## 2. 纵轴：一条用户消息的一生（挂靠层号）

```
用户消息
   │
   ▼
[L6 界面] 流式输出 / 人审按钮 ────────────── D5
   │
   ▼
[入口 / 会话恢复]  thread_id / session ────── L4 ── D2(checkpoint) / D4
   │
   ▼
[L4 System Prompt 组装]  静态段 + 动态段（记忆/技能/环境快照）── D1(s10) / D2(记忆注入)
   │
   ▼
┌──────────────────────── L4 主循环（ReAct）────────────────────────┐
│  观察 → 思考 → 行动                                               │
│    │                                                             │
│    ▼                                                             │
│  [L1 LLM 调用] 路由 / 缓存 / 回退 / 计费 ────────── D3            │
│    │                                                             │
│    ├─ 要调工具? ──→ [L3 工具注册表] ──→ 权限判定 ──→ 执行          │
│    │                 ├─ MCP / OpenAPI / 内置（副作用决策树）D3     │
│    │                 ├─ 沙箱 / 人审（HITL）────────── D3/D4       │
│    │                 └─ tool_result 回填（上下文膨胀的源头）       │
│    └─ 不要? ──→ [生成最终答案]                                    │
│                                                                  │
│  上下文膨胀 → 压缩（s08 四层）/ 记忆 / 子 Agent 隔离 ── D1/D2     │
└──────────────────────────────────────────────────────────────────┘
   │
   ▼
[L2 上下文注入]  RAG 检索 / 记忆召回 ────────────────── D2
   │
   ▼
[L5 状态写入 + 观测]  轨迹落盘 / 指标 / 门禁 ────────── D5
   │
   ▼
[L3 协同层] subagent / teams / 多智能体编排 ────────── D4
```

---

## 3. 五日总览（层 × 天），日期已重锚

> **日程重锚（2026-09-18）**：原计划 D1=9/9（9/8 因身体不适顺延）实际未启动；
> 今天 **2026-09-18（周五）** 为 D1，D5=9/22（周二）。dtodo 已同步。

| 天 | 日期 | 覆盖层 | A（当天能答的面试锚） | 主产出 | 前置专题 |
|:--:|:--:|:--:|---|---|---|
| **D1** | 09-18 五 | **总纲 + L4a 内核** | 六层栈逐层讲 + "一条消息的一生" + 手写 ReAct | 六层栈总纲表（先填 L4 行）+ 生命周期总图 v1 + 五范式对比表 | `00-我的深度整合专题\循环工程深度解析\Loop_Engineering_Deep_Dive.md` ✅ 567 行|
| **D2** | 09-19 六 | **L2 上下文** | "凭什么决定记什么/忘什么" + "向量库不是 RAG" | 记忆对照表（含 mem0 列）+ RAG 十步管线卡 + RAG/记忆/长上下文边界卡 | `提纯精读\P2-记忆实现对照提纯.md` ✅ 572 行 + 已有两份专题 |
| **D3** | 09-20 日 | **L1 推理 + L3 动作** | 模型怎么选/怎么跑/怎么路由 + 工具协议与权限 | L1 选型卡 + 工具协议对照表 + 权限决策树（+ 写码挑战③） | `推理与路由深度解析\Model_Route_Deep_Dive.md` ✅ 623 行|
| **D4** | 09-21 一 | **L4b 选型 + 协同** | "LangGraph 和 Hermes 是同层二选一" + 多智能体 vs 单 agent | 框架选型矩阵终版 + runtime 五方对照表（LangGraph/Hermes/waku/pi/DSH） | `运行时选型-LangGraph-vs-Hermes.md` ✅ 312 行 + `运行时选型深度解析\Runtime_Five_Way_Deep_Dive.md` ✅ 616 行 |
| **D5** | 09-22 二 | **L5 观测 + L6 界面 + 收口** | agent 怎么评测/怎么进 CI + 六层栈总演练 | **面试总纲 v1** + 模拟面试记录 + CICD 背题卡 | `观测与评测深度解析\Observability_Eval_Deep_Dive.md` ✅ 546 行|

**每日文件**：
`day1-loop-harness.md` ｜ `day2-context.md` ｜ `day3-inference-tools.md` ｜ `day4-runtime-multiagent.md` ｜ `day5-observability-closeout.md`
（v1 的四份旧 day 文件已合并进上表并删除，避免"文件真实性"歧义）

---

## 4. 全仓覆盖矩阵（每个目录去哪天，按层组织）

| 模块 | 覆盖层 | 处理日 | 深度 | 说明 |
|---|:--:|:--:|---|---|
| `00-大纲` | 总纲 | D1 | 浏览 10min | 作者序仅作对照（`00-大纲\Agent教学大纲.md` 44 行，**已核验存在**）|
| `00-我的深度整合专题` | 全程 | 全程 | 复用+产出 | 记忆专题→D2；RAG 评估专题→D2/D5；本目录即产出 |
| `01-Agent` | L4a/L3 | D1 + D3 | ReAct 精读 + 五范式 | 工具协议三变体的源头；`03-Reﬂexion` 目录名含连字 ﬂ（U+FB02）|
| `02-RAG` | L2 | D2 | 读+跑（`--mock`/离线） | simple→basic→high→Agentic RAG→评测 |
| `03-memory` | L2 | D2 | 跑 2 本（离线） | 四本：windowed / long_term / summary / **three_factor**（纯 stdlib）|
| `04-multiagent` | L3/L4b | D4 | 讲义精读 + 只读 | `multi-agent-arch` 01.1-01.7 模式 + 09 agent ops + 11 个 py demo |
| `05-model-route` | L1(+L3/L5) | D3 + D5 | 跑/读 11 模块 | D3 读 01-06/10；**07 trace / 08 guard / 09 deploy / 11 governance → D5** |
| `06-harnes` | L4a | D1(+D2/D4) | s01-03·s10 精读 | s08/s09→D2；s06/s15-20→D4 选读；`learn-harness-engineering` 讲义备查 |
| `07-llm_from_scrach` | L1 | D3 | 概念卡 2h | part_1 注意力 + part_3 kv_cache + part_5 MoE + part_9 GRPO 中文详解；其余跳过 |
| `08-hermes-agent` | L2/L3/L4/L5 | D2+D4+D5 | 读（源码为 Python，**可读不可跑**） | 9 个模块；`hermes_src` 是真实源码摘录 |
| `09-loop-engineering` | L4a | D1 | 三文全量（已蒸馏） | `01.context-looop-engineering.md`（**文件名拼写 looop**）/ 02 / 03 |
| `10-CICD` | L5 | D5 | 4 组背题 | 01-basic / 02-pytest / 03-gitlab-ci / 08-review，其余跳过 |
| `11-langgraph` | L4b(+L2/L6) | D2+D4+D5 | chatbot 精读+试跑 | 最贴本机环境：DeepSeek key + BGE 本地 + SQLite threads |
| `12-hermes-agent-small`(waku) | L2/L4/L5/L6 | D2+D4+D5 | 读（有余力 uv 跑） | 最完整的小型 harness 实证：memory 四层 + loop + ops + evals + gateway |
| `13-pi-agent` | L2/L4 | D2+D4 | 读 60min | 会话树 / compaction / HITL / 事件模型 |
| `14-deepseek-harness` | L4 | D4+D5 | 30min | tool vs skill / code vs config 话术 |
| `15-Edge-Agent` | — | **不纳入** | — | 端侧 Agent，与主线弱相关；D6+ 有余力再看 |
| `99-My idea` | 全程 | 全程 | 早晚背诵 | `99-My idea\memory\01.md`＋`99-My idea\memory\02.md` 问答稿；`99-My idea\AI Agent 学习指南\01.longterm memory.md`（mem0 详解）→ D2；`99-My idea\Agent eval\01-eval.md` → D5 |

---

## 5. 每日文件核验机制（v2 新增，回应"文件真实性"要求）

**规则**：每天开工前，先跑核验脚本；每张 day 卡里列出的每个路径，都必须是**核验过的真实路径**（含准确的文件名与行数）。

```powershell
# 在仓库根目录执行：扫描冲刺目录所有 md，把反引号里的仓库路径逐个验存在
python "00-我的深度整合专题\Agent面试5日冲刺\核验脚本.py"
```

- 输出：每个路径 ✅/❌ + 行数 + 缺失汇总；**有缺失则退出码 1**。
- 例外白名单写在脚本里（仓库外路径如 `~/.dsh/...`、参考源 `personal-knowledge\...`、已确认不存在的研究对象）。

### 5.1 本次全量勘察结论（2026-09-18，逐文件实测）

| 结论 | 证据 |
|---|---|
| ✅ 仓库共 17 个顶层目录、约 4548 个文件；`06-harnes` 最大（1505 个 md，含 8 种语言翻译，**只用中文/英文主体，跳过 docs\ar,de,en,es… 译本**） | 全量 walk |
| ✅ **`00-大纲\Agent教学大纲.md` 确实存在**（44 行，1458 字节） | `Test-Path` = True；已读全文 |
| ✅ 它列出的 `04-multiagent\multi-agent-arch\` 10 个 notebook **也全部存在**（01.1-01.7 模式、01 demo、02 hierarchical、09 agent ops…） | 目录实测 |
| ✅ `03-memory` = 4 个 notebook（不止 `03-memory\requirements.txt`）| 目录实测 |
| ✅ `02-RAG\06 Agentic RAG\ppt\agentic-rag-deck.html` 与 `...\lesson2_rag_metrics\diagnostic_report.html` 都在 | 实测 |
| ⚠️ **`08-hermes-agent\02-run-agent\hermes_src\agent\conversation_loop.py` 确实存在，但在 `08-hermes-agent\02-run-agent\hermes_src\agent\`（5355 行）**；顶层 `hermes-study\` 是被剪枝的副本，**其中没有该文件**（v1 卡片写"本机缺此文件"不准确，已修正） | 两处分别实测 |
| ⚠️ 文件名坑 3 个：`08-hermes-agent\03-hermes Agent  学习大纲.md`（Agent 后有**两个空格**）；`01.context-looop-engineering.md`（**looop** 三个 o）；`01-Agent\03-Reﬂexion`（连字 **ﬂ**） | 实测 |
| ❌ 明确跑不了（只读概念）：Neo4j/GraphRAG（Docker 未启动）、hermes `hermes-study` 剪枝副本（不可 import）、任何需要 GPU 的推理 | 环境实测 |

---

## 6. 贯穿线清单（六层版，面试"看见共性"的弹药）

| 贯穿线 | 仓库出处 | 处理 |
|---|---|---|
| 循环 / 谁拥有 loop | `01-Agent` 五范式 → `06-harnes` s01 → `08-hermes-agent` conversation_loop → `09-loop-engineering` → `12-hermes-agent-small\waku\loop`（~113 行）→ `11-langgraph` | **D1 建立，D4 收口** |
| 上下文组装与膨胀 | `06-harnes` s10 组装 / s08 四层压缩 → hermes 冻结快照 + prefetch → 记忆/RAG 注入 | D1 起，D2 加深 |
| 工具协议三变体 | 原生 tools JSON（`01-Agent\00`）/ 注册中心（`06 s02`、`08 registry`、`12 registry`）/ 手写 Action 文本协议（`01-Agent\02-Agent_react`） → MCP | **D3 收口** |
| 记忆分层与淘汰 | `03-memory` 四本 / `06 s09` / hermes 四层+provider / waku 四层+gate → `13-pi` 会话树 → LangGraph checkpoint → mem0 | D2 |
| 评测闭环与门禁 | RAG 四指标四象限 / hermes 03-eval / waku evals+release_gate / `10-CICD` | D2 起 + D5 收口 |
| 路由与成本 | `05-model-route` / Adaptive RAG / 语义缓存 / 兜底降级 | **D3 主打**（07/08/09/11 → D5）|
| 权限与安全 | `06 s03` 四决策 / `05-model-route\08` guard / hermes `05-env` 沙箱阶梯 / 插件内存写的三道闸 | D1 挂，D3 深挖 |

---

## 7. 打卡协议与学习科学机制

**打卡协议（技能 `daily-sprint-coach`）**：定位当天 → 晨间复盘昨日 3 问（**主动回忆，AI 不代答**）→ 今日卡 →
逐时间盒引导 → 写码挑战（**AI 只提示不代写**）→ 晚间收尾（3 答入 day 文件 + 情绪 feedback + dtodo 打卡 + 写 memory）。
**铁律**：不代写你该写的代码/答案/产出；每天 ≤9h；每 90min 休息；睡前 30min 不塞新知识。

**学习科学**：
1. **主动回忆**：每天开场 30min 闭卷复述昨日（不是重读）。
2. **交错练习**：相邻两天互为"同一内核的不同抽象层"（D1 循环 ↔ D4 运行时；D2 记忆 ↔ D3 路由成本；层号在 day 卡里显式标出）。
3. **生成式产出**：每天亲手写图/表/卡（六层总纲表、对照表、决策树、矩阵）。
4. **间隔重复**：D1 卡片在 D3/D5 晨间复测；`99-My idea\memory\01.md`＋`99-My idea\memory\02.md` 问答稿早晚各 10min。
5. **写码渐进**：D1 抄写 → D2 填空重写 → D3 伪代码 → D4 真改小图 → D5 白板口述。
6. **时间盒与休息**：90min 一盒；每天 ≤9h；睡前 30min 不学新知识。

---

## 8. 环境约束与诚实标注

- ❌ Docker 未启动 → GraphRAG(Neo4j)、沙箱类只读概念不跑。
- ⚠️ hermes 完整仓库不在本机 → 只读 `hermes_src` 摘录与教学版，不 import、不打断点。
- ✅ 离线/低成本可跑：`03-memory\04_three_factor_scoring.ipynb`（纯 stdlib）、`03-memory\02_long_term_memory.ipynb`（mock 向量）、
  `02-RAG\06 Agentic RAG`（`--mock`）、`11-langgraph\02-Agentic-Chatbot-using-LangGraph\` chatbot（BGE 本地 + DeepSeek key）、`12-hermes-agent-small\`（uv + 一把 key）。
- ✅ **纯 CPU 无 GPU 的现实**：够走通全链路与调试，不够做并发服务（与"本地跑通 + 生产用托管 API / 小模型兜底"一致）。
- ✅ **诚实标注**：① mem0 列 = 作者详解实证（`99-My idea\AI Agent 学习指南\01.longterm memory.md` 965 行），**非源码级**；
  ② 六层栈的选型清单来自 UP主配套笔记（其原文件 `02.opensource_AI.md` 未上传，本地只有截图还原稿）；
  ③ 视频口述对 LangGraph 有情绪化否定，**笔记侧中立**——面试用笔记的对比表，口述批评只作反面观点。

---

## 9. 决策记录

| # | 决策 | 结论 |
|:--:|---|---|
| 1 | 产物落点 | `00-我的深度整合专题\Agent面试5日冲刺\`，每日产出入 day 文件 |
| 2 | 两篇 P0 新专题 | Agentic RAG 做压缩版；Multi-Agent 用选型矩阵替代 |
| 3 | 打卡闭环 | AI 每日早晨发今日卡，晚间回 3 答，产出入文件 |
| 4 | 插件能力进冲刺（09-07） | dtodo 固化日程；技能 `daily-sprint-coach`；每日情绪反馈；D2 对照表加 `dsh-memory-evolve` 生产实证列 |
| 5 | 顺延与 mem0 调优（09-08） | 全部顺延；mem0 列升级为"作者详解实证" |
| 6 | **主轴换六层栈（09-18）** | 主轴 = 六层栈 L1-L6；D1 加"六层总纲"；L4 明确**同层二选一**；产出加《六层栈总纲表》 |
| 7 | **日期重锚（09-18）** | D1=9/18 … D5=9/22；day 文件按层重命名为 `dayN-<层>-<主题>.md`，旧 4 份合并删除 |
| 8 | **多文件模块一律先做专题（09-18）** | 用户要求：凡"一个文件夹下多个子文件"的模块，先蒸馏成专题（仿现有 Deep_Dive 格式 + 📍溯源节），再精读；不再直接散读源文件 |

---

## 10. D6+ 缓冲期（面试前只做三件事）

1. 简历项目叙事打磨（只用 5 天里**真正跑通**的 2-3 个 demo）。
2. 二次模拟面试（换题自问自答，重点练"六层栈逐层答"）。
3. 按《面试总纲 v1》薄弱点回炉，不学新知识。
