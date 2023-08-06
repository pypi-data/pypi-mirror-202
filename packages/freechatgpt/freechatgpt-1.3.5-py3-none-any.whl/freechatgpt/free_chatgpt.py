# -*- coding: utf-8 -*-
# @Time    : 2023/3/2 10:42
# @Author  : abo123456789
# @Desc    : free_chatgpt.py
import json
import urllib.parse
from abc import ABCMeta
from json import JSONDecodeError

import requests
import retrying
from detool import timer_cost
from requests import ReadTimeout

from freechatgpt.ip_util import IpTool


def retry_if_timeout_error(excep):
    return isinstance(excep, ReadTimeout)


class FreeChatgpt(object):

    @staticmethod
    @timer_cost
    def ask(question: str):
        try:
            @retrying.retry(stop_max_attempt_number=5, stop_max_delay=100*1000,
                            wait_fixed=1000, retry_on_exception=retry_if_timeout_error)
            def ask_q():
                if not question or not question.strip():
                    return {'code': 0, 'error': 'question is null!'}
                print('AI问题思考中=====')
                answer_q = None
                try:
                    answer_q = PlatformGptZxx(question)._get_chat_res()
                    print(f'AI问题回答:{answer_q}')
                    return answer_q
                except JSONDecodeError:
                    return {'code': 0, 'error': answer_q}

            return ask_q()
        except ReadTimeout:
            return {'code': 0, 'error': 'ReadTimeout,please retry'}


class BasePlatform(metaclass=ABCMeta):
    def __init__(self, question: str):
        if question:
            self.question = urllib.parse.quote(question)
        else:
            raise Exception('question is null')

    def _get_chat_res(self) -> str:
        pass


class PlatformGptStore(BasePlatform):
    def _get_chat_res(self) -> str:
        url = "http://free-gpt.fun/chatgpt.php"
        ip = IpTool.get_host_ip() or '121.78.25.14'
        payload = f'message={self.question}&mychat_ip={ip}&user_uuid=CHAT-APIGPT-oj3uoj-gxhg-3u9ut-oj6q'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '83',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'vtins__JyvVgnc34VsbRCoA=%7B%22sid%22%3A%20%22d464cbac-4c29-5db2-9aa4-97ad394b66f4%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201681231922594%2C%20%22ct%22%3A%201681230122594%7D; __51uvsct__JyvVgnc34VsbRCoA=1; __51vcke__JyvVgnc34VsbRCoA=13fce5dc-d74d-50cc-b2c9-c4a588b479d6; __51vuft__JyvVgnc34VsbRCoA=1681230122602',
            'Host': 'free-gpt.fun',
            'Origin': 'http://free-gpt.fun',
            'Referer': 'http://free-gpt.fun/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=60)
        rs = response.text.split('答：')[1].strip('<br />').strip('<br />')
        return rs


class PlatformGptZxx(BasePlatform):

    @retrying.retry(stop_max_attempt_number=3)
    def _get_chat_res(self) -> str:
        url = "https://chat.zhuleixx.top/api"

        payload = "{\"messages\":[{\"role\":\"user\",\"content\":\"" + self.question + "\"}],\"temperature\":0.6,\"password\":\"\",\"model\":\"gpt-3.5-turbo\"}\n"
        headers = {
            'authority': 'chat.zhuleixx.top',
            'method': 'POST',
            'path': '/api',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'content-type': 'text/plain;charset=UTF-8',
            'cookie': 'Hm_lvt_220930121be5ed42a5f54a30151d15ae=1681444427; Hm_lpvt_220930121be5ed42a5f54a30151d15ae=1681444427',
            'origin': 'https://chat.zhuleixx.top',
            'referer': 'https://chat.zhuleixx.top/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=30)

        return response.text


class PlatformGptApi(BasePlatform):

    def _get_chat_res(self) -> str:
        url = f"https://v1.apigpt.cn/?q={self.question}"
        res = requests.get(url, timeout=70)
        if not res.text:
            raise ReadTimeout()
        res_json = json.loads(res.text)

        answer_q = res_json.get("ChatGPT_Answer")
        return answer_q


if __name__ == '__main__':
    # r = FreeChatgpt.ask(question='帮我优化这段话:pandas快速替换所有字符中的特殊字符')
    # print(r)
    # t = FreeChatgpt.ask(question='中国文化的特点是什么？')
    # print(t)
    q = '根据我的预算9000元,风险偏好进取型,预期收益率10.3%,请为我提供一种个人理财方案'
    s = FreeChatgpt.ask(question=q)
    print(s)

    # r = FreeChatgpt.ask(question='帮我创作一个广告视频OPPO卖点？')
    # print(r)
