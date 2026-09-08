# P1b Harness：一次会话的生命周期（提纯版）

> **用途**：Agent 面试 5 日冲刺 · D1 精读。提纯自 `06-harnes/learn-claude-code` 的 s01–s20 二十讲（中文 README）+ `01-simple_harnes_demo` + `02-rag-harness-demo` 两个最小 demo。
> **阅读法（25–40 分钟一遍）**：① §1 先看"生命周期总图"，把 20 讲挂到一条线上，建立骨架；② §2 精读 9 个最关键机制的**实现**（面试问机制细节）；③ §3 记工程层的取舍与避坑（面试问"踩过什么坑"）；④ §4 用 12 个面试问题自测（遮住要点先自己答）；⑤ §5 考前 5 分钟只扫速查表。
> **事实基准**：技术事实一律以各章 `README.md`（中文版）为准；`code.py` 未细读；凡拿不准处标注【存疑】；各章"深入 CC 源码"附录是对真实 Claude Code 源码的核查结论，与教学简化分开引用。`ragent/` 与 `learn-harness-engineering` 未读——课程太重，冲刺跳过。

**一句话主线**：这 20 讲不是 20 个孤立技巧，而是同一条流水线——**"一条用户消息进入 Agent 会话后，如何被处理、工具如何被调用、上下文如何被管理、任务如何被扩展，直到会话停止"**——每讲是流水线上的一道工序，s20 把它们装回同一个循环。

---

### 📍 本页定位与蒸馏溯源（必读，先回答"我在哪、从哪来、为什么这样提纯"）

- **在整体计划中的位置**：5 日冲刺 **D1「循环与 Harness」** 的主阅读之一（另一篇 `P1a-循环与五范式提纯.md` 讲循环内核与推理范式）。主轴位置 = "一条用户消息的一生"第一层：**循环内核 + Harness 骨架**。D1 读法：先 P1a 建立"循环是什么"，再读本页建立"循环的工程外壳"，最后动笔画"生命周期总图 v1"。
- **被蒸馏文档（共 24 个）**：`06-harnes\learn-claude-code\README-zh.md`（总入口）+ **s01-s20 二十讲的 `README.md`（中文版）**（每个源文件的"一句话主题 / 生命周期挂点 / 深挖建议"见下方 §0 源文件清单表，一行一条）+ `01-simple_harnes_demo`、`02-rag-harness-demo` 的 `README.md`/`CLAUDE.md`（两行，见 §0）。
- **蒸馏理由与方法（约 100 字）**：作者按"每讲只加一个机制"的顺序教学（s01 最小循环 → s20 总装），单篇通读只见树木；但每讲的 README 其实都在描述**同一条流水线的某道工序**。因此蒸馏 = 先通读全部 24 个文档，逐篇抽出"机制 + 生命周期挂点"，再按"一条消息的一生"把 20 个挂点重新排序重组为一张总图；同时把"教学机制"与"真实 Claude Code 生产事实"分列，避免面试引用失真。知其然（每讲讲什么），也知其所以然（各站流水线什么位置、harness 为何这样长出来）。

---

## 0 源文件清单（s01–s20 一览）

> 列：主题一句话 / 挂靠的生命周期节点 / 深挖建议。★越多越值得回读原 README 附录。

| 章节 | 主题一句话 | 生命周期节点 | 深挖 |
|---|---|---|---|
| s01 agent_loop | 一个 `while True` + bash 就是最小 agent；模型说用工具就继续，不用就停 | **主循环本体（全生命周期的心脏）** | ★★★ |
| s02 tool_use | 加工具 = 工具定义（schema）+ handler 两行，循环不动，查表分发 | 工具注册表与分发 | ★★★ |
| s03 permission | 执行前先过三道闸门：硬拒绝→规则匹配→问用户 | 工具执行前的权限门 | ★★★ |
| s04 hooks | 扩展逻辑挂在 4 个事件点上，不写进循环；循环只调 trigger_hooks | 横切：输入/执行前/执行后/停止 | ★★★ |
| s05 todo_write | 计划工具不给执行能力，只给"先想后做"；3 轮不更新就 nag | 会话内轻量规划 | ★ |
| s06 subagent | 大任务派独立子 Agent：全新 messages[]，只回传结论 | 委派/上下文隔离 | ★★★ |
| s07 skill_loading | 知识两级加载：目录常驻 SYSTEM，内容用到才 load_skill | system prompt 组装（按需知识） | ★★ |
| s08 context_compact | 上下文总会满：四层压缩（大结果落盘/裁消息/占位/LLM 摘要） | 上下文管理 | ★★★ |
| s09 memory | 压缩会丢细节：.memory/ 文件+索引+按需注入+提取+整理，跨会话 | 长期记忆 | ★★★ |
| s10 system_prompt | prompt 是运行时按真实状态分 section 拼出来的，不是写死的 | system prompt 组装（入口装配） | ★★★ |
| s11 error_recovery | 输出截断升 token、上下文超限 reactive compact、429/529 退避换模型 | 主循环韧性 | ★★★ |
| s12 task_system | 任务=磁盘 JSON+blockedBy 依赖图+claim/complete，跨会话可恢复 | 长目标持久化 | ★★★ |
| s13 background_tasks | 慢命令丢后台线程，占位结果先回，完成以 task_notification 注入 | 异步扩展一轮会话 | ★★ |
| s14 cron_scheduler | 调度线程到点把任务入队，Agent 空闲时自动拉起一轮 | 定时触发新一轮 | ★★ |
| s15 agent_teams | Lead+队友线程，文件收件箱（jsonl）异步通信 | 多 Agent 协作 | ★★★ |
| s16 team_protocols | 队友间用 request_id 关联的请求-响应协议（关机握手/计划审批） | 团队协议层 | ★ |
| s17 autonomous_agents | 队友 WORK→IDLE 轮询看板→SHUTDOWN，自己认领任务不靠分配 | 自治扩展 | ★★ |
| s18 worktree_isolation | 每任务一个 git worktree 目录+分支，改文件互不覆盖 | 并行执行的目录隔离 | ★★ |
| s19 mcp_plugin | MCP 标准协议：连接 server、发现工具、mcp__server__tool 进工具池 | 外部能力接入 | ★★★ |
| s20 comprehensive | 全部机制按固定位置挂回同一个 while True（27 个内置工具） | 收尾/总装 | ★★★ |

两个 demo（最小"包一层"形态的 harness，与 sXX 机制互相印证，面试可当例子讲）：
| 目录 | 一句话 | 与课程对应 |
|---|---|---|
| 01-simple_harnes_demo | CLAUDE.md（规则+DoD）+ skills(/plan /implement /validate) + Stop 质量门 hook | "把 Agent 用规则和工作流包起来"，即 s04 hooks + s05 计划 + s20 的骨架版 |
| 02-rag-harness-demo | RAG 全栈教学 harness：五阶段管道 + PostToolUse lint + Stop 质量门（阻塞式） | 工程化 RAG 项目同样吃 harness：质量门靠 hook 不靠提示词（对应 s04） |

### 0.1 二十讲的内在顺序 = harness 能力的六个阶段（源自 README 学习路径图）

> 记这个六段式，就能回答"harness 是怎么一步步长出来的"：每一讲只在上一讲上加**一个机制**，其余循环不动。

| 阶段 | 涵盖章节 | 能力增量（一句格言） | 面试定位 |
|---|---|---|---|
| ① 让 Agent 能动手 | s01–s04 | 一个循环+bash → 加工具只加 handler → 执行前先划权限边界 → 扩展挂 hooks 不写进循环 | 最小 harness 四件套 |
| ② 能做复杂任务 | s05–s08 | 先列计划再动手 → 大任务拆子 agent 保干净上下文 → 知识用到才加载 → 上下文满了有四层压缩 | 单 Agent 长任务 |
| ③ 能记住与恢复 | s09–s11 | 压缩会丢细节所以有记忆三子系统 → prompt 运行时组装 → 错误不是终点是重试起点 | 状态与韧性 |
| ④ 能长期运行 | s12–s14 | 大目标拆成带依赖的磁盘任务图 → 慢操作丢后台 → 定时触发不需要人推 | 从"会话"到"系统" |
| ⑤ 能多 Agent 协作 | s15–s18 | 一个搞不定组队（收件箱）→ 队友间有请求-响应约定 → 自己看板自己认领 → 各干各的 worktree | 团队与隔离 |
| ⑥ 接外部能力并合体 | s19–s20 | 能力不够插 MCP → 机制很多，循环一个 | 生态与总装 |

### 0.2 版本与范围说明（防读错，面试也可引用）

- **新旧两套章节号**：根目录 s01–s20 是新主线（本提纯基于它）；`docs/`、`agents/`、`web/` 仍是旧 12 章，新旧编号不对应（旧 s03≈新 s05 等），引用时别混。
- **README 明示的教学省略项**（= 生产 harness 与教学版的差距清单，被问"生产还差什么"时可用）：完整事件/Hook 总线（SessionStart/End、ConfigChange 等 27 事件之外更全的）与基于规则的权限治理/信任流程；会话生命周期控制（resume/fork）；更完整的 worktree 生命周期；MCP 运行时细节（transport/OAuth/资源订阅/轮询）；团队 JSONL 邮箱协议是**教学实现**，不是对生产内部实现的声明。
- **本提纯的事实边界**：只精读各章 `README.md`（zh），`code.py` 未细读；凡教学版与 CC 源码不一致处，本文按"教学机制 / 生产事实"分开标注。

---

## 1 概念层：harness 全景

### 1.1 两个统一类比

**驾驶舱类比（分工）**：模型 = 驾驶员（感知、推理、决策来自训练，不是来自外部代码）；harness = 载具（方向盘、仪表盘、导航、油门刹车、黑匣子、安全带）。"模型做决策，harness 执行；模型做推理，harness 提供上下文。**模型是驾驶者，harness 是载具**。Agency（能感知-推理-行动）是学出来的，不是编出来的——你不可能用 if-else 流程图堆出 agent，那是"提示词水管工"的幻觉（GOFAI 借 LLM 还魂）。

**生产线/流水线类比（流程）**：一条用户消息 = 进厂的原料，依次过：**进料质检**（UserPromptSubmit hook）→ **料仓预清洁**（上下文压缩，能腾就腾）→ **装配工艺卡**（system prompt 按状态组装：身份/工具/工作区/技能目录/记忆索引/MCP 状态）→ **核心机床**（LLM 主循环）→ **工序许可**（PreToolUse hooks + 权限闸门）→ **各工位**（工具执行：内置/MCP/后台）→ **出料检验**（PostToolUse hooks）→ **回流**（tool_result 拼回 messages 再上机床）→ 成品（模型不再调工具，Stop hooks 收尾）。旁路工位随时可以把**新的原料**塞进产线：定时器（cron）、后台任务完成通知、队友收件箱——它们都是"新一轮输入"的来源。

### 1.2 生命周期总图（把 20 讲挂到一条线上）

```text
【一次 Agent 会话的生命周期】  s01=循环; 其余 = 挂在循环上的 harness 机制（s20 总装）

 触发新一轮的来源（都是"输入"）
   ├─ 用户输入 ────────────────┐
   ├─ cron 定时到点 (s14) ──────┤
   ├─ 后台任务完成通知 (s13) ───┼─► UserPromptSubmit hooks (s04，可注入/拦截)
   └─ 队友收件箱消息 (s15/s16) ─┘          │
                                          ▼
   ① 入口装配：压缩预处理器（若超阈值 s08）
   ② system prompt 组装 (s10)：identity + workspace + enabled_tools
      + 技能目录 (s07) + 记忆索引 (s09) + MCP 状态 (s19)
                                          ▼
   ③ 主循环 LLM 调用 (s01)  ──错误?──► 错误恢复 (s11)：max_tokens 升级 /
       ▲                              reactive compact / 429·529 指数退避+换模型
       │
       │ 响应里有 tool_use 块？───否──► ④ 记忆提取 (s09) → Stop hooks (s04，
       │                                   可强制续跑) → 返回结果
       │是（逐个工具过流水线）
       ▼
   ⑤ PreToolUse hooks (s04：权限/日志/审计)  → ⑥ 权限三闸门 (s03)
       → ⑦ 工具分发 (s02 TOOL_HANDLERS 查表；s19 mcp__server__tool 前缀；
             s13 慢命令 → 后台线程占位返回)
       → ⑧ 执行 → PostToolUse hooks (s04)
       → ⑨ tool_result 追加回 messages ───────────────┘(回 ③)
 
 会话内"计划/扩展"横切件：
   s05 todo_write（会话内清单，防漂移）        ← 单 Agent 的"先想后做"
   s06 task 工具（一次性 subagent，隔离上下文）
   s12 任务图（.tasks/*.json，blockedBy，可 claim，跨会话）
   s15-s17 团队（队友线程+收件箱+协议+自主认领）  ← 多人协作
   s18 worktree（每任务独立 git 目录，并行不互踩）
   s14 cron + s13 后台 = 让"新一轮"自己来，不用人等
```

教学顺序的隐藏逻辑（为什么 s01→s20 这样排）：先能动手（s01-04：循环/工具/权限/钩子）→ 能完成复杂任务（s05-08：计划/子代理/技能/压缩）→ 能记住与恢复（s09-11：记忆/prompt 组装/错误恢复）→ 能长期运行（s12-14：任务图/后台/定时）→ 能协作（s15-18：团队/协议/自治/隔离）→ 能接外部能力并合体（s19 MCP / s20 总装）。面试叙事就照这条主线讲。

**分清两个时间尺度（面试别混）**：
- **一个 turn**（毫秒~秒级）：一次 LLM 往返 + 可能多轮工具执行，s01–s04 的循环/工具/权限/hooks 都发生在这里；
- **一个任务/一次会话**（跨 turn、甚至跨进程重启）：目标要靠 todo/task graph 钉在磁盘（s05/s12），偏好要靠 memory 跨会话（s09），新输入可以来自 cron/后台/收件箱而不必等人（s13–s17），并行要靠 worktree 隔离（s18）。
- 被问"一次循环里发生了什么"答前者；被问"一个任务怎么不丢"答后者——两者都用"生命周期"叙事串起来正是本文骨架。

### 1.3 harness 与"直接调 LLM"的本质差别

| 维度 | 裸调 LLM（一次 API 往返） | harness（一次会话） |
|---|---|---|
| 状态 | 无状态，每轮重发 | 多步状态：messages 全程累积、工具结果回流、任务/记忆落盘 |
| 可观测 | 只见输入输出 | hooks + 事件日志 + transcript + 后台通知，每一步可审计可打断 |
| 权限 | 模型说什么就是什么 | 执行前有闸门：硬拒绝/规则/审批（甚至 hook 返回 allow 也不能绕过 deny/ask 规则） |
| 可恢复 | 错了就崩 | max_tokens 升级、压缩、退避重试、降级模型、reactive compact |
| 上下文 | 一次传完 | 预算落盘、裁消息、占位、LLM 摘要、记忆分层——"腾地方"是核心工程 |
| 扩展性 | 加逻辑改调用代码 | 加工具加两行、加行为挂 hook、加能力连 MCP，循环不动 |

一句话面试版：**harness = Tools + Knowledge + Observation + Action Interfaces + Permissions（+ 循环 + 上下文管理）**；模型提供智能，harness 提供行动空间与安全边界。

### 1.4 补充视角：harness 工程师到底在做什么 + 两种 harness 工作

