# D3 — L1 推理 + L3 动作：模型·引擎·路由 + 协议·工具

> **日期：2026-09-20（周日）** ｜ 覆盖层：**L1 推理 ＋ L3 动作**
> **今日面试锚（A）**：① "模型怎么选 / 怎么跑 / 怎么路由 / 怎么控成本？" ② "工具协议有几种变体？MCP 到底是什么？" ③ "工具有副作用——权限决策怎么做？"
> **主阅读（提纯版）**：`00-我的深度整合专题\推理与路由深度解析\Model_Route_Deep_Dive.md`（今日新增，L1）
> L3 用现有散件收口（工具协议三变体 + MCP + 权限/沙箱），可用 `提纯精读` 线索快速定位

---

## 📎 本日文件核验（逐路径实测）

| 路径 | 状态 | 行数/大小 |
|---|:--:|---|
| `00-我的深度整合专题\推理与路由深度解析\Model_Route_Deep_Dive.md` | 🆕 今日生成 | 400–600 |
| `05-model-route\README.md` | ✅ | 52（**自带"面试清单→代码映射"，先读它**） |
| `05-model-route\01\main.py` + `01\breaker\circuit_breaker.py` | ✅ | 60 / 61 |
| `05-model-route\02\main.py` + `02\cache\exact_cache.py` | ✅ | 55 / 19 |
| `05-model-route\03\main.py` + `03\runtime\two_level_cache.py` | ✅ | 81 / 20 |
| `05-model-route\05\main.py` + `05\pipeline\fallback.py` + `router.py` | ✅ | 50 / 58 / 17 |
| `05-model-route\06\main.py` + `06\billing\reconcile.py` | ✅ | 36 / 35 |
| `05-model-route\10\main.py` + `10\cache\semantic.py` | ✅ | 39 / 37 |
| `05-model-route\11\main.py` + `11\governance\`（before/during/after） | ✅ | 67 / 20+34+27 |
| `05-model-route\04\`（可测试的 stub agent） | ✅ | main.py 22 + tests\test_agent.py 18 |
| `07-llm_from_scrach\part_1\README.md` | ✅ | 7.7 KB（注意力 / tokenizer 概念） |
| `07-llm_from_scrach\part_3\kv_cache.py` | ✅ | 8.8 KB（KV cache 实证） |
| `07-llm_from_scrach\part_5\README.md` | ✅ | 1.9 KB（MoE） |
| `07-llm_from_scrach\part_9\GRPO_TRAINING_EXPLANATION.md` | ✅ | 10.4 KB（中文详解） |
| `01-Agent\00-llm_function_call.py` | ✅ | 334（协议变体①：模型原生 tools JSON） |
| `01-Agent\01-small-llm-function-call-project\README.md` | ✅ | 171（变体①的工程版） |
| `01-Agent\02-Agent_react\agent\tools\__init__.py` + `01-Agent\02-Agent_react\agent\tools\calculator.py` | ✅ | 24 / 36（变体②：注册中心；变体③：手写 Action 文本协议见 `01-Agent\02-Agent_react\agent\prompt.py`） |
| `06-harnes\learn-claude-code\s02_tool_use\README.md` | ✅ | 222 |
| `06-harnes\learn-claude-code\s19_mcp_plugin\README.md` | ✅ | 282 |
| `12-hermes-agent-small\waku\tools\registry.py` + `mcp_client.py` | ✅ | 49 / 100 |
| `12-hermes-agent-small\waku\tools\__init__.py` | ✅ | 61（工具集总装） |
| `05-model-route\08\guard\schema.py` + `05-model-route\08\guard\whitelist.py` + `05-model-route\08\guard\executor.py` | ✅ | 41 / 10 / 27 |
| `08-hermes-agent\05-env\hermes_src\tools\environments\base.py` | ✅ | 959（沙箱抽象基类） |
| `08-hermes-agent\05-env\hermes_src\tools\environments\docker.py` | ✅ | 1460（容器沙箱） |
| `08-hermes-agent\05-env\README.md` | ✅ | 106 |

> ⚠️ `05-model-route` 的 **07 trace / 08 guard / 09 deploy / 11 governance** 会与 D5（L5 观测）重叠：今天只做**导读级**浏览，深挖留 D5。
> ⚠️ `07-llm_from_scrach` **只做概念卡**，不训练（本机纯 CPU 无 GPU，`part_2\train.py` 别跑）。

---

## ⏱ 时间盒（≈8.5h）

| 时段 | 动作 | 具体内容 | 产出 |
|---|---|---|---|
| 08:30-09:00 | **主动回忆** | 口述 D2 三问（不看笔记） | 3 答记录 |
| 09:00-11:00 | **L1 实证 D** | `推理与路由深度解析\Model_Route_Deep_Dive.md` 全读；**挑 4 个模块真跑**（各自目录下的 main.py 直接 `python` 跑，看打印输出）：`05-model-route\01\main.py`（熔断重试）、`05-model-route\05\main.py`（路由+回退+计费）、`05-model-route\10\main.py`（语义缓存）、`05-model-route\11\main.py`（治理三段式） | L1 选型卡（引擎/路由/成本） |
| 11:00-12:30 | **L1 概念 M** | `07-llm_from_scrach\part_1\README.md`（注意力/tokenizer）→ `part_3\kv_cache.py` → `part_5\README.md`（MoE）→ `part_9\GRPO_TRAINING_EXPLANATION.md`（1h，重点） | **一页演进卡**：tokenizer→attention→SFT→RM→PPO→GRPO + KV cache + MoE |
| 14:00-15:30 | **L3 协议 M** | 工具协议三变体对照：`01-Agent\00-llm_function_call.py`（原生 tools JSON）↔ `01-Agent\01-small-llm-function-call-project\README.md` ↔ `01-Agent\02-Agent_react\agent\tools\__init__.py` + `01-Agent\02-Agent_react\agent\prompt.py`（手写 Action 文本协议）；再看 `06-harnes\learn-claude-code\s02_tool_use\README.md` | **工具协议对照表** |
| 15:30-16:15 | ⚔️ **写码挑战③** | 闭卷写一个工具的 schema + 分发函数（见下） | 差异点笔记 |
| 16:15-17:30 | **L3 权限与 MCP** | MCP：`06-harnes\learn-claude-code\s19_mcp_plugin\README.md` + `12-hermes-agent-small\waku\tools\mcp_client.py` + `12-hermes-agent-small\waku\tools\registry.py`；权限：`05-model-route\08\guard\schema.py`（契约）+ `05-model-route\08\guard\whitelist.py`（白名单）+ `05-model-route\08\guard\executor.py`（执行守卫）；沙箱阶梯：`08-hermes-agent\05-env\README.md` + `08-hermes-agent\05-env\hermes_src\tools\environments\base.py`（读类结构） | **权限决策树** + 沙箱阶梯表 |
| 17:30-18:45 | **收口 A** | L1 选型卡成稿 + 工具协议对照表成稿 + 权限决策树成稿；回填 D1 六层栈总纲表的 **L1 / L3 两行** | 三张卡 |
| 20:00-21:30 | **整合** | 挂总图（LLM 调用节点 + 工具节点）+ 面试卡 8 问 + 口述自测 | 本文件产出区 |

---

## ⚔️ 写码挑战③（45min，闭卷）

不看代码写两段东西：

```python
# 1) 一个工具的 schema（要求：名字用清晰动词、描述含参数含义与示例、参数类型严格）
# 2) 工具分发函数：从模型输出里取出 tool_call → 校验参数 → 查白名单 → 执行 → 回填 tool_result
```

写完对照 `01-Agent\02-Agent_react\agent\tools\__init__.py`（注册表写法）与 `05-model-route\08\guard\`（校验+白名单+执行三段式），把差异写进笔记。差异通常出现在：**参数校验位置**、**白名单判定时机**、**错误信息是否可行动**。

---

## 🎴 面试卡（今日自答，晚间口述）

1. L1 层你到底要定哪几件事？（开放权重 vs 闭源 / 本地引擎 vs 并发引擎 / 路由 / 按任务分层 / 兜底）
2. Ollama+llama.cpp 与 vLLM/SGLang 的分工是什么？为什么"重复前缀"场景会提 SGLang？
3. LiteLLM 这类路由层解决什么？（Routing / Retries / Budgets / Fallbacks / Observability Hooks）
4. **什么时候不该上路由/网关？**（提示：异质模型间提示词不一致会导致语义漂移）
5. 按任务分层用模型怎么分？"4B 小模型做固定 task"的判据是什么？
6. 工具协议三变体各自的 trade-off？（原生 tools JSON / 注册中心 / 手写 Action 文本协议）
7. MCP 是什么形状？（tools / resources / prompts 三原语；stdio → Streamable HTTP；OAuth 2.1）为什么说"MCP 底层还是 tool call"？
8. 工具权限决策怎么做？prompt injection 为什么能藏在检索内容里？

---

## 🌙 晚间复盘 3 问（明早 D4 开场口述）

1. L1 的"分层配置"用一句话讲清（成本 vs 智商）。
2. 工具协议三变体，你推荐哪个、为什么？
3. 权限决策树四分支背出来。

---

## 今日产出区

### ① L1 选型卡

| 决策点 | 候选 | 我选什么 | 为什么不选另一个 | 本仓库实证 |
|---|---|---|---|---|
| 权重来源 | 开放权重 / 闭源 API | | | |
| 本地引擎 | Ollama·llama.cpp / vLLM·SGLang | | | `05-model-route\README.md` |
| 路由 | 自研 / LiteLLM / 不上 | | | `05-model-route\05\pipeline\router.py` |
| 缓存 | 精确 / 语义 / 两级 | | | `05-model-route\10\cache\semantic.py` |
| 回退 | fallback + retry + 熔断 | | | `05-model-route\01\breaker\circuit_breaker.py` |
| 成本治理 | before / during / after | | | `05-model-route\11\governance\` |

### ② 工具协议对照表

| 变体 | 谁定义协议 | 解析可靠性 | 出错时怎么办 | 出处 | 适用场景 |
|---|---|---|---|---|---|
| 模型原生 tools JSON | | | | `01-Agent\00-llm_function_call.py` | |
| 注册中心 | | | | `01-Agent\02-Agent_react\agent\tools\__init__.py` | |
| 手写 Action 文本协议 | | | | `01-Agent\02-Agent_react\agent\prompt.py` | |

### ③ 权限决策树

```
只读公开页？ ──是→ 当不可信文本（prompt injection 可能藏在检索内容里）
   └─否→ 会改外部状态？ ──是→ 人审批再执行（HITL，注意幂等键）
            └─否→ 要跑代码？ ──是→ 沙箱/容器
                     └─否→ 最小权限调用
（待填：每一支在本仓库的对应实现文件）
```

### ④ 一页演进卡（LLM 概念）

（待填：tokenizer→attention→预训练→SFT→RM→PPO→GRPO(组内均值基线)；KV cache 为什么省算力；MoE top-k 稀疏 + 负载均衡）

### ⑤ 面试卡答案 / 口述记录

（待填）
