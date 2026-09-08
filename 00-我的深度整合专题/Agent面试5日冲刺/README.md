# Agent 面试 5 日冲刺（从使用者到建造者）

> 目标：面试前用 5 天把本仓库从"作者的线性教学序"翻转为"使用者的面试冲刺序"，**查漏补缺 + 内核串联**，每天 8-9h。
>
> **MDA 类比（本计划第一原则）**：面试那天 = **A**（能在白板画系统 / 答系统设计 / 讲出验证过的项目叙事）；跑通的 demo 与亲手填的对照表 = **D**；循环 / 记忆 / 上下文 / runtime 内核 = **M**（按需深挖，不线性刷）。
>
> **基线（用户确认，2026-09）**：D1 从明天开始，面试在 D6 或更后；动手基线 = 能读懂代码 → 每日含 45-60min **写码渐进挑战**；缺口优先级 5 线；产出 = 混合型（上午读+写卡，下午跑必要 demo）。

## 目录文件

| 文件 | 内容 | 状态 |
|---|---|---|
| `README.md` | 本总纲：主轴 / 贯穿线 / 覆盖矩阵 / 科学机制 / 避坑 / 决策记录 | 定稿 |
| `day1-loop-harness.md` | D1 循环与 Harness：生命周期总图 v1 + 五范式对比表 | 待填 |
| `day2-memory.md` | D2 记忆与上下文：记忆对照表（补 mem0 列） | 待填 |
| `day3-rag.md` | D3 RAG 主线：RAG 质量决策树 + 边界论述 | 待填 |
| `day4-multiagent.md` | D4 多智能体 + 框架：框架选型矩阵 + runtime 对照 | 待填 |
| `day5-closeout.md` | D5 评测闭环 + 收口：面试总纲 v1 + 模拟面试 | 待填 |
| `prep0-plugin-memory-arch.md` | D1 晨/D2 预习：dsh-memory-evolve 源码速览（10-15min） | 就绪 |

## 打卡协议（与 AI 助手的每日闭环）

- **每天早晨**：AI 助手发"今日卡"= 昨日复盘 3 问 + 当日清单（对应各 day 文件）。
- **每天晚上**：把复盘 3 问的回答口述/打字给 AI；产出填进当日 day 文件。
- **系统侧闭环**：dtodo 已固化 D1-D5（due 9/9-9/13，2026-09-08 用户休整顺延 1 天）；技能 `daily-sprint-coach`（设置面板采纳后）保证新会话按同一协议推进；每晚收尾给一句情绪反馈（顺/卡/难在哪），D6 可做"5 日学习分析"。
- 5 天结束后合并出《面试总纲 v1》，用于 D6+ 缓冲期。

## 主轴：一条用户消息的一生（每天往上叠一层）

```
用户消息
   │
   ▼
[入口 / 会话恢复]  ←──── D2: checkpointer(thread_id) / 记忆跨会话
   │
   ▼
[System Prompt 组装]  ←── D1: s10 组装原则 + s07 技能按需注入
   │                       D2: 记忆冻结快照 / mem-provider prefetch 注入
   ▼
┌────────────────────────────────────────────────┐
│  主循环（ReAct：观察→思考→行动）                 │
│    │                                            │
│    ▼                                            │
│  [LLM 调用] → 解析输出                          │
│    ├─ 要调工具? ──→ [工具注册表 s02]            │
│    │                 ├─ 权限判定 s03            │
│    │                 ├─ 工具执行（含 MCP s19）  │
│    │                 └─ tool_result 回填        │
│    └─ 不要? ──→ [生成最终答案]                  │
│                                                  │
│  上下文膨胀 → 四层压缩 s08（D2 细讲）            │
└────────────────────────────────────────────────┘
   │
   ▼
[停止 / 返回]
   │
   ▼
[状态写入：记忆 / 线程存储]（D2）
   │
   ▼
[协同层] subagent(s06) / teams(s15) / 多智能体编排（D4）
   │
   ▼
[评测与可观测] eval / trace / 门禁（D3 指标 + D5 收口）
```

