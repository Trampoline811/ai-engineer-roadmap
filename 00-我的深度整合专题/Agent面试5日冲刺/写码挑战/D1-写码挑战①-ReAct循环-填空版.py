# -*- coding: utf-8 -*-
r"""D1 写码挑战① · 填空版（ReAct 主循环）

────────────────────────────────────────────────────────────────
先说清楚这个循环在干嘛（30 秒看懂，然后往下填）
────────────────────────────────────────────────────────────────
一句话：把「问题 + 到目前为止干过的所有事」拼成一段文字发给模型；
模型回来说"我要用某个工具、参数是 X" → 你执行工具、把结果记下来；
或者模型直接说出了最终答案 → 你返回它。
干满 max_steps 步还没答案 → 硬停，返回失败。

它为什么能"自己一轮一轮干"？就因为这个 for 循环把
    拼上下文 → 问模型 → 看它要干嘛 → 执行 → 记结果 → 回到循环头
转了一遍又一遍。这就是最小 loop。

────────────────────────────────────────────────────────────────
你的任务
────────────────────────────────────────────────────────────────
把下面所有 ____ 填上，让这个文件能跑通。
· 不许翻 `01-Agent\02-Agent_react\agent\loop.py`（本行原样保留）
· 先凭理解填；哪一空卡住，看文件最底部的「逐空提示」
· 填空顺序建议：空3 → 空4 → 空5 → 空6 → 空7 → 空8 → 空9 → 空10 → 空11 → 空12 → 空13 → 空15 → 空14 → 空1 → 空2

原本的 7 个必答点，对应到空里就是：
  1) 函数签名（含硬顶参数）      → 空2
  2) history 存什么、几个字段    → 空3、空10
  3) 循环怎么写、为什么不是 while → 空4
  4) 判断"这轮该调工具"          → 空8
  5) 工具调完做什么、然后去哪    → 空9、空11
  6) 什么情况下返回最终答案      → 空12、空13
  7) 跑满步数返回什么            → 空15
"""

import json
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple


# 空1：给 Tool 补上三个字段 —— name（工具名）/ description（给模型看的说明）/ run（真正执行的函数）
@dataclass
class Tool:
    name: str
    description: str
    run: Callable[[str], str]


# history 每条 = (thought, action, action_input, observation)   ← 这就是"状态"
HistoryItem = Tuple[str, str, str, str]


def react_loop(question:str , 
               tools:Dict[str, Tool], 
               llm:Callable[[str], str], 
               max_steps=6):          # 空2：给这三个参数补类型标注
    # question: 用户问题（str）
    # tools:    工具名 → Tool 的字典（Dict[str, Tool]）
    # llm:      收一段 prompt 字符串、返回模型输出字符串的可调用对象（Callable[[str], str]）
    # max_steps: 硬顶
    history: List[HistoryItem] = []                          # 空3：一开始历史里有什么？

    for step in range(1, max_steps + 1):                     # 空4：循环上限写什么？
        prompt = build_prompt(question, history, tools)      # 空5：把"问题+历史+工具说明"拼成 prompt
        out = llm(prompt)                                   # 空6：把 prompt 交给模型

        action, action_input = parse_action(out)                     # 空7：从模型输出里解析出"要用哪个工具"

        # 模型这轮说要调工具 —— 那就先干活
        if action and (action in tools):                                  # 空8：什么情况下这个工具才算"能用"？
            thought = ""
            for line in out.splitlines():
                if line.startswith("Thought:"):
                    thought = line.split("Thought:", 1)[1].strip()
                    break
            obs = tools[action].run(action_input or "")      # 空9：调用工具的 run 方法，拿到"观察结果"
            print(json.dumps({"action": action, "observation": obs}, indent=2, ensure_ascii=False))
            history.append((thought, action, action_input, obs))   # 空10：把这一轮的四个字段按顺序塞进历史
            continue                                             # 空11：这一轮处理完了，接下来去哪？（一个关键字）

        # 模型没调工具，而是直接给了答案 —— 正常出口
        if "Final Answer:" in out:                                    # 空12：最终答案的标记词是什么？
            answer = out.split("Final Answer:", 1)[1].strip()         # 空12b：同上，从标记后面取答案
            return answer                                     # 空13：返回什么？

        # 模型输出既不调工具、也没给答案 —— 既不重试也不退出，而是把错误当成"观察结果"记下来
        obs = f"ERROR: invalid Action. Must be one of {list(tools.keys())}."
        history.append(("", action or "", action_input or "", obs))
        # 空14：这里为什么不是 return？（一句话写在下面这行注释里，不用写代码）
        # 答：不能 return。一次模型格式错误不应终止整个循环；应该把错误作为 observation 写回 history，让模型下一轮自我纠正。

    return "Failed: max steps exceeded."                                            # 空15：跑满 max_steps 还没答案，返回什么？


