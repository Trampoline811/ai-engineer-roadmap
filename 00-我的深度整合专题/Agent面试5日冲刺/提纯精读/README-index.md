# 提纯精读（P 文档）与模块专题 —— 索引与规范（v2·六层栈版）

> **方法**（用户提出，v1 确立、v2 扩展）：**"多文件散读"改为"粗读 → 筛选提纯 → 精读提纯文档"**。
> 散源文件只在文档标注 `↳深挖` 时按需回读；不再直接啃原始文件夹。
>
> **v2 更新（2026-09-18）**：
> 1. **主轴换六层栈（L1→L6）**，日程重锚 **D1=9/18 … D5=9/22**（原 9/9-9/13 实际未启动）；
> 2. **凡"一个文件夹下多个子文件"的模块，先做「模块专题」再精读**（仿 `00-我的深度整合专题` 下的 `*_Deep_Dive.md` 三层格式）。P 文档保留给**对照/收口类**（跨系统横向对照），模块专题用于**单模块纵向深挖**；
> 3. 所有文档里的文件引用一律写**仓库根相对全路径**，并由 `核验脚本.py` 校验（见冲刺 `README.md` §5）。

## 规范（每篇文档的骨架）

```
# P{n} {主题}（提纯版）/ {主题} 深度解析
> 生成日期 / 用途(D几精读) / 阅读法（先 5 分钟速查卡 → 概念层 → 实现层按需）
## 📍 本页定位与蒸馏溯源（每篇必写，先回答"我在哪、从哪来、为什么这样提纯"）
   ① 在整体计划中的位置：对应 Day / 六层栈位置 / 配套文档 / 建议读法
   ② 被蒸馏文档明细：文档总数 + 主干清单（每个源 1 行：内容→提炼点）
   ③ 蒸馏理由与方法（100-150 字）：每个文档讲什么 → 连在一起说明什么 → 因此怎么提纯——知其然且知其所以然
## 0 定位与源文件清单        （源路径 ↔ 提炼点 ↔ ↳深挖?）
## 1 概念层                 （统一类比 + 全景图/表 + 因果链 + 面试怎么说）
## 2 实现层                 （结构提纯：关键函数/协议/伪代码 + 为什么）
## 3 工程层                 （避坑清单 ≥10 条 + 生产取舍 + 决策树）
## 📋 每层末尾面试卡片
## 5 分钟速查卡             （终极压缩，可打印）
```

## 状态表 · A. P 文档（对照/收口类）

| 文档 | 覆盖 | 层 | 对应 Day | 状态 |
|---|---|:--:|:--:|---|
| `P1a-循环与五范式提纯.md` | 09-loop 三文 + 01-Agent 六范式 + ReAct 代码结构 | L4a | D1 | ✅ 460 行（含📍溯源节） |
| `P1b-Harness生命周期提纯.md` | learn-claude-code s01-s20 重组为会话生命周期 | L4a | D1 | ✅ 425 行（含📍溯源节） |
| `P2-记忆实现对照提纯.md` | 03-memory 四本 + harness s08/s09 + hermes 四层与 provider + waku 四层/gate + pi 会话树 + LangGraph checkpoint + mem0 + dsh-memory-evolve **跨系统对照表** | L2 | **D2** | ✅ 就绪（572 行） |
| `P3-RAG主线提纯.md` | 02-RAG simple/basic/high_level 五范式 + Agentic RAG + 幻觉治理（评测复用 RAG 评估专题） | L2 | **D2** | 待产（D2 白天直接用模块专题替代，P3 可视时间降级为可选） |
| `P4-多智能体与框架提纯.md` | multi-agent 模式 + 框架选型矩阵 + runtime 对照 | L4b | **D4** | 待产（已被 `Runtime_Five_Way_Deep_Dive.md` 大量覆盖，剩余部分并入 D4 产出区） |
| `P5-评测CICD概念提纯.md` | Agent eval + CICD 突击 + LLM 概念卡 + model-route | L5 | **D5** | 待产（评测部分已由 `Observability_Eval_Deep_Dive.md` 承担） |

## 状态表 · B. 模块专题（单模块纵向深挖，v2 新增）

| 专题 | 覆盖源 | 层 | 对应 Day | 状态 |
|---|---|:--:|:--:|---|
| `00-我的深度整合专题\循环工程深度解析\Loop_Engineering_Deep_Dive.md` | `09-loop-engineering\` 三文（484+445+424） | L4a | **D1** | ✅ 567 行（📍溯源节在 L11） |
| `00-我的深度整合专题\Agent面试5日冲刺\运行时选型-LangGraph-vs-Hermes.md` | `08-hermes-agent\09-lang-serial-not`、`01-arch`、`12-hermes-agent-small`、`13-pi-agent`、`14-deepseek-harness`、`11-langgraph\02` | L4 | **D4** | ✅ 199 行（回答"同层二选一 + 语言门槛"） |
| `00-我的深度整合专题\推理与路由深度解析\Model_Route_Deep_Dive.md` | `05-model-route\` 11 模块 + `07-llm_from_scrach`（注意力/KV cache/MoE/GRPO） | L1 | **D3** | ✅ 就绪（623 行，首版 992 已压缩） |
| `00-我的深度整合专题\运行时选型深度解析\Runtime_Five_Way_Deep_Dive.md` | `11-langgraph`(3 项目) + `08-hermes-agent` + `12-hermes-agent-small` + `13-pi-agent` + `14-deepseek-harness` + `04-multiagent` | L4 | **D4** | ✅ 就绪（616 行） |
| `00-我的深度整合专题\观测与评测深度解析\Observability_Eval_Deep_Dive.md` | `08-hermes-agent\03-eval` + `12-hermes-agent-small\waku\ops`+`evals` + `02-RAG\04_RAG_Evaluation` + `99-My idea\Agent eval` + `10-CICD` + `05-model-route` 07/08/09/11 | L5 | **D5** | ✅ 就绪（546 行） |

## 生产节奏（每日闭环的一部分）

- **模块专题**（400–620 行）与 **P 对照文档**（300–480 行）由"蒸馏员"子代理粗读源文件后落盘，主代理复核质量与路径真实性。
- 每晚打卡后产**次日**要用的文档 → 每天早晨一定 ready。
- 文档是**主阅读**；day{n} 时间盒里凡标注源文件处，优先读对应文档，`↳深挖` 才回源。

## 与已有专题的关系（不重造）

- 记忆：`00-我的深度整合专题\Agent记忆深度解析\Agent_Memory_Deep_Dive.md`（1565 行）已覆盖 03-memory 四 notebook → **P2 只补实现对照**，不重做。
- RAG 评估：`00-我的深度整合专题\RAG评估深度解析\RAG_Evaluation_Deep_Dive.md`（2861 行）已完备 → D2/D5 **直接复用**。
- 插件源码速览：`00-我的深度整合专题\Agent面试5日冲刺\prep0-plugin-memory-arch.md`（29 行）→ D2 预习；插件源码在仓库外 `~/.dsh/profiles/web/node_modules/dsh-memory-evolve/lib/`。

## 转正规则（面试后可选）

压缩版（P 文档/模块专题）面试后可按 `00-我的深度整合专题\专题创作指南.md` 扩写成完整 1500+ 行专题（补计算层细节、公式三版本演进、诊断决策树）。
