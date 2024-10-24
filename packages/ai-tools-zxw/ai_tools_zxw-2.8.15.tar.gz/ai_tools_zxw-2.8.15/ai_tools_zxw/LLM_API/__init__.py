"""
# File       : __init__.py.py
# Time       ：2024/8/18 下午1:59
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
from pydantic import BaseModel
from typing import List, Optional

model_price = {
    "qwen-plus": {"input": 0.0008, "output": 0.0002}
}


class UsageStatistic(BaseModel):
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]


class LLM:
    chat_history = [
        # {"role": "system", "content": "你现在扮演李白，你豪情万丈，狂放不羁；接下来请用李白的口吻和用户对话。"} , # 设置对话背景或者模型角色
        # {"role": "user", "content": "你是谁"},  # 用户的历史问题
        # {"role": "assistant", "content": "....."} , # AI的历史回答结果
        # # ....... 省略的历史对话
        # {"role": "user", "content": "你会做什么"}  # 最新的一条问题，如无需上下文，可只传最新一条问题
    ]

    usage_statistic: List[UsageStatistic] = [
        # UsageStatistic(**{'prompt_tokens': 6, 'completion_tokens': 348, 'total_tokens': 354}) ,
    ]

    def __del__(self):
        ...

    def cal_total_price(self):
        ...

    def chat(self, input_content: str, single_chat: bool) -> str:
        ...

    async def chat_async(self, input_content: str, single_chat=False) -> str:
        ...

    def 添加上下文(self, role, content):
        """
        :param role: system, user, assistant
        :param content:
        :return:
        """
        self._set_text(role, content)

    # def 清除所有上下文(self):
    #     self.chat_history = []
    #
    # def 删除上条对话(self):
    #     last = self.chat_history[:-1]
    #     if len(last) % 2 != 0:
    #         last = last[:-1]
    #     self.chat_history = last

    def _set_usage(self, usage: dict):
        self.usage_statistic.append(UsageStatistic(**usage))
        return self.usage_statistic

    def _set_text(self, role, content) -> List[dict]:
        json_con = {"role": role, "content": content}
        self.chat_history.append(json_con)
        return self.chat_history

    def _check_length(self, text):
        while self._get_length(text) > 18000:
            del text[0]

        # check if the beginning is not user
        if text[0]["role"] != "user":
            del text[0]

        return text

    @staticmethod
    def _get_length(text: List[dict]) -> int:
        length = 0
        for content in text:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length
