# prep0：dsh-memory-evolve 源码速览（10-15 分钟导览）

> 用途：D1 早晨/晚间零碎时间 或 D2 预习。它是 **D2 对照表的"生产实证"第三行素材**——你在面试里能说"我天天在用的宿主记忆就是 Hermes-style 实现"，比任何 demo 都有说服力。
> 插件本体：`C:\Users\陈柏林\.dsh\profiles\web\node_modules\dsh-memory-evolve\`（github:csyangwen/dsh-memory-evolve，commit 999a0ed…）

## 读法（按序，每步 ≤3min，别陷进去）

1. **`README.md` 场景一**（"让 AI 真正记住你"）：五轨记忆 + 使用方式——2min 建立全貌。
2. **`lib/store.js` 词表定位**（用 grep/read 只看这些行，其他跳过）：
   - `ENTRY_DELIMITER` / `ENTRY_HEAD_RE`（L39/L138）：条目格式 = `§` 分隔 + `[日期]` + `[git 分支]` + `[id:xxxxxxxx]` —— **记忆是可 grep 的纯文本**。
   - `BRANCH_TAG_RE`（L79）+ `gitBranch()`（L485）：`[branch:xx]` 只在该 git 分支注入——分支隔离的落法。
   - `SUMMARY_TAG_RE` / `autoSummary`（L128/L160，80 字摘要）：**渐进式披露**的落法。
   - `THREAT_PATTERNS` / `scanThreat`（L422）：中英双语注入拒写正则——**防记忆投毒**。
   - `withLock`（L387）+ stale lock（L352）：目录锁 + tmp+rename 原子写——并发安全。
   - `SuggestionQueue`（L1286）：SUGGESTIONS.jsonl = **人确认队列**本体。
   - `ArchiveStore`（L1349）：冷存储 + 可"移回主记忆"——淘汰机制。
3. **`lib/index.js` 两个点**（grep "renderSnapshot"/"addOne"）：
   - 快照注入策略：注入=全局 memory + user + 当前项目 KEY；**daily/project 永不注入**，只靠"每回合收尾写"duty + 看门狗。
   - `addOne` 里 key 写入 → `enqueueSuggestion`（进队列等你确认）；subagent 禁写全局轨。
4. （可选）`src/client/MemoryQueueView.tsx`：你记忆页里"待确认"列表的前端。

## 产出（3 行笔记，并入 D2 对照表 dsh-memory-evolve 列）

1. 分层注入：慢变轨（USER/全局/项目 KEY）注入且分支过滤；流水轨（daily/project）永不注入、按需读。
2. 写入三道闸：投毒扫描（正则）→ 关键轨人确认队列（JSONL）→ 来源分级（subagent 禁碰全局轨）。
3. 工程细节：纯 md + 标签 = 可 grep 记忆；目录锁 + 原子写；归档冷存储可逆；git 分支隔离。

## 一句话面试答法
见 day2-memory.md 对照表下方"面试一句话答法"。