## 贯穿线清单（面试"看见共性"的弹药）

| 贯穿线 | 仓库出处 | 计划处理 |
|---|---|---|
| ReAct 循环 | 01-Agent(ReAct/Plan-Execute/Reflexion/LATS) → 06 s01 → hermes 主循环 → 09-loop 三文 → waku loop(~95行) → LangGraph | D1 建立，D4 源码对照收口 |
| 工具协议三变体 | 原生 tools JSON / 注册中心 / 手写 Action 文本协议 → s02 → MCP s19 | D1 |
| 上下文管理 | s10 组装 / s08 四层压缩 / hermes 冻结快照+prefetch / 记忆各层 / RAG 注入 | D1 起逐层挂 |
| 记忆分层与淘汰 | 03-memory 四本 / s09 / hermes 四层记忆 / waku gate+consolidation / pi 会话树 / LangGraph checkpoint | D2 |
| 评测闭环 | RAG 四指标+四象限 / hermes 03-eval / waku ops / 99-My idea Agent eval / langsmith / CICD 门禁 | D3 起 + D5 收口 |
| 路由与成本 | 05-model-route / Adaptive RAG / 多向量库路由 / Hub-Spoke / 缓存 | D5 轻补 |

## 五日总览

| 天 | A（当天能答的面试题锚） | 主轴位置 | 主产出 |
|---|---|---|---|
| D1 | 一条消息的一生 / 手写 ReAct | 循环内核 + Harness | 生命周期总图 v1 + 五范式对比表 |
| D2 | 凭什么决定记什么/忘什么 | 状态与记忆 | 记忆对照表（含 mem0 列） |
| D3 | 高级 RAG / 指标低了怎么修 | 上下文注入 | RAG 质量决策树 + RAG vs 记忆边界卡 |
| D4 | 多智能体 vs 单 agent / 框架选型 | 协同层 + runtime 对照 | 框架选型矩阵终版 |
| D5 | 怎么评测 agent / CICD / 概念补漏 | 评测闭环 + 收口 | 面试总纲 v1 + 项目叙事 + 模拟面试 |

## 全仓覆盖矩阵（5 日内完成整个项目的证据）

| 模块 | 处理日 | 深度 | 说明 |
|---|---|---|---|
| 00-大纲 | D1 启动 | 浏览 10min | 作者序仅作对照，不走 |
| 00-我的深度整合专题 | 全程 | 复用+产出 | 记忆专题→D2；RAG评估专题→D3；本目录即产出 |
| 01-Agent | D1 | ReAct 精读；其余 README | 五范式对比表；`03-Reﬂexion` 目录名含特殊字符 ﬂ，复制原路径 |
| 02-RAG | D3 | 读+跑（--mock/离线） | simple→basic→high→Agentic RAG→评测 |
| 03-memory | D2 | 跑 2 本（离线） | 三因子纯 stdlib、长时记忆 mock 向量 |
| 04-multiagent | D4 | 讲义精读（无 key 只读） | 模式 01.1-01.4 + supervisor + 框架对比 |
| 05-model-route | D5 | 1h 浏览 | README 自带面试清单→代码映射 |
| 06-harnes | D1(+D2) | s01/02/03/10 精读；s08/09 留给 D2；其余 README | learn-claude-code s01-s20 骨架 |
| 07-llm_from_scrach | D5 | 概念卡 1.5-2h | part_1 + part_9(GRPO)，其余跳过 |
| 08-hermes-agent | D2+D4 | 读笔记 | 源码不在本机，hermes-study 剪枝不可跑，勿打断点 |
| 09-loop-engineering | D1 | 01 精读 + 02/03 浏览 | 四层演进口述 |
| 10-CICD | D5 | 4 组背题 | 01-basic/02-pytest/03-gitlab-ci/08-review |
| 11-langgraph | D2(概念)+D4(项目) | chatbot 精读+跑 | 最贴环境：DeepSeek+BGE+SQLite threads |
| 12-hermes-agent-small(waku) | D4 晚 | 读（有余力 uv 跑） | 四支柱目录对照 |
| 13-pi-agent | D4 晚 | 读 30min | Core/Interactive、会话树 |
| 14-deepseek-harness | D5 可选 | 30min | tool vs skill / code vs config 话术 |
| 99-My idea | 全程 | 早晚背诵 | memory 01/02 问答稿；**AI Agent 学习指南（00.guide + 01.longterm memory.md Mem0 详解，9/8 上游同步）→ D2**；D5 用 Agent eval |

