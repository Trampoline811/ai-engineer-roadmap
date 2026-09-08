# D2 — 记忆与上下文收尾

> 日期：____ ｜ 今日面试锚（A）：
> 📖 主阅读（提纯版）：先读 `提纯精读\P2-记忆实现对照提纯.md` + `prep0-plugin-memory-arch.md` + 已有记忆专题（Agent_Memory_Deep_Dive.md）；**Mem0 详解：`99-My idea\AI Agent 学习指南\01.longterm memory.md`（上游 9/8 同步新源，P2 已蒸馏）**；源文件按需深挖**"你凭什么决定记什么/忘什么？" + "memory 与 RAG 的边界？"**
> 主轴位置：状态与记忆（总图第二层：会话恢复、记忆注入、压缩）
> ⚠️ 若启动前一天已按"1h/2h 版"补过三因子+mem-provider，本日压缩为 2-3h，省出时间做写码练习。

## 时间盒（≈8.5h 有效学习）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 08:30-09:00 | 主动回忆 | 口述 D1 复盘 3 问（不看笔记） | 3 答记录 |
| 09:00-10:30 | 跑通 D | `03-memory\04_three_factor_scoring.ipynb`（**纯 stdlib 可离线**）；`03-memory\02_long_term_memory.ipynb`（mock 向量可离线） | 三因子公式口述 + 见**写码挑战②** |
| 10:30-12:30 | 源码 M | `08-hermes-agent\01-arch.md` + `02-memory.md`（记忆组织）；`01-memory\README.md` + `07-mem-provider\README.md`（provider 生命周期 ABC）；`07-mem-provider\demo\` 下已跑产物（exports 报告，若路径不符则按目录内找） | hermes 四层记忆 + provider 接线笔记 |
| 14:00-15:30 | 对照 D | `06-harnes\learn-claude-code\s08_context_compact\README.md`（四层压缩）+ `s09_memory\README.md` 精读；回看记忆专题 `Agent_Memory_Deep_Dive.md` 的 3.8（Memory Evolve 逆向）与 2.4 | 压缩与记忆机制对照 |
| 15:30-17:00 | 补缺 D | `12-hermes-agent-small\waku\memory\`（retrieval_gate.py + consolidation.py + episodic/semantic/procedural）→ `13-pi-agent\04-sessions.md` + `05-compaction.md`（会话树，轻）→ **LangGraph checkpoint 30min**：`11-langgraph\02-Agentic-Chatbot-using-LangGraph\backend\threads.py` | 三种 runtime 的记忆差异 |
| 17:00-18:45 | 收口 A | **记忆对照表成稿**（模板在本文件下方），含 mem0 列（**诚实标注：概念对照，非源码实证**） | 对照表 |
| 20:00-21:30 | 整合 | 挂总图（会话恢复/记忆注入/压缩节点）+ 面试卡 + 口述自测 | 本文件产出区 |

## 写码挑战②（45min，不查 notebook）

手写三因子打分函数（Python，10-15 行），必须包含：relevance 的 min-max 批内归一化、recency 的指数衰减 exp(-decay×hours)、importance 加权合成。写完与 `04_three_factor_scoring.ipynb` 对照。

## 面试卡（今日自答，次日回填）

1. 记忆三因子（relevance/recency/importance）各是什么公式？为什么"凭什么决定记什么"要用它答？
2. "memory 比 RAG 多两个因子"——这句话怎么解释（写入准入 vs 检索排序）？
3. 分层记忆：什么进上下文（KEY/画像）、什么持久化（日志/向量）、什么淘汰（归档/过期）？举一个生产系统（Memory Evolve 六轨）为例。
4. 上下文压缩 s08 四层怎么做？与"摘要记忆"什么关系？
5. checkpointer/thread_id（LangGraph）与记忆系统是同一件事吗？边界在哪（会话恢复 vs 长期知识）？
6. 记忆投毒/Context Rot 是什么？怎么防？
7. hermes mem-provider 的生命周期（initialize/prefetch/sync_turn/shutdown）里，prefetch 为什么放 turn 前（prompt cache）？

## 晚间复盘 3 问（明早 D3 开场口述）

1. 三因子公式完整背出，并解释 min-max 批内归一化为什么不是全局。
2. 一条消息的一生里，记忆出现在哪 3 个节点？
3. RAG 与记忆都往上下文里塞东西，区别你准备怎么答（预告：明天验证）？

## 今日产出区

### 记忆对照表（内核问题 × 实现）

★ 最后一列 = **dsh-memory-evolve（生产实证）**：你天天在用的宿主记忆插件，代码在 `~/.dsh/profiles/web/node_modules/dsh-memory-evolve/lib/`，已由对话记录预填（源码级证据，10 分钟导览见 `prep0-plugin-memory-arch.md`）。
★ mem0 列：上游 9/8 同步作者详解 `99-My idea\AI Agent 学习指南\01.longterm memory.md`（三套存储/ingestion/retrieval）→ 由"纯概念对照"升级为"作者详解实证"（非源码级，如实标注）。

| 内核问题 | 03-memory | harness s09 | hermes(四层+provider) | waku | pi | LangGraph(checkpoint) | mem0（作者详解实证：三存储/infer/检索） | dsh-memory-evolve（生产实证） |
|---|---|---|---|---|---|---|---|---|
| 什么进上下文 | | | | | | | | 全局 MEMORY/USER + 本项目 KEY（按 git 分支过滤）；**daily/project 永不注入**、工具按需读（index.js renderSnapshot） |
| 什么持久化 | | | | | | | | 纯 md 文件：USER/MEMORY.md + projects\<hash>\{KEY,MEMORY,TODOS}.md + daily\ + SUGGESTIONS.jsonl |
| 什么过期/淘汰 | | | | | | | | ArchiveStore → *-archive.md（memory/user/key + TODO-archive）冷存储，可"移回主记忆" |
| 跨会话恢复 | | | | | | | | 快照注入（live read + 变更检测）；KEY 摘要注入（≤80 字）+ [mem-id] expand 全文 |
| provider 抽象 | | | | | | | | 宿主内六轨直管；可选 git 同步（记忆专属分支）≈ hermes external provider 层 |
| 防投毒/一致性 | | | | | | | | 威胁扫描（中英注入正则 store.js:422）+ subagent 禁写全局轨 + 目录锁 withLock + tmp-rename 原子写 |
| 人确认/HITL | | | | | | | | KEY/全局/技能创建 → SuggestionQueue(SUGGESTIONS.jsonl) → 记忆 Tab /memory_review 采纳 |

**面试一句话答法（可直接背）**："我日常用的宿主记忆系统就是 Hermes-style 分层实现：注入层只放慢变轨（用户画像/项目关键记忆），流水日志永不注入、按需读 + 每轮收尾写；写入有三道闸——投毒扫描、人确认队列、来源分级（subagent 不能碰全局轨）。"

### 面试卡答案 / 口述记录
（待填）
