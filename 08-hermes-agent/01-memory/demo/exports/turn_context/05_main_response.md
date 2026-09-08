用 `turn_context` 的视角总结如下：

**1. preflight 什么时候触发压缩？**

在每轮组装主模型请求之前，`turn_context` 会做一次 preflight 检查：先粗估当前 `messages` 的总 token 数，如果超过 `context_length * threshold_percent`（例如阈值为 80% 时，就是接近爆窗的 80%），就触发 `context_compressor` 压缩；否则原样发送，不动历史。  
所以它不是在“对话变长就立即改历史”，而是在“预算快撑爆”时才启动，平时通过不修改 messages 来保住 prompt cache。

**2. 压缩后发给主模型的 messages 长什么样？**

压缩会按 `protect_first_n` / `protect_last_n` 把历史切成三段：

- **head**：最前面的几条原样保留，通常是 `system` 消息，里面包含 MEMORY 等稳定事实；
- **middle**：中间大量对话轮次被交给辅助模型生成结构化摘要，不再逐条保留；
- **tail**：最近几条 `user` / `assistant` 消息原样保留，最后一个 user 消息就是当前任务。

middle 被压成 **一条 `user` 角色的摘要消息** 插回，内容大致是：

```text
[CONTEXT COMPACTION — REFERENCE ONLY]
<结构化摘要：背景 / 已完成动作 / 关键上下文>
注：只读背景，不要重答旧问题
END
```

最终发给主模型的 messages 结构形如：

```text
[ system, user(摘要消息), ...tail ]
```

其中摘要消息故意用 `user` 而不是 `system`，是为了不破坏后续 `assistant/user` 的 role 交替约定。

所以一句话：  
**preflight 只在 token 预算越线时触发；触发后 messages 变成 “system + 一条 user 摘要 + 最近 tail”，中间历史被压成只读背景，主模型仍以 tail 里最新的 user 消息作为当前任务。**