## 学习科学机制（为什么这么排）

1. **主动回忆**：每天开场 30min 闭卷复述昨日（不是重读）。
2. **交错练习**：相邻两天互为"同一内核的不同抽象层"（D1 harness↔D2 s08/s09；D2 记忆↔D3 RAG 注入；D4 runtime↔D1 loop），强制迁移。
3. **生成式产出**：每天亲手写图/表/卡（对照表、决策树、矩阵），费曼式"写出来才算会"。
4. **间隔重复**：D1 卡片在 D3/D5 晨间复测；`99-My idea/memory/01-02.md` 问答稿早晚各背 10min。
5. **写码渐进**（动手弱→每日 45-60min）：D1 抄写→D2 填空重写→D3 伪代码→D4 真改小图→D5 白板口述。
6. **时间盒与休息**：90min 一盒；饭后/茶歇硬休；每天 ≤9h；睡前 30min 不学新知识（睡眠巩固是学习的一部分）。

## 环境约束与避坑（勘察实锤）

- ❌ Docker 未启动 → graph_rag(Neo4j)、sandbox 类只读概念，不跑。
- ❌ hermes 完整源码不在本机 → 08 只读笔记与已跑产物，不打断点、不 import hermes-study。
- ✅ 离线/低成本可跑：三因子 notebook（纯 stdlib）、02_long_term_memory（mock 向量）、06-Agentic RAG demo（--mock）、LangGraph chatbot（BGE 本地 + DeepSeek key）、waku（uv + 一把 key）。
- ✅ 诚实标注：mem0 列 = 仓库无 mem0 源码，但上游 2026-09-08 同步进作者详解（`99-My idea\AI Agent 学习指南\01.longterm memory.md`，684 行）→ 由"纯概念对照"升级为"作者详解实证"；面试被追问就说"我读过 Mem0 架构的详细拆解 + 在 hermes mem-provider 上验证过接线模式"。
- ⚠️ `01-Agent\03-Reﬂexion` 目录名含特殊连字字符 ﬂ（U+FB02），引用时复制原路径。

## 决策记录

| # | 决策 | 结论（2026-09 拍板，默认采纳） |
|---|---|---|
| 1 | 产物落点 | 建 `00-我的深度整合专题\Agent面试5日冲刺\`，每日产出入 day 文件 |
| 2 | 两篇 P0 新专题 | Agentic RAG 做压缩版；Multi-Agent 用选型矩阵替代（时间不够的全文稿留面试后） |
| 3 | 打卡闭环 | AI 每日早晨发今日卡，晚间回 3 答，产出入文件 |
| 4 | 插件能力进冲刺（2026-09-07 已执行） | dtodo 固化 D1-D5 日程；技能 `daily-sprint-coach`（待设置面板采纳）；每日情绪反馈闭环；D2 对照表新增 dsh-memory-evolve 生产实证列；`prep0-plugin-memory-arch.md` 源码速览 |
| 5 | 顺延与 mem0 调优（2026-09-08） | 用户休整 → D1-D5 全部顺延 1 天（9/9-9/13，dtodo/索引已同步）；上游同步进 `99-My idea\AI Agent 学习指南\01.longterm memory.md`（Mem0 详解 684 行）→ mem0 列升级为"作者详解实证"并纳入 P2 蒸馏范围 |

## D6+ 缓冲期（面试前剩余天只做三件事）

1. 简历项目叙事打磨（基于 5 天里真正跑通的 2-3 个 demo）。
2. 二次模拟面试（换题自问自答）。
3. 按《面试总纲 v1》薄弱点回炉，不学新知识。