README 总论给出 harness 工程师的五项真实工作，面试讲项目经历时按这五条归类自己做的事：
1. **实现工具**——给 agent 一双手（原子化、可组合、描述清晰；s02）；
2. **策划知识**——给 agent 领域专长，按需加载不前置塞入（s07）；
3. **管理上下文**——子 agent 隔离防噪声、压缩防淹没、任务系统让目标越过单次对话（s06/s08/s12）；
4. **控制权限**——沙箱、破坏性操作审批、信任边界（s03）；
5. **收集任务过程数据**——agent 的每条行动轨迹都是训练下一代模型的信号（harness 服务 agent，也在进化 agent）。

**两种"造 harness"的形态（20 讲 vs 两个 demo 的分工）**：
- 20 讲（s01–s20）= 从零**写**一个 harness：循环、工具、权限、hooks、压缩、记忆、团队全自己实现；
- 两个 demo = 用现成 agent 工具（Cursor/Claude Code）**配置**一个 harness：CLAUDE.md（规则）+ .claude/skills（工作流）+ .claude/hooks（质量门）把模型"包起来"。
两者是同一门手艺的两端：面试讲"我搭过 Agent"，用 20 讲的机制术语；讲"我让团队用 agent 干活不出事"，用 demo 的 CLAUDE.md+质量门叙事。

### 1.5 demo 精读：最小的"规则型 harness"长什么样

