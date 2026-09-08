# D5 — 评测闭环 + 工程收口 + 概念补漏

> 日期：____ ｜ 今日面试锚（A）：
> 📖 主阅读（提纯版）：先读 `提纯精读\P5-评测CICD概念提纯.md` + `99-My idea\Agent eval\01-eval.md`，源文件按需深挖**"怎么评测一个 agent？评测怎么进 CI/CD？" + 全仓收口**
> 主轴位置：评测闭环层（总图最后一层）+ 5 天成果合并

## 时间盒（≈8.5h 有效学习）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 08:30-09:00 | 主动回忆 | 口述 D4 复盘 3 问 + 回看总图全貌 | 3 答记录 |
| 09:00-10:30 | 评测演进 | `99-My idea\Agent eval\01-eval.md`（四维：Capability/Reliability/Cost/Safety）+ hermes `08-hermes-agent\03-eval\`（notes/README/demo 产物）+ waku `12-hermes-agent-small\waku\ops\`（tracing/judge/release_gate 浏览）+ `04-multiagent\multi-agent-arch\09_agent_ops_langsmith_demo.ipynb` 讲义 | "RAG 评测 → Agentic eval"演进卡 |
| 10:30-12:30 | CICD 突击 | `10-CICD\cicd学习大纲.md` + `01-basic` + `02-pytest` + `03-gitlab-ci` + `08-review`（各子目录 README/说明，**背题**；其余 5 组跳过） | CICD 背题卡 |
| 14:00-15:30 | 概念补漏 | `07-llm_from_scrach\part_1\README.md`（注意力/tokenizer 概念，快）+ `part_9\GRPO_TRAINING_EXPLANATION.md`（291 行中文详解，1h） | **一页演进卡**：SFT→RM→PPO→GRPO + KV cache + MoE 一句 |
| 15:30-16:30 | 路由+可选 | `05-model-route\README.md`（自带面试清单→代码映射）+ 01/08 代码读；可选 `14-deepseek-harness\01.arch.md` 30min（tool vs skill / code vs config 话术） | 路由与选型一句话卡 |
| 16:30-17:30 | 收口 | 合并 5 天全部图/表 → **《面试总纲 v1》** + 可讲项目叙事清单（从真正跑通的 demo 里挑 2-3 个） | 总纲 |
| 19:30-21:00 | 总演练 | **模拟面试 60-75min**（自问自答/录音）+ 5 分钟速查卡通背 | 模拟记录 |

## 面试卡（今日自答）

1. 评测一个 RAG 系统 vs 评测一个 agent，有什么本质区别？（确定性 vs 轨迹/工具链）
2. Agent eval 四维（Capability/Reliability/Cost/Safety）怎么落地成指标？
3. 评测怎么进 CI/CD？（数据集→门禁阈值→回归→trace 可观测；Faithfulness≥0.8 这类门禁）
4. pytest + GitLab CI 的最小闭环怎么搭？排查 CI 挂了的思路？
5. GRPO 与 PPO 的核心区别一句话？（组内均值基线替代 value head）DeepSeek-V3/R1 相关话题可引申。
6. MoE 一句话？（top-k 稀疏专家路由 + 负载均衡损失）KV cache 为什么省算力？
7. 模型路由：什么时候值得 route_by_complexity？（成本 vs 质量）

## 晚间收口（面试总纲 v1 结构建议）

1. 三条主线口述稿：一条消息的一生 / 记忆与上下文 / RAG 与评测。
2. 两张王牌表：记忆对照表、框架选型矩阵。
3. 两个可讲项目叙事：每个 = 背景→我做了什么→指标/评测→踩坑（各 2 分钟版 + 5 分钟版）。
4. 薄弱点清单（写给自己）：D6+ 只补这些。

### 面试总纲 v1 / 模拟面试记录
（待填）

### 一页演进卡（LLM 概念）
（待填：tokenizer→attention→预训练→SFT(masked loss)→RM(BT)→PPO→GRPO(组内均值)；KV cache；MoE 一句）

### CICD 背题卡
（待填：什么是 CI/CD、pytest 用法、gitlab-ci 关键段、排查思路）