# ────────────────────────────────────────────────────────────────
# 空1 的具体化：三个工具（照抄即可，不用改）
# ────────────────────────────────────────────────────────────────
def _calculator(expr: str) -> str:
    """只允许数字与 + - * / ( ) 的算式求值。"""
    import re
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expr):
        return "ERROR: 只支持数字与 + - * / ( )"
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:                                    # noqa: BLE001
        return f"ERROR: {e}"


def _get_current_time(_: str) -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _word_count(text: str) -> str:
    return str(len(text))


def build_tools() -> Dict[str, "Tool"]:
    return {
        "calculator": Tool("calculator", "计算一个算术表达式，输入如 21+21", _calculator),
        "get_current_time": Tool("get_current_time", "获取当前时间，输入为空", _get_current_time),
        "word_count": Tool("word_count", "统计字符串的字符数，输入为待统计的字符串", _word_count),
    }


# ────────────────────────────────────────────────────────────────
# 做题用：把 prompt 拼装与解析先给你（这两块不属于本次挑战点）
# 真实仓库里它们在同目录的 agent\prompt.py
# ────────────────────────────────────────────────────────────────
def build_prompt(question: str, history: List[HistoryItem], tools: Dict[str, "Tool"]) -> str:
    tool_desc = "\n".join(f"- {t.name}: {t.description}" for t in tools.values())
    parts = [
        "你是一个可以使用工具的助手。",
        "可用工具：", tool_desc, "",
        "严格按下面格式输出，一次只输出一个 Thought 和一个 Action：",
        "Thought: 你的推理",
        "Action: 工具名",
        "Action Input: 传给工具的输入（没有则留空）",
        "当你已经能回答用户时，输出：",
        "Final Answer: 你的最终回答",
        "",
        f"用户问题：{question}",
    ]
    if history:
        parts.append("\n之前的尝试：")
        for thought, action, action_input, obs in history:
            parts.append(f"Thought: {thought}")
            parts.append(f"Action: {action}")
            parts.append(f"Action Input: {action_input}")
            parts.append(f"Observation: {obs}")
    return "\n".join(parts)


def parse_action(out: str) -> Tuple[str, str]:
    action, action_input = "", ""
    for line in out.splitlines():
        if line.startswith("Action:") and not line.startswith("Action Input:"):
            action = line.split("Action:", 1)[1].strip()
        elif line.startswith("Action Input:"):
            action_input = line.split("Action Input:", 1)[1].strip()
    return action, action_input


# 用一个"假模型"就能离线自测：它会先调 calculator，再调 word_count，
# 再调 get_current_time，最后给 Final Answer。
class FakeLLM:
    def __init__(self, tools):
        self.tools = tools
        self.n = 0

    def __call__(self, prompt: str) -> str:
        self.n += 1
        if self.n == 1:
            return "Thought: 先算加法\nAction: calculator\nAction Input: 21+21"
        if self.n == 2:
            return "Thought: 再数字符\nAction: word_count\nAction Input: 42"
        if self.n == 3:
            return "Thought: 还要当前时间\nAction: get_current_time\nAction Input: "
        return "Thought: 信息齐了\nFinal Answer: 21+21=42，共 2 个字符，现在时间是 …"


if __name__ == "__main__":
    tools = build_tools()
    llm = FakeLLM(tools)
    result = react_loop("请帮我计算 21+21，并统计答案字符串有多少个字符, 并且打印当前时间。", tools, llm)
    print("=" * 60)
    print("最终结果：", result)


# ════════════════════════════════════════════════════════════════
# 逐空提示（卡住才看，一次只看一条）
# ════════════════════════════════════════════════════════════════
# 空1  三行字段：name: str、description: str、run: Callable[[str], str]（照抄你在 agent\types.py 见过的）
# 空2  question: str, tools: Dict[str, Tool], llm: Callable[[str], str] —— 按注释里的说明写就行
# 空3  循环开始前，历史是空的：一个空列表 []
# 空4  上限就是那个硬顶参数本身（想想它叫什么名字）
# 空5  同目录的 build_prompt 已经给你了，直接调它
# 空6  llm 本身就可调用，直接把 prompt 交给它
# 空7  parse_action 已经给你了
# 空8  不只要"模型说了工具名"，还要"这个名字确实在我们提供的工具里"——想想字典怎么判断键存在
# 空9  Tool 的第三个字段是什么？直接调它
# 空10 顺序是 (thought, action, action_input, obs) —— 和文件顶部 HistoryItem 的定义一致
# 空11 这一轮已经处理完，该进入下一轮了，用哪个关键字？
# 空12 见 build_prompt 里那段格式说明（"当你已经能回答用户时，输出：…"）
# 空13 你要把答案交给调用者——那个关键字你已经在 main.py 里见过
# 空14 想一想：如果这里 return，模型偶发一次格式错误就直接结束了，那 loop 还有什么意义？
#      正确做法是"把错误当成观察结果喂回去，让它自己纠正"——所以这里不能退出
# 空15 硬顶触发意味着"没做完"，返回一句能看出原因的话（仓库里那句是 "Failed: max steps exceeded."）