**01-simple_harnes_demo（极简 harness 闭环）**：三件套——①`CLAUDE.md`：Mission + Coding rules + Workflow rules + Safety rules + **Definition of done**（feature works + tests pass + validation passes，三条件缺一不算完成）；②`.claude/skills/`：`/plan`（需求→plans/*.md）、`/implement`（按计划改代码+写报告）、`/validate`（跑 scripts/validate.py 验收）三个命令级工作流；③`.claude/hooks/stop_validate.py`：**Stop 前质量门**，测试不过不让 Agent 结束。练习流程即 PIV 闭环：`/plan`（必须单独先跑，才落盘计划文件）→ `/implement` → `/validate` → 不过就 fix & retry。它的定义很直白：**harness = 不让模型自由发挥，用"规则+工作流+自动校验"把它包起来**；示例业务是 `app/password.py` 密码强度判断 + 单测。

**02-rag-harness-demo（同一套包在 RAG 全栈上，教学 45 分钟版）**：
- AI Layer 即 CLAUDE.md：命名规范（snake_case/PascalCase/test_<module>.py/api/<resource>）、代码模式（每 RAG 阶段独立成文件、路由只做解包、LLM 调用在测试里必须 mock）、构建命令表、**硬性规则**（改 app/ 下任何文件后对应测试必须仍通过；不允许跳过 Task 验证直接标记完成；不读写真实 .env、不递归删目录）。
- 自动化 Hook 两个：`PostToolUse` 每次编辑 `app/`、`tests/` 下 .py 后自动 `ruff check`（**建议性**：告警不阻塞，让 Agent 自修）；`Stop` 结束前自动跑 `python scripts/validate.py`（**阻塞性**：失败输出 `{"decision":"block","reason":...}` 阻止停止，Agent 收到 reason 继续修，`stop_hook_active` 防无限循环）。
- RAG 管道五阶段各一文件：`ingest → chunk(固定长度+overlap) → index(TfidfIndex，纯 CPU 无向量库) → retrieve → generate`（基线是模板拼接，课堂练习点=换成真 LLM，Prompt 约束：只能依据 context 作答、context 空不许编造；环境变量读 key，不入代码不入 Git）。
- 面试用法：当被问"RAG 项目怎么保证质量/怎么让 agent 稳定交付"，答"五阶段管线 + 硬规则 CLAUDE.md + PostToolUse lint + Stop 阻塞式质量门"，并强调一句：**质量门是代码级强制，不是提示词请求**——这就是 s04 Stop/PostToolUse 在生产项目上的样子。

---

## 2 实现层：最关键机制的提纯（9 讲重点，其余带过）

### 2.1 s01 主循环：判据与迭代结构（一切的骨架）

**机制**：`while True`：①把用户问题作为第一条 user 消息；②`client.messages.create(model, system, messages, tools)`；③把 assistant 响应追加进 messages；④判据——`stop_reason == "tool_use"` 就执行工具、把结果作为新 user 消息回填、继续循环；否则返回。不到 30 行就是最小可运行 harness。

```python
while True:
    response = client.messages.create(model=MODEL, system=SYSTEM,
                                      messages=messages, tools=TOOLS)
    messages.append({"role": "assistant", "content": response.content})
    if response.stop_reason != "tool_use":      # 判据：模型"做完了"
        return
    for block in response.content:              # 逐个执行模型要的工具
        if block.type == "tool_use":
            out = TOOL_HANDLERS[block.name](**block.input)
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": out})
    messages.append({"role": "user", "content": results})   # 结果回流
```

**判据的坑（附录核查，面试加分点）**：真实 Claude Code 并不信任 `stop_reason == "tool_use"`——流式响应里 stop_reason 可能滞后，而内容里已经出现 tool_use 块了。CC 用 `needsFollowUp` 标志：流式接收时一旦检测到 tool_use 块即置 true（query.ts:554-558）。教学版 30 行 ≈ CC 1729 行 query.ts 的核心，其余全是保护机制：State 对象 10 个字段（压缩追踪/恢复计数/stop hook 状态/轮次计数…）、多条退出与继续路径（blocking limit、prompt too long、abort、hook stop、token budget continuation…）、流式工具执行器（工具在模型还在生成时就并行启动）。**背结论：循环属于 agent，机制属于 harness——后面 19 章循环本身一行不改。**

### 2.2 s02 工具分发：TOOLS schema + TOOL_HANDLERS 查表

**机制**：加一个工具只做两件事：①`TOOLS` 数组加一条**工具定义**（name/description/input_schema，这是告诉模型"我能做什么"的 JSON schema）；②`TOOL_HANDLERS` 字典加一行 name→handler 映射。循环里的执行行从硬编码 `run_bash()` 变成查表 `TOOL_HANDLERS[block.name](**block.input)`。s02 把 1 个 bash 扩到 5 个（bash/read_file/write_file/edit_file/glob），循环零改动。模型可一次返回多个 tool_use（读 a、读 b、列 *.py），教学版按原始顺序逐个执行。

**生产要点（附录）**：CC 一个工具的真实调用链有 5 步验证：①Zod schema（类型）→②工具级 validateInput()（值语义，如路径在工作区内）→③PreToolUse hooks（可拦可改）→④权限检查（canUseTool→allow/deny/ask）→⑤tool.call()。并发不是"只读就能并发"，而是按具体输入判断 `isConcurrencySafe`（如 bash `ls` 可并发、`rm` 不可；TaskCreate 改状态但写不同文件也可并发），把调用按**连续块分批**：可并发的连续块同批并行（上限 10），遇不可并发开新批串行，批间严格顺序。大结果有 `maxResultSizeChars`：超限落盘、上下文只留预览+路径；FileRead 设为 Infinity——否则"读文件→落盘→再读落盘文件→再落盘"死循环。

### 2.3 s03 权限：不是 3 种而是 4 种决策

**机制（教学版三闸门）**：每个工具执行前插 `check_permission()`：
1. **拒绝列表**（硬拒绝，不执行）：`rm -rf /`、`sudo`、`shutdown`…——永远禁止；
2. **规则匹配**（取决于上下文）：如 write 到工作区外、bash 含 `rm `/`> /etc/`/`chmod 777`，命中即进闸门 3；
3. **用户审批**：暂停 `Allow? [y/N]`，用户决定。
三道都不命中 → 直接执行（大部分日常操作）。

**生产版（附录）**：CC 的 `PermissionResult` 是 **4 个 behavior：allow / deny / ask / passthrough**（passthrough=工具不表态，交给通用管线，教学无对应）。规则不是一张表而是 8 个来源按优先级合并：`userSettings < projectSettings < localSettings < flagSettings < policySettings`，再加 cliArg（--allowedTools/--deniedTools）、command、session 会话内临时授权；规则形如 `{toolName:"Bash", ruleBehavior:"deny", ruleContent:"npm publish:*"}`。auto 模式靠 **YoloClassifier**（小 LLM 看"工具调用+对话上下文"判断安不安全；连续拒绝太多回退人工）。两个安全事实要背：
- `isDestructive` 只是 UI 标签，**不参与权限决策**；
- **hook 返回 allow 也不能绕过 settings 里的 deny/ask 规则**（s04 不变式）——权限底线在规则层，不在 hook 层。
- 子 agent 的权限模式是 `'bubble'`：审批弹窗冒泡到父终端，不在子进程静默拒绝。

### 2.4 s08 上下文压缩：便宜的先跑，贵的后跑（顺序不能换）

**机制**：每轮 LLM 调用前先跑三层 0-API 预处理器，仍超阈值才上 LLM 摘要；API 报 413 再应急裁剪。

| 层 | 干什么 | 代价 |
|---|---|---|
| L3 `tool_result_budget` | **先跑**。最后一条 user 消息所有 tool_result 超 200KB → 从最大的开始落盘到 `.task_outputs/tool-results/`，上下文留 `<persisted-output>` 标记+前 2000 字符预览 | 0 API |
| L1 `snip_compact` | 消息 >50 条：保留头 3（初始上下文）+ 尾 47，中间裁掉并留占位说明 | 0 API |
| L2 `micro_compact` | 只留最近 3 条 tool_result 全文，更旧的替换为一行占位（"需要可重跑"） | 0 API |
| L4 `compact_history` | 先存 transcript（JSONL）→ 让 LLM 写摘要（保留当前目标/重要发现/已改文件/剩余工作/用户约束）→ 全历史替换为一条摘要；熔断：连续失败 3 次停 | 1 API |
| 应急 `reactive_compact` | API 仍回 prompt_too_long(413)：比摘要更激进，保留末尾 5 条，重试上限 1 | 1 API |

**顺序为什么不能换（面试必答）**：budget（L3）必须在 micro（L2）之前——micro 会把旧的大 tool_result 替换成一行占位符，budget 必须抢先把完整内容落盘。CC 真实执行序：budget→snip→micro→**contextCollapse**（独立上下文管理系统）→auto。边界保护：裁消息切口不能把 `assistant(tool_use)` 和它的 `user(tool_result)` 拆开（API 配对语义）。模型也可主动调 `compact` 工具触发摘要。生产细节：摘要 prompt 禁止调工具、先 `<analysis>` 再 `<summary>`；压缩后按预算恢复最近文件（如 5 个文件×5K token、总预算 50K）；CC 的 sessionMemoryCompact 会先用 s09 的 session memory 做轻量摘要省一次 LLM 调用。

### 2.5 s10 system prompt 组装：分段 + 按需 + 缓存

**机制**：把一大段硬编码 SYSTEM 拆成 `PROMPT_SECTIONS` 字典（identity/tools/workspace/memory…），`assemble_system_prompt(context)` 按 **context 的真实状态**拼接——始终加载段（身份/工具列表/工作区）每轮都要；按需段（记忆内容）只在 `.memory/MEMORY.md` 存在才拼。判断依据是"真实状态"（工具是否注册、文件是否存在），**不是在消息里搜关键词**。`get_system_prompt` 用确定性序列化做缓存 key（`json.dumps(sort_keys=True)`，**不用 Python `hash()`**——进程随机化且 list/dict 不可哈希）；context 没变直接返回缓存串。

**为什么不全塞（面试答法）**：system prompt 每轮都计费，无关指令是噪音，信息越少 LLM 越专注。生产版（附录）：静态 section 与动态 section 用 `SYSTEM_PROMPT_DYNAMIC_BOUNDARY` 分开——静态部分合并成 global cache 块命中 API prompt cache，动态部分不参与全局缓存；`mcp_instructions` 是唯一"易失"段（MCP server 可在轮次间断开）。标准模式核心约 20-30KB，CLAUDE_CODE_SIMPLE 只有 ~150 字符。**注意教学缓存 ≠ CC 的 API prompt cache**：教学版只是避免重复拼字符串。

### 2.6 s06 subagent：上下文隔离，只回传结论

**机制**：主 agent 把 `task` 当普通工具调 → `spawn_subagent(description)` 给子 agent **全新的 messages[]**、独立 SUB_SYSTEM（"直接完成任务，不要再委派"）、受限工具集（bash/read/write/edit/glob，**没有 task → 禁止递归 spawn**）、30 轮安全上限，跑自己的完整循环，结束只把**最后一条文本结论**回传主 agent。上下文被丢弃，但文件系统副作用保留在工作目录。**关键决策表**：隔离=全新 messages[]（中间过程不污染主对话）；只回结论（不是回传整个列表）；禁递归（不给 task 工具）；**子 agent 的工具调用仍走 PreToolUse 权限 hook——上下文隔离 ≠ 权限隔离**。

**什么时候用（面试答法）**：像人"开新终端追调用链"——子任务专注、中间过程与主目标无关、会污染注意力时。生产版（附录）：CC 有三种模式——Normal（全新上下文）、**Fork（`buildForkedMessages()` 构造 cache-friendly 前缀共享 prompt cache：父子 system/tools/messages 前缀字节级一致才命中）**、General-Purpose；隔离不是绝对的（readFileState 从父克隆防重复读文件）；递归防护用历史里的 `FORK_BOILERPLATE_TAG` 标记而非简单不给工具；支持 async 子代理（run_in_background 立即返回，完成经通知机制回来——s13 讲通知）。

### 2.7 s12 任务系统：blockedBy 依赖图，落盘可恢复

**机制**：`Task{id, subject, description, status(pending|in_progress|completed), owner, blockedBy[]}` 每任务一个 `.tasks/{id}.json`。工具 5 个：create_task（可带 blockedBy）/ list_tasks / get_task（完整 JSON）/ claim_task / complete_task。状态机只有两个动作：`claim`（pending→in_progress，设 owner；**前置检查 can_start=所有 blockedBy 都 completed，依赖不存在视为 blocked**；非 pending 或依赖未完成则拒绝认领）与 `complete`（→completed，并**扫描解锁下游**：返回 "Unblocked: xxx"）。跨会话时 `.tasks/` 还在磁盘，读文件即恢复进度。

**与 s05 TodoWrite 的分工（面试常考）**：TodoWrite = 当前会话内执行清单（内存，无依赖）；Task System = 跨会话可恢复的任务图（磁盘，blockedBy，owner 认领）。CC 两套并存，`isTodoV2Enabled()` 切换：交互式会话默认 Task(V2)，SDK/非交互默认 TodoWrite(V1)。生产细节：CC 9 字段（+blocks/metadata/activeForm），递增 ID+`.highwatermark` 防 ID 重用，`proper-lockfile` 双锁防并发认领（任务文件锁内重读防 TOCTOU + 列表级锁做 busy check），4 个工具（Create/Get/Update/List）均 concurrency-safe 且 shouldDefer（schema 不进初始 prompt，ToolSearch 后才可见），claim 与"开始工作"分离（claim 只设 owner，状态由 Update 改）。

### 2.8 s19 MCP：外部工具用标准协议进同一个工具池

**机制**：不需要给每个外部服务（Jira/自建部署/Notion）手写一套工具。MCP 定义：MCPClient（agent 端：连 server→`tools/list` 发现→`tools/call` 调用）；MCP Server（外部服务只需实现 tools/list + tools/call）。`connect_mcp(name)` 连接后工具立即可用；`assemble_tool_pool()` 把内置 + MCP 工具**动态组装**成工具池，名字规范化为 `mcp__{server}__{tool}`（所有非 `[a-zA-Z0-9_-]` 字符替换为 `_`）避免跨 server 冲突；description 带 (readOnly)/(destructive) 标注供权限判断。教学版 mock 了 stdio 子进程（真实是 JSON-RPC over stdio）。

**一个精致的工程坑（面试加分）**：s10 起的 prompt/tool **缓存必须去掉**——`connect_mcp` 之后工具池变了（新增 `mcp__docs__search` 等），缓存的旧工具列表会让模型调不到新工具，所以每次重新 assemble。生产版（附录）：6 种 transport（stdio/sse/http/ws/sse-ide/sdk），本地批量 3、远程批量 20 并发连接；工具池去重时**内置优先**（CC 在最后一个内置工具后放全局缓存断点，混排会破坏缓存设计）；MCP 工具有独立权限声明体系；server 可反向推送（channel 通知，agent 被 SleepTool 唤醒）；OAuth2+PKCE 全流程（过期前 5 分钟自动刷新）；连接错误分级重试（终局性错误连续 3 次→关闭重连）。定位一句话：**MCP = harness 的插件系统，让"能力"与"谁写的"解耦。**

### 2.9 s15 团队收件箱（+s16/s17 合并带过）

**机制**：子 agent（s06）是"临时工"，团队需要"长期队友"。三件套：①**MessageBus=文件收件箱**：每个 agent 一个 `.jsonl` 邮箱（`MAILBOX_DIR/{name}.jsonl`），发消息=往对方文件 append 一行 JSON，读消息=读完删文件（消费式）；教学用文件而非内存队列是因为跨线程可观察，CC 也是文件收件箱（`~/.claude/teams/{team}/inboxes/`）但加 proper-lockfile 防并发写冲突。②**spawn_teammate_thread**：Lead 用 `spawn_teammate` 工具启动队友 daemon 线程（自己的 system/messages/简化工具集 bash+read+write+send_message）。③**inbox 注入**：Lead 每轮结束后读自己收件箱，队友消息注入 history，LLM 才"看得见"并协调。教学版队友限 10 轮；CC 是 idle loop：干完一轮发 `idle_notification`，等收件箱，收到 `shutdown_request` 才退出。权限冒泡：队友要审批→发 permission_request 到 Lead→用户在 Lead 终端审批→permission_response 回队友（500ms 轮询）→继续/拒绝。

**s16/s17 各一句**：s16 把松散文本升级为**带 request_id 的请求-响应协议**（ProtocolState: pending→approved/rejected；dispatch_message 按类型路由、match_response 校验响应类型防串台；两种协议实例=关机握手、计划审批——真实 CC 共 15 种消息类型，关机是 shutdown_request→shutdown_approved/rejected→系统 teammate_terminated 三向）。s17 让队友自治：生命周期 WORK→IDLE（5s 轮询收件箱+任务板，60s 超时）→SHUTDOWN；`scan_unclaimed_tasks`（pending+无 owner+can_start 即可认领）；压缩后身份重注入（messages ≤3 条说明被 compact 过，重新插 `<identity>`）。生产版组合路径：idle_notification + 500ms 收件箱轮询 + fs.watch 任务板监听 + 主动 tryClaimNextTask，文件锁保证认领原子性。

### 2.10 其余 sXX 合并带过（不摊大饼）

- **s05 todo_write**：纯"规划"工具——不增加任何执行能力，只让模型先列清单再动手（pending→in_progress→completed 带状态渲染 + 连续 3 轮没更新就 nag 提醒，防长任务被工具结果带偏）。CC 的真实做法是在 ≥3 个 todo 全 completed 但缺 verification 项时追加校验提醒。
- **s07 skill_loading**：两级知识加载——①启动扫描 skills/ 目录把每个 SKILL.md 的 frontmatter（name/description）做成**目录注入 SYSTEM**（~100 tokens/技能，每轮都带）；②模型调 `load_skill(name)` 才把全文经 **tool_result** 注入（~2000 tokens，按需；经注册表查、不走文件路径→无路径遍历风险；SKILL.md 正文可指引后续 read_file/bash 拿 references/）。与 s08 天然衔接：按需加载解决"不该提前带的别带"，压缩解决"该丢的怎么丢"。CC 里技能来源不止一个目录，frontmatter 还有 context(inline/fork)/allowed-tools/hooks/paths(条件激活)/model 等字段；目录预算 ≈ 上下文窗口 1%（上限 8000 字符）。
- **s13 background_tasks**：bash schema 加 `run_in_background` 参数让**模型自己决定**丢后台（教学版另有 install/build/test 关键词启发式兜底）；后台 = daemon 线程，立即返回 `bg_id` 占位 tool_result；完成后以 **`<task_notification>` 独立注入**——不复用原 tool_use_id（API 语义：一个 tool_use 只对应一个 tool_result）。CC 是单线程事件循环，"后台"=不 await，输出重定向到文件；7 种后台任务类型；通知队列分 next/later 优先级；后台 bash 有停滞看门狗（45s 无输出检测交互式提示卡死）。
- **s14 cron_scheduler**：四层解耦——调度 daemon 线程（每秒检查五段式 cron）→ `cron_queue` → queue processor（Agent 空闲且有任务就拉起一轮）→ agent_loop 消费注入 `[Scheduled] prompt`。关键设计：date-aware minute_marker 防同分钟重复触发；单 job try/except 坏任务不杀线程；注册前 validate_cron；durable 任务写 `.scheduled_tasks.json` 重启恢复。**重要前提（面试主动提）**：调度器活在进程内，进程关调度就停——durable 只是任务定义跨重启；要"应用关了还定时跑"得上 OS crontab/systemd。生产版还有防惊群抖动、7 天自动过期、MAX_JOBS=50。
- **s18 worktree_isolation**：任务管"做什么"，worktree 管"在哪做"，按 ID 绑定。`create_worktree(name, task_id)`：name 白名单 `[A-Za-z0-9._-]{1,64}` 防路径穿越 → `git worktree add -b wt/{name}` → `bind_task_to_worktree` 只写 task.worktree 字段**不改状态**（仍 pending，等队友认领）；队友 claim 到带 worktree 的任务后 bash/read/write 自动切 cwd。收尾两选：keep（留分支给人 review）/remove（有未提交改动默认拒绝，除非 discard_changes=true）；events.jsonl 审计日志。CC 教学版差异：真实 CC 的 worktree 与 task 是两个独立系统（EnterWorktree 用 process.chdir 进程级切目录；子 agent 隔离用 cwdOverride），没有 task-worktree 绑定。
- **s20 comprehensive**：唯一"新机制"是总装。27 个内置工具按生命周期位置归位：用户输入→UserPromptSubmit hooks→cron/后台通知注入→压缩管线→memory+skills+MCP 状态组装 system prompt→LLM→**以实际 tool_use 块（不是 stop_reason）判定继续**→PreToolUse+permission→TOOL_HANDLERS/MCP/background 分发→PostToolUse→tool_result 回流→下一轮；无 tool_use→Stop hooks→返回。两层计划并存（todo_write 会话级 + task graph 磁盘级）；两种委派并存（task 一次性隔离 vs spawn_teammate 持久协作）。核心结论：**Claude Code 的复杂性不是"另一个 agent 大脑"，而是一个成熟 harness 的复杂性——机制很多，循环一个。**

### 2.11 常考关键数字与生产细节（附录核查，背个位数就够）

| 主题 | 数字/细节 | 出处 |
|---|---|---|
| 主循环状态 | CC State 对象 10 字段：messages / toolUseContext / autoCompactTracking / maxOutputTokensRecoveryCount / hasAttemptedReactiveCompact / maxOutputTokensOverride / pendingToolUseSummary / stopHookActive / turnCount / transition | s01 附录 |
| 工具结果落盘 | `maxResultSizeChars` 超限落盘留预览；**FileRead 设为 Infinity** 防"读文件→落盘→再读落盘文件→再落盘"死循环 | s02 附录 |
| 工具并发 | `isConcurrencySafe` 按**具体输入**判（bash ls 可并发、rm 不可）；前台并发上限默认 10；连续块分批、批间严格顺序 | s02/s13 附录 |
| hooks | CC 27 个事件（教学 4 个是同构子集）；HookResult 常用字段：blockingError（注入对话让模型自纠）、preventContinuation（优雅停机）、permissionBehavior、updatedInput、additionalContext | s04 附录 |
| 压缩参数 | autoCompact 熔断=连续失败 3 次；reactive 重试上限 1；压缩后恢复预算 50K token / 最多 5 个文件 × 5K；time-based micro_compact 间隔 60 分钟；摘要输出上限 20K | s08 附录 |
| 记忆 | 注入预算：每记忆文件 ≤200 行/4096 字节，单 session 总预算 60KB；LLM side-query 最多选 5 条；MEMORY.md 索引上限 200 行/25KB；Dream 四层门控（≥24h、扫描节流、≥5 会话改动、锁文件 1h 过期） | s09 附录 |
| system prompt | 核心 ~20–30KB；CLAUDE_CODE_SIMPLE ≈150 字符；静态段与动态段用 boundary 分 cache scope；唯一"易失"段 = mcp_instructions；CLAUDE.md+currentDate 作为 `<system-reminder>` user 消息前置（不进 system） | s10 附录 |
| subagent fork | 共享 prompt cache 需 5 要素字节级一致：system prompt / tools / model / messages 前缀 / thinking config | s06 附录 |
| 任务系统 | ID 递增 + `.highwatermark` 防重用；`proper-lockfile` 任务文件锁（重试 30 次、退避 5–100ms）+ 列表级锁；TaskCreated/TaskCompleted hooks | s12 附录 |
| 团队 | 收件箱在 `~/.claude/teams/{team}/inboxes/`；CC 共 **15 种消息类型**；teammate 之间**禁止嵌套 spawn** | s15/s16 附录 |
| MCP | 6 种 transport（stdio/sse/http/ws/sse-ide/sdk）；连接并发本地批量 3、远程批量 20；配置优先级：claude.ai 连接器 < plugin < user settings < 已批准 .mcp.json < local settings（企业 managed-mcp.json 存在时排除其余） | s19 附录 |

### 2.12 九大机制的面试一句话（考前 60 秒回忆表）

| 机制 | 一句话本质 | 最容易答错的点 |
|---|---|---|
| s01 主循环 | 模型决定何时停、代码只负责执行并回填结果 | 生产**不信 stop_reason**，看内容里有没有 tool_use 块（needsFollowUp） |
| s02 工具系统 | schema 告诉模型能做什么 + handler 执行，双注册查表分发 | 加工具=两处修改；循环零改动 |
| s03 权限 | 硬拒绝→规则→审批三闸门；生产四决策 allow/deny/ask/passthrough | deny/ask 规则不能被 hook 的 allow 绕过；isDestructive 只是 UI 标签 |
| s04 hooks | 输入/执行前/执行后/停止四个事件点，扩展注册不内联 | Stop hook 可"强制续跑"；blockingError 是把错误喂给模型自纠 |
| s08 上下文压缩 | 大结果落盘→裁消息→旧结果占位→LLM 摘要，便宜先跑 | 顺序不可换：budget 必须先于 micro，否则完整内容先被占位符替换 |
| s10 system prompt | 按真实状态分 section 运行时拼装 + 确定性缓存 | 缓存会在"能力变化"时失效（如 MCP 连上后工具池变了） |
| s06 subagent | 全新 messages[] 跑自己的循环，只回传结论 | 隔离上下文 ≠ 隔离权限；防递归（无 task 工具/标记检测） |
| s12 任务系统 | 每任务一个磁盘 JSON + blockedBy 依赖图 + claim/complete | 与 s05 todo_write 是两套系统：内存清单 vs 跨会话可认领任务图 |
| s19 MCP | 外部服务实现 tools/list+call 即接入，工具池动态组装 | 名字规范 mcp__server__tool；连上后 prompt/tool 缓存必须重建 |

---

## 3 工程层：错误恢复 / hooks / 后台与定时 的取舍与避坑

### 3.1 错误恢复（s11）：错误分类 → 各管各的恢复

**三类最常见的故障与对策（先背这张表）**：

| 故障 | 症状 | 恢复动作 | 上限 |
|---|---|---|---|
| 输出截断 | stop_reason=max_tokens | ①先把 max_tokens 8K→64K **原请求重试**（不追加截断输出）；②仍不够才存截断输出+注入续写提示（"Resume directly—no apology, pick up mid-thought"） | 升级仅 1 次；续写 ≤3 次 |
| 上下文超限 | prompt_too_long(413) | reactive compact（s08 应急层）后重试 | 压缩仅 1 次，再超就退出 |
| 临时故障 | 429 限流 / 529 过载 | 指数退避+抖动 `min(500×2^attempt, 32000)ms + 随机0~25%`；服务器 Retry-After 优先；**连续 3 次 529 → 切 fallback 模型** | ≤10 次 |

**架构结论**：外层 try/except 抓 API 异常、with_retry 管瞬态错误、stop_reason 检查管截断——三种机制各管一种错误类型，恢复后 `continue` 回循环开头。教学版 3 条 vs CC 十几种 reason/transition（aborted_streaming、stop_hook_blocking、token_budget_continuation、diminishing returns 检测——连续 3 次 continuation 且增量 <500 token 就停，避免"无产出续写"）。

**避坑清单（工程层通用，README 提炼）**：
1. **截断输出不能先追加再重试**——首次升级要"原请求原样重试"，否则半截输出污染上下文；
2. **压缩重试只有一次机会**——压缩过还超限说明"再压也没用"，退出比死循环好；
3. **退避必须有抖动**——全世界的重试同时打上来等于没退避；
4. **熔断器处处要**——autoCompact 连续失败 3 次停、reactive 重试上限 1、Stop hook 有 stopHookActive 防"模型自纠→hook 再报错→再自纠"死循环。

### 3.2 hooks（s04）：挂在循环上，不写进循环里

**4 个核心事件覆盖一个完整 cycle**：`UserPromptSubmit`（输入后、进 LLM 前：注入上下文/拦截修改）→ `PreToolUse`（工具执行前：权限、日志、审计；返回非 None=阻止执行）→ `PostToolUse`（执行后：副作用如自动 git add、大输出告警）→ `Stop`（循环退出前：收尾统计；返回非 None=**强制续跑**）。注册表 = dict[事件]→回调列表；循环只调 `trigger_hooks(event, ...)`，回调里第一个返回非 None 者生效。

**设计动机（面试答法）**：不加 hook 时，每加一个横切需求（日志/权限/通知/副作用）都要改 agent_loop 本体，循环很快"认不出来"。hook 把**循环变成稳定核心**、扩展挂在外围，且多个 hook（权限+日志+审计）可以叠在同一事件点上。

**生产事实（背 4 条）**：①CC 有 27 个 hook 事件（会话/用户交互/子 agent/压缩/团队/配置…），教学 4 个是同构子集；②HookResult 带 `blockingError`——把错误注入对话让**模型自己修正**（不是静默失败）；③**关键不变式：hook 说 allow 也不能绕过 settings 的 deny/ask 规则**，否则 hook 脚本是权限后门；④PostToolUse 返回 preventContinuation 是"优雅停机"（hook_stopped_continuation），不是崩溃。demo 印证：02-rag-harness-demo 的 Stop hook 输出 `{"decision":"block","reason":...}` 阻止 Agent 在测试红时结束——质量门是**代码级强制**，不是提示词请求。

### 3.3 后台与定时（s13/s14）的取舍

| 问题 | 结论 |
|---|---|
| 什么操作该后台？ | 分钟级操作（install/build/test/deploy）；毫秒级（read/git status）同步。判定主路径是**模型显式 run_in_background**（CC bash schema 内建参数），关键词启发式只是兜底 |
| 后台完成怎么通知？ | 独立 `<task_notification>` 注入下一轮，**不复用 tool_use_id**（保持 API 工具配对语义）；占位结果让模型"先干别的，回头再看" |
| 后台的边界？ | 教学版内存 dict 追踪（daemon=True 随进程退出）；生产版输出重定向文件、支持停止/续读、停滞看门狗防交互式卡死 |
| cron 的边界？ | **进程内调度**：进程死调度停，durable 只保任务定义；真要"应用关闭仍触发"用系统级 cron/systemd（README 明示） |
| 轮询 vs 事件？ | 教学统一轮询（scheduler 1s / queue processor 0.2s / idle 5s）；CC 组合：fs.watch 文件监听 + 通知队列 + 轮询兜底，且都带锁防并发 |

**整体避坑三条**：①**通知与 tool_result 语义**：一个 tool_use 只能配一个 tool_result，后台完成是独立事件，混用会破坏 API 配对；②**缓存与动态能力冲突**：MCP 连上后工具池变了，prompt/tool 缓存必须失效重建（s19）；③**权限底线在规则层**：hook 的 allow、模型的请求都越不过 deny/ask 规则（s03/s04），子 agent 隔离上下文但**不隔离权限**（s06）。

### 3.4 最小质量门范式（两个 demo 提炼的工程模板）

面试讲"我怎么保证 agent 干活质量"时，直接套这个三层模板（README 与 demo 均支持）：

1. **规则层（CLAUDE.md 类）**：把"完成标准"写死成代码可判定的条件——DoD 三元组（功能可用 + 测试通过 + 校验通过）；硬性规则（不许读真实 .env、改文件后对应测试必须仍绿、测 LLM 必须 mock）。
2. **过程层（PostToolUse 建议性门）**：每次编辑后自动跑轻量检查（ruff lint），**告警不阻塞**——让模型自己看到并修复，保持节奏不被打断。
3. **终局层（Stop 阻塞性门）**：Agent 想结束前强制跑完整验证（pytest/validate.py），失败返回 `{"decision":"block","reason":...}` 阻止停止——**质量门是代码强制，不是提示词请求**；用 stopHookActive / blockingError 机制防止"检查失败→模型修→再失败→死循环"。

### 3.5 把教学机制搬到生产：README 的取舍提醒

- **轮询 vs 通知**：教学用固定间隔轮询（scheduler 1s / idle 5s / micro 60min）；生产优先"事件驱动 + 通知队列 + 锁"，轮询只做兜底（CC 的 fs.watch 任务板、useInboxPoller、time-based microcompact 都是反例教材）。
- **内存 vs 磁盘**：教学版大量状态在内存 dict（background_tasks、scheduled_jobs、pending_requests）；生产关键状态必须落盘或可重建，并加锁防并发（proper-lockfile、highwatermark、.consolidate-lock）。
- **进程边界**：cron 调度活在进程内；要"应用关闭仍定时"得用 OS 级 cron/systemd（README 明示，别答反）。
- **教学简化是刻意的**：每章的"简化是刻意的"清单本身就是面试题库——如权限 8 来源→1 张 DENY_LIST、27 hooks→4、Zod→JSON Schema、embedding→无、file lock→无。被问"你知道生产实现更复杂在哪"时照单回复即可。

---

## 4 面试卡（12 问：问题 → 要点 → 出处）

1. **Q：一条用户消息在 harness 里的一生是怎样的？**
   A：触发（用户/cron/后台通知/收件箱）→ UserPromptSubmit hooks → 上下文压缩预处理器（若超阈值）→ system prompt 按状态组装（身份/工具/工作区/技能目录/记忆索引/MCP 状态）→ LLM 调用（外层包错误恢复）→ 有 tool_use 块则逐工具走 PreToolUse→权限→分发（内置/MCP/后台）→执行→PostToolUse→tool_result 回流；模型不再调工具→记忆提取→Stop hooks→返回。出处：s20（总装表）+ s01/s04。
2. **Q：agent 循环什么时候停？判据可靠吗？**
   A：教学版看 stop_reason != "tool_use"；生产 CC **不信任 stop_reason**（流式下滞后），改为流式期间一旦出现 tool_use 块就置 needsFollowUp 继续。结论：判据是"内容里有没有 tool_use 块"，不是字段值。出处：s01 附录。
3. **Q：加一个新工具需要改几处？**
   A：两处——TOOLS 数组加 schema 定义（告诉模型能做什么）+ TOOL_HANDLERS 加一行 handler 映射；主循环零改动。出处：s02。
4. **Q：一次工具调用在生产 harness 里经过哪些验证？**
   A：Zod schema（类型）→ validateInput（值语义，路径在工作区）→ PreToolUse hooks（可拦/可改输入）→ 权限检查（allow/deny/ask/passthrough）→ 执行；并发则按 isConcurrencySafe 分批（可并发连续块同批并行、不可并发串行、批间有序）。出处：s02/s03 附录。
5. **Q：权限系统怎么设计？hook 能绕过权限吗？**
   A：四决策 allow/deny/ask/passthrough；规则来自多来源按优先级合并（user<project<local<flag<policy + cli/command/session）；**hook allow 不能绕过 deny/ask 规则**——权限底线在规则层。auto 模式由分类器 LLM 预判安全。出处：s03/s04。
6. **Q：hooks 和"把逻辑写进循环"有什么区别？**
   A：循环是稳定核心，只调 trigger_hooks(event)；扩展以回调注册在 4 个事件点（输入前/执行前/执行后/停止）上，可叠加（权限+日志+审计同点）；Stop hook 还能强制续跑、PostToolUse 能优雅停机。CC 有 27 个事件，模式相同。出处：s04。
7. **Q：上下文满了怎么办？为什么压缩顺序重要？**
   A：四层：大 tool_result 落盘留标记（budget）→ 裁中间历史消息（snip，保留头 3 尾 47）→ 旧 tool_result 换占位（micro，留最近 3 条）→ LLM 全量摘要（compact_history，先存 transcript）；413 应急 reactive compact。**budget 必须先于 micro**，否则完整内容还没落盘就被占位符替换了。便宜的先跑、贵的后跑。出处：s08。
8. **Q：压缩会丢用户偏好，怎么补？**
   A：加一层不参与压缩、跨会话的记忆：.memory/*.md + MEMORY.md 索引（目录常驻 SYSTEM）+ 每轮启动按需注入（LLM side-query 从 name/description 里选最多 5 条相关记忆）+ 每轮结束提取（stop 且无 tool_use 时）+ 低频整理去重。要点：**记忆选择用 LLM 判断相关、不是 embedding 向量相似度**；四类记忆 user/feedback/project/reference；写入前查重。出处：s09。
9. **Q：subagent 和 tool、teammate 各解决什么问题？什么时候用谁？**
   A：tool=原子动作（一双手）；subagent=一次性委派，解决**上下文隔离**（中间过程别污染主对话，只回结论；禁递归）；teammate=持久协作（多轮、异步收件箱、可自组织认领）。选型：子任务独立且过程无关→subagent；长期并行、需互通→teammate；能用一个工具搞定→别开新 agent。出处：s06/s15/s17。
10. **Q：system prompt 为什么要运行时组装？**
    A：静态一大段的问题——换项目重写全局、改一处可能冲突、无关内容每轮烧 token。拆 section 后按**真实状态**（工具是否注册、记忆文件是否存在）按需拼，再用确定性 key 缓存避免重复拼接；生产上静态/动态分段还有利于 API prompt cache 命中。出处：s10。
11. **Q：MCP 解决什么问题？工具名为什么要带前缀？**
    A：外部服务实现 tools/list+tools/call 标准协议即可被 agent 调用，不用为每个服务手写工具代码——能力与实现解耦。工具池动态组装，`mcp__server__tool` 命名 + 字符规范化防跨 server 冲突与注入；副作用是**工具池变化会让 prompt 缓存失效**。出处：s19。
12. **Q：为什么需要 harness？直接调 LLM 不行吗？**
    A：Agency（感知-推理-行动）来自模型训练，但 agent 产品 = 模型 + harness（工具/知识/观测/行动接口/权限）。裸调 LLM 无状态、不可观测、无权限边界、错了就崩；harness 提供多步状态、权限闸门、hooks 可观测、压缩与记忆、错误恢复、任务持久化、团队与外部能力——**你造的不是智能，是智能栖居的世界**。出处：README-zh 总论 + s20。

### 4.1 考官可能追问的四个变体（答案要点给到，细节回 §2/§3 查）

1. **追问：todo_write 只是个工具，凭什么能改变 agent 行为？**
   要点：它不增加执行能力，增加的是**结构**——把隐含的"步骤"变成上下文里可见、可勾选、带状态的清单（pending→in_progress→completed），再加 reminder 把漂移的注意力拉回来；给模型一个"自我规划的脚手架"，比在提示词里喊"要有计划"可靠。出处：s05。
2. **追问：记忆相关性为什么用 LLM 选、不用 embedding？**
   要点（README 事实，勿加戏）：CC 就是让 Sonnet 看 name+description 清单做 side-query 选出最多 5 条（"不确定就不要选"），教学版同思路并加关键词降级；全文注入有预算（每文件 ≤200 行/4096B，单 session ≤60KB）。出处：s09 附录。
3. **追问：这套 harness 能变成"常驻个人助手"吗？还差什么？**
   要点：20 讲教的是"用完即走"型（开终端→干活→关掉，重开是全新会话）。README 姊妹仓库 claw0/OpenClaw 证明：在同样的 agent core 上加 **heartbeat（每 30s 自己醒一次找活）+ cron（自己安排未来任务）+ IM 多通道路由 + 不清空的记忆 + Soul 人格**，就变成主动式常驻 agent——"被动临时会话 → 主动常驻助手"的跃迁仍是加 harness 机制，不是换模型。出处：README-zh 姊妹教程段。
4. **追问：为什么 20 讲要把 permission 放在 hooks 前面讲、循环却永远不改？**
   要点：教学顺序刻意让每个机制**可单独增量验证**（加工具不动循环、加权限不动分发、加 hooks 不动权限逻辑），对应 s20 的结论：可组合性来自"机制挂在循环上、不写进循环里"——这也是把 19 个机制合回一个 while True 仍能跑的原因。出处：s02–s04/s20。

---

## 5 五分钟速查卡

| sXX | 一句话 | 面试作用 |
|---|---|---|
| s01 | while True + stop_reason(tool_use?)：用工具就续、不用就停 | 一切的地基；背 CC 不信 stop_reason 用 needsFollowUp |
| s02 | 加工具 = schema 定义 + handler 两行，查表分发 | 答"工具系统怎么设计"；5 步验证链+分批并发 |
| s03 | 执行前三道闸门：硬拒绝→规则→审批；生产四决策+8 来源规则 | 答权限；hook allow 不能绕过 deny/ask |
| s04 | 4 个事件点挂扩展，循环只调 trigger_hooks | 答可观测/扩展性；Stop hook 可强制续跑 |
| s05 | todo_write：只给规划能力不给执行能力 + nag | 答"怎么让 agent 有计划" |
| s06 | subagent：全新 messages[] 只回结论，禁递归，权限不跳过 | 答上下文隔离；fork 模式共享 prompt cache |
| s07 | 知识两级加载：目录常驻、全文按需 load_skill | 答"别把文档全塞 prompt"；frontmatter |
| s08 | 四层压缩：落盘/裁消息/占位/LLM 摘要，budget 先于 micro | 答上下文管理；顺序不可换+413 应急 |
| s09 | .memory 文件+索引+LLM 选记忆+提取+Dream 整理 | 答跨会话记忆；选记忆不用 embedding |
| s10 | system prompt 按真实状态分 section 拼 + 缓存 | 答 prompt 工程；静态/动态与 API cache |
| s11 | 截断升 8K→64K、超限 reactive compact、429/529 退避+换模型 | 答韧性/生产级；三种错误三种对策 |
| s12 | 任务 = 磁盘 JSON + blockedBy 图 + claim/complete | 答任务系统；与 todo_write 分工 |
| s13 | 慢命令后台线程，完成注入 task_notification（不复用 tool_use_id） | 答异步；一个 tool_use 配一个 tool_result |
| s14 | 调度线程→队列→空闲自动拉起一轮；进程内调度是边界 | 答定时/自主触发；durable≠系统级 cron |
| s15 | MessageBus 文件收件箱 + 队友线程 + Lead 注入 inbox | 答多 agent 通信；权限冒泡 |
| s16 | request_id 关联的请求-响应协议（关机/计划审批） | 答协议层；type 校验防串台 |
| s17 | WORK→IDLE(轮询看板)→SHUTDOWN，自动认领 | 答自治/自组织；claim 前置 can_start |
| s18 | git worktree 每任务一目录一分支，绑定不改状态 | 答并行不互踩；删除前检查未提交改动 |
| s19 | MCP：tools/list+call 标准协议，mcp__server__tool 进工具池 | 答生态接入；连上后缓存要失效 |
| s20 | 机制很多，循环一个：27 工具按位置归位 | 答"综合架构"；两层计划+两种委派 |

> demo 记忆锚点：01-simple = "CLAUDE.md 规则 + /plan→/implement→/validate 工作流 + Stop 质量门"的最小 harness（DoD：功能可用+测试过+校验过）；02-rag = 同一套包在 RAG 五阶段管道上（PostToolUse 每次编辑后 ruff 建议性 lint，Stop 结束前 pytest 阻塞式质量门，LLM 调用在测试里必须 mock）。面试讲"RAG 项目的工程化"直接引用：**质量门是代码强制，不是提示词请求**。

## 附：时间有限时怎么回读原仓库

- **第一优先（面试细节可能深挖）**：`s01/s03/s08` 的"深入 CC 源码"附录、`s20` 的"组件在循环中的位置"表、`README-zh.md` 总论前 120 行（Agency 来自模型的论证 + Harness 公式 + 五件工作）。
- **第二优先**：`s06/s10/s19` 附录（fork 共享 prompt cache 五要素、静态/动态 boundary、6 transport 与配置优先级）；两个 demo 的 README 全文（短，例子可直接引用当项目叙事）。
- **可跳过（本文已提纯到位）**：s05/s07/s13/s14/s16/s17/s18 正文与附录。
- **code.py**：想动手验证就按 README 推荐路径跑 `s01 → s08 → s20`（需 ANTHROPIC_API_KEY）；纯面试准备可不跑——本提纯的机制描述均以 README 为准，与 code.py 实现可能有细节出入【存疑时以原 README 为准】。

**最后 3 句可背的金句**：
1. "Agency 来自模型，harness 让 agency 落地。造好 harness，模型会完成剩下的。"
2. "循环属于 agent，机制属于 harness——后面 19 章，循环一行没改。"
3. "你不是在编写智能，你是在构建智能栖居的世界。"（Bash is all you need.）
