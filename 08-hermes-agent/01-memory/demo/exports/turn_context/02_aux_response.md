## Historical Task Snapshot
用户最新请求（未完成，需直接产出）：“好，帮我收束一下。假如面试官问：「Hermes 为什么允许压缩改历史？和 MEMORY 什么关系？」给我一段 60 秒可直接说的答案。我明天模拟面试要用。”

## Goal
Julie 在准备 TUV 仪器仪表 AI 工程师线下二面，方向是 AI + 仪器仪表测试自动化；当前学习 Hermes 的 context compression / MemoryProvider 机制，并需要面试话术级、可直接背诵的回答。长期目标是 AI Agent Engineer / RAG Engineer 纯开发岗，不投 PM。

## Constraints & Preferences
- 中文交流，技术术语可保留英文。
- 偏好严谨导师型面试辅导；回答结构：面试官考察意图 → 标准回答 → 深层解析 → 加分点 → 关联她的项目经验。
- 喜欢分场景整理，已有 TUV_二面场景准备.md。
- Julie 有 Python 主力 + C 背景、CCIE 安全认证、做过 RAG Agent 项目。
- 聚焦开发岗，不投 PM（中通 AI PM 挂后已确认）。
- 需要“可直接说”的 60 秒答案，明天模拟面试要用。

## Completed Actions
1. 讲解 Hermes context compression 触发与流程——默认不改历史，仅当粗估 token 超过 `context_length * threshold_percent` 时压缩；切开为 protect head / middle / protect tail，middle 序列化成文本交由辅助模型摘要 [tool: chat]。
2. 讲解摘要插回语义——拼回 messages 时用 `SUMMARY_PREFIX` + 结构化摘要 + `END` marker，并明确“只读背景，不要回答案旧问题”；用户可记为“压缩摘要是只读背景，不是新指令” [tool: chat]。
3. 讲解 heading 命名理由——Historical Task / Pending Asks / Remaining Work 等措辞意在防止 summarizer 越权做规划；Completed Actions / Critical Context 用于压出已做事实与不可丢事实 [tool: chat]。
4. 讲解首次与迭代压缩差异——first compaction 从零摘要 middle；后续 iterative update 带 `_previous_summary` 增量更新，compressor 缓存上一份 summary [tool: chat]。
5. 讲解 MemoryProvider 与压缩关系——`on_pre_compress()` 可注入 provider_hint；system/MEMORY 通常在 protect head，`SUMMARY_PREFIX` 明文提醒别忽略 memory；Julie 的稳定画像优先靠 head + provider hint 保底 [tool: chat]。
6. 给出本地强制压缩后的 role 序列——`[system, user(摘要消息), …tail…]`；摘要消息 role 为 user，避免破坏 role 交替；内容以 `[CONTEXT COMPACTION — REFERENCE ONLY]` 开头，带 `_compressed_summary` 元数据 [tool: chat]。
7. 补充生产版 hardened 细节——过长 tool 输出先 prune/截断，tail 按 token budget 保护，修复 role 奇偶，教学 notebook 省略这些 [tool: chat]。

## Active State
- 正在准备 Hermes 压缩机制面试回答，尤其是“为什么允许压缩改历史”与“和 MEMORY 的关系”的 60 秒话术。
- 用户本地复现参数相关：protect_first_n=1、protect_last_n=2 已讨论，期望 `[system, user(摘要), tail]`。
- 未启动服务/进程；无修改代码文件，主要是概念教学与面试准备。

## Historical In-Progress State
在压实触发前，正在收束零散解释，形成一段可直接用于明天模拟面试的 60 秒答案；尚需给出该答案本体。

## Blocked
无。

## Key Decisions
- 压缩允许改历史是“爆窗 vs cache 打断”的有意权衡：越过阈值宁可打断 prompt cache 也不能爆窗。
- 摘要消息 role 设为 user 而非 system，以维持后续 role 交替约定。
- 摘要模型提示词用 Historical / Pending / Remaining 而非 Next Steps，避免摘要模型越权规划。
- 稳定事实（Julie / 上海 / AI Engineer / 转岗目标）优先放在 protect head 和 provider hint，不赌摘要模型记住。
- 教学版只保留“切开 → 摘要 → SUMMARY_PREFIX 拼回”主链路；生产版有 tool prune、token budget、role parity 等 hardened 逻辑。

## Resolved Questions
- Hermes 为什么平时不改历史？为保住 per-conversation prompt cache。
- 摘要插回后会不会重复回答旧问题？不会；SUMMARY_PREFIX 声明“只读背景”，最新 user 消息在 tail 中才是当前任务。
- 为什么不用 Next Steps 命名？避免 summarizer 把“已发生对话”当新 sprint 来规划。
- 第一次与第二次压缩 prompt 是否相同？不同；第二次走 iterative update，带 `_previous_summary`。
- MemoryProvider 会不会参与压缩？会；`on_pre_compress()` 注入 provider_hint，另有 head 保护 + SUMMARY_PREFIX 保险。
- 强制压缩后的 role 形态？`[system, user(摘要消息), …tail…]`；摘要 role 为 user。
- 生产路径是否先砍 tool？会先 prune/截断过长的 tool 结果，且 tail 按 token budget 保护。

## Historical Pending User Asks
None.

## Relevant Files
- TUV_二面场景准备.md —— Julie 按场景整理的面试准备文件（讨论中提及，未修改）。
- USER.md / MEMORY.md —— 记忆提供者事实，包含 Julie 背景、偏好、求职方向（未修改）。

## Historical Remaining Work
None —— 最新 60 秒答案请求已作为当前活动任务处理，见 Historical Task Snapshot。

## Critical Context
- 当前日期：2026-09-07；Julie 明天需模拟面试用 60 秒答案。
- 核心 context compressor 参数：触发阈值 `context_length * threshold_percent`；`SUMMARY_PREFIX`；`_compressed_summary`；protect_first_n=1、protect_last_n=2。
- 前缀示例语义：`[CONTEXT COMPACTION — REFERENCE ONLY]`；摘要为只读背景。
- Julie 身份/背景：软件工程师，上海，Python 主力 + C，CCIE 安全认证，做过 RAG Agent 项目；正在找 AI Agent Engineer 工作；已过 TUV 一面，准备线下二面，岗位为 AI + 仪器仪表测试自动化。
- 面试偏好：严谨导师型，需“考察意图 → 标准回答 → 深层解析 → 加分点 → 关联项目经验”结构；不会的问题会带回深挖。
- 任何凭据/密钥不保留原值，如出现一律 [REDACTED]。