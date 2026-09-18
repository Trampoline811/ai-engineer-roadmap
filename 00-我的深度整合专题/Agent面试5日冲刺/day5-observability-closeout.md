# D5 — L5 观测 + L6 界面 + 总收口

> **日期：2026-09-22（周二）** ｜ 覆盖层：**L5 观测（Trace·Eval·护栏）＋ L6 界面 ＋ 六层栈总收口**
> **今日面试锚（A）**：① "怎么评测一个 agent？评测怎么进 CI？" ② "出错了怎么查"（**失败归因链**）③ "六层栈逐层讲"（今天必须能完整讲一遍）
> **主阅读（提纯版）**：`00-我的深度整合专题\观测与评测深度解析\Observability_Eval_Deep_Dive.md`（今日新增）＋`99-My idea\Agent eval\01-eval.md`＋既有 `RAG评估深度解析\RAG_Evaluation_Deep_Dive.md`（复习）

---

## 📎 本日文件核验（逐路径实测）

| 路径 | 状态 | 行数/大小 |
|---|:--:|---|
| `00-我的深度整合专题\观测与评测深度解析\Observability_Eval_Deep_Dive.md` | 🆕 今日生成 | 380–560 |
| `99-My idea\Agent eval\01-eval.md` | ✅ | 267（四维：Capability / Reliability / Cost / Safety） |
| `08-hermes-agent\03-eval\README.md` | ✅ | 228 |
| `08-hermes-agent\03-eval\notes\02_logging_trace.md` / `03_eval_harness.md` | ✅ | 229 / 283 |
| `08-hermes-agent\03-eval\demo\README.md` | ✅ | 393 |
| `08-hermes-agent\03-eval\demo\exports\eval_run\`（4 份产物） | ✅ | case_scores / invariants / trace_rca / session_log_slice |
| `12-hermes-agent-small\waku\ops\release_gate.py` / `tracing.py` / `judge.py` | ✅ | 114 / 167 / 101 |
| `12-hermes-agent-small\evals\deterministic\README.md` | ✅ | 86（该目录 30 个确定性测试） |
| `12-hermes-agent-small\docs\benchmarks.md` | ✅ | 445 |
| `02-RAG\04_RAG_Evaluation\lesson2_rag_metrics\README.md` | ✅ | 150（＋`diagnostic_report.html`） |
| `05-model-route\07\trace\collector.py` | ✅ | 58 |
| `05-model-route\08\guard\schema.py` | ✅ | 41 |
| `05-model-route\09\deploy\canary.py` / `blue_green.py` | ✅ | 14 / 23 |
| `05-model-route\11\main.py` | ✅ | 67（before / during / after） |
| `10-CICD\cicd学习大纲.md` | ✅ | 251 |
| `10-CICD\01-basic\01-ci-cd-定义.md` | ✅ | 362 |
| `10-CICD\02-pytest\README.md` | ✅ | 48（＋`10-CICD\02-pytest\demos\` 5 组） |
| `10-CICD\03-gitlab-ci\03-标准流水线流程.md` | ✅ | 249 |
| `10-CICD\08-review\02-高频面试题.md` | ✅ | 49 |
| `11-langgraph\02-Agentic-Chatbot-using-LangGraph\frontend\hitl.py` / `11-langgraph\02-Agentic-Chatbot-using-LangGraph\frontend\chat.py` | ✅ | 183 / 207 |
| `12-hermes-agent-small\waku\gateway\cli.py` / `12-hermes-agent-small\waku\gateway\telegram.py` / `12-hermes-agent-small\waku\gateway\voice.py` | ✅ | 88 / 122 / 360 |
| `14-deepseek-harness\01.arch.md` | ✅ | 296（tool vs skill / code vs config 话术） |
| `00-我的深度整合专题\Agent面试5日冲刺\README.md` | ✅ | v2 六层栈总纲 |

---

## ⏱ 时间盒（≈8.5h，最后一段留给模拟面试）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 08:30-09:00 | **主动回忆** | 口述 D4 三问 + 回看六层栈总图全貌 | 3 答记录 |
| 09:00-10:30 | **L5 概念 M** | `观测与评测深度解析\Observability_Eval_Deep_Dive.md` 概念层 + 实现层；`99-My idea\Agent eval\01-eval.md`（四维） | "RAG 评测 → Agentic eval" 演进卡 |
| 10:30-12:30 | **L5 实证 D** | hermes：`08-hermes-agent\03-eval\README.md` + `08-hermes-agent\03-eval\notes\02_logging_trace.md` + `08-hermes-agent\03-eval\notes\03_eval_harness.md` + `08-hermes-agent\03-eval\demo\README.md` + 4 份已跑产物；waku：`12-hermes-agent-small\waku\ops\release_gate.py` + `12-hermes-agent-small\waku\ops\tracing.py` + `12-hermes-agent-small\waku\ops\judge.py`；`12-hermes-agent-small\evals\deterministic\README.md` | **失败归因链 8 步**卡 + 门禁卡 |
| 14:00-15:00 | **L5 补漏** | `05-model-route\07\trace\collector.py`（trace 落盘）+ `05-model-route\08\guard\`（护栏三件套）+ `05-model-route\09\deploy\canary.py`（灰度）+ `05-model-route\11\main.py`（治理三段式） | 观测/发布/治理三件套笔记 |
| 15:00-16:00 | **CI/CD 突击** | `10-CICD\cicd学习大纲.md` + `10-CICD\01-basic\01-ci-cd-定义.md` + `10-CICD\02-pytest\README.md` + `10-CICD\03-gitlab-ci\03-标准流水线流程.md` + `10-CICD\08-review\02-高频面试题.md`（**背题**；其余 5 组跳过） | CICD 背题卡 |
| 16:00-16:45 | **L6 界面** | `11-langgraph\02-Agentic-Chatbot-using-LangGraph\frontend\hitl.py` + `11-langgraph\02-Agentic-Chatbot-using-LangGraph\frontend\chat.py`（流式 + 人审按钮）；`12-hermes-agent-small\waku\gateway\cli.py` + `12-hermes-agent-small\waku\gateway\telegram.py` + `12-hermes-agent-small\waku\gateway\voice.py`（多通道入口） | L6 一句话 + 界面原则卡 |
| 16:45-17:45 | **总收口 A** | 合并 5 天全部图/表 → **《面试总纲 v1》**：三条主线口述稿（一条消息的一生 / 记忆与上下文 / RAG 与评测）+ 两张王牌表（记忆对照表、框架选型矩阵）+ **六层栈逐层答法**；挑 2-3 个**真正跑通**的 demo 写成项目叙事 | 面试总纲 v1 |
| 19:30-21:00 | **总演练** | **模拟面试 60–75min**（自问自答/录音）+ 5 分钟速查卡通背 + 薄弱点清单 | 模拟记录 + D6+ 清单 |

---

## 🎴 面试卡（今日自答）

1. 评测一个 RAG 系统 vs 评测一个 agent，本质区别是什么？（确定性输出 vs **轨迹/工具链**）
2. Agent eval 四维（Capability / Reliability / Cost / Safety）怎么落地成指标？
3. **失败归因链 8 步**背出来，并说每步你用什么观测手段（提示：本仓库 hermes 的 trace RCA 与 waku 的 `show_trace`）。
4. LLM-as-judge 有哪三类系统性偏差？怎么缓解？（位置偏差 / 冗长偏差 / 自我偏好；交换位置 / 参考答案锚定 / 多 judge 投票）
5. 评测怎么进 CI/CD？（数据集 → 门禁阈值 → 回归 → trace 可观测；"应先批准"和"应拒绝"两类用例也要有）
6. **护栏库 ≠ 安全策略**——这句话怎么展开？（护栏只拦输出层；真正的控制层是权限范围 / 沙箱 / 输入校验 / 输出校验 / 密钥隔离 / 审计日志 / 人审）
7. pytest + GitLab CI 的最小闭环怎么搭？CI 挂了你的排查顺序是什么？
8. L6：界面为什么"越简单越好"？"界面不替系统的智力"是什么意思？

---

## 六层栈逐层答法（今天必须能一口气讲完）

```
L1 推理    → 我按"成本 vs 智商"分层配置：固定 task 用本地小模型，复杂推理走大模型，缺一层路由代码就会散落各处（实证：05-model-route 11 个模块）
L2 上下文  → 知识 ≠ 记忆；向量库 ≠ RAG，它只是十步管线第 6 步；先查解析再调检索
L3 动作    → MCP 底层还是 tool call；工具会改世界→只读当不可信文本、改状态先人审、跑代码进沙箱
L4 运行时  → LangGraph 与 Hermes 同层二选一，不叠两套循环；按"业务工作流 vs 终端干活"选
L5 观测    → 没有 traces 你只是在猜；先建 30 条真实用例；失败按归因链查
L6 界面    → 界面是栈顶，不替系统智力；越简单越好
```

（待填：为每一层补上"我为什么**不**选另一个"——这是面试官最想听的部分）

---

## 今日产出区

### ① 失败归因链（8 步，可直接排障/面试）

| # | 现象 | 查什么 | 本仓库对应观测手段 |
|:--:|---|---|---|
| 1 | 答错了 | 先查 RAG | |
| 2 | RAG 解析有问题 | 查文档解析 | |
| 3 | 疑似记忆不准 | 查记忆是否过期 | |
| 4 | 记忆过期 | 查 mem0 / 记忆层 | |
| 5 | 工具失败 | 查工具本身 | |
| 6 | 工具正常 | 查 loop / graph | |
| 7 | loop 也正常 | 查模型 | |
| 8 | 都正常还是错 | 微调适配业务 | |

### ② Agent eval 四维落地表

| 维度 | 落地成什么指标 | 本仓库依据 | 门禁阈值（我定） |
|---|---|---|---|
| Capability | | `99-My idea\Agent eval\01-eval.md` | |
| Reliability | | `12-hermes-agent-small\evals\deterministic\` | |
| Cost | | `05-model-route\06\billing\reconcile.py` | |
| Safety | | `05-model-route\08\guard\` | |

### ③ L6 界面原则卡

（待填：流式 SSE / 引用来源 / 工具过程可见 / 人审按钮 / 会话管理——每项对应本仓库哪个文件）

### ④ 《面试总纲 v1》

（待填）
- 三条主线口述稿：① 一条消息的一生 ② 记忆与上下文 ③ RAG 与评测
- 两张王牌表：记忆对照表（D2）、框架选型矩阵（D4）
- 六层栈逐层答法（上面那张）
- 可讲项目叙事 ×2–3（**只用真跑通的**）：背景 → 我做了什么 → 指标/评测 → 踩坑

### ⑤ 模拟面试记录 + 薄弱点清单（D6+ 只补这些）

（待填）
