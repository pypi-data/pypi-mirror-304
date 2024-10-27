#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2024/10/21 20:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.hailuo_types import BASE_URL, UPLOAD_BASE_URL, FEISHU_URL, FEISHU_URL_ABROAD
from meutils.schemas.hailuo_types import VideoRequest, VideoResponse
from meutils.config_utils.lark_utils import get_next_token_for_polling
import requests
import json

url = "https://hailuoai.com/api/multimodal/generate/video?device_platform=web&app_id=3001&version_code=22201&uuid=8c059369-00bf-4777-a426-d9c9b7984ee6&device_id=243713252545986562&os_name=Mac&browser_name=chrome&device_memory=8&cpu_core_num=10&browser_language=zh-CN&browser_platform=MacIntel&screen_width=1920&screen_height=1080&unix=1729512887000"

"https://hailuoai.com/v1/api/files/request_policy?device_platform=web&app_id=3001&version_code=22201&uuid=8c059369-00bf-4777-a426-d9c9b7984ee6&device_id=243713252545986562&os_name=Mac&browser_name=chrome&device_memory=8&cpu_core_num=10&browser_language=zh-CN&browser_platform=MacIntel&screen_width=1920&screen_height=1080&unix=1729563007000"


async def get_request_policy(token: Optional[str] = None):
    """
    {
        "data": {
            "accessKeyId": "STS.NUVNbdQfqTNixCxUTAhdeJToq",
            "accessKeySecret": "DRBsh8Qm8VnXXxTwFMX5KkXVoqbbsPj4ewEfgTLysGvM",
            "securityToken": "CAISiwN1q6Ft5B2yfSjIr5bjBdjQvLlQ44yCemXJsVQUZOtJpZHEkzz2IHhMf3VpAusWsPw1n2tT6/sdlrBoS4JMREPJN5EhtsQLrl75PdKY4Jzltedb0EIf6JFQUUyV5tTbRsmkZj+0GJ70GUem+wZ3xbzlD2vAO3WuLZyOj7N+c90TRXPWRDFaBdBQVH0AzcgBLinpKOqKOBzniXayaU1zoVhYiHhj0a2l3tbmvHi4tlDhzfIPrIncO4Wta9IWXK1ySNCoxud7BOCjmCdb8EpN77wkzv4GqzLGuNCYCkkU+wiMN+vft9ZjKkg7RNBjSvMa8aWlzKYn57OCyt2v8XsXY7EJCRa4bZu73c7JFNmuMtsEbrvhMxzPqIvXbsKp6lh/MSxDblgRIId8dWURExUpTSrBIaOh6M4Bo5NbzHzuOsgSpnkVpz2AlbLiT9M/1aieRiRTcymwO/ayjeq6CeAF3mM8Mm0qPRouTM2+Zo5YD3N1opjTpiapdUYLox8awbuQLp25tMiF6FiLDvouuRqAAQJZHVcOeb5qnR6mkzw5hwzSOXoMXVFzDE2aB7dvRYFD9HiG6T66hE4Xlfpph9H7xWrpaBf5vqHQXp4gyuqVOgFIjdPECwisXlyAKQWMak7bGToh3cetCux3pjq74sP/KAjzSzDkwciJBbn8vZzNKKR/ozxqve925vtPPPWGPowwIAA=",
            "expiration": "2024-10-22T02:55:14Z",
            "dir": "cdn-yingshi-ai-com/prod/2024-10-22-09/user/multi_chat_file",
            "endpoint": "oss-cn-wulanchabu.aliyuncs.com",
            "bucketName": "minimax-public-cdn",
            "serverTime": "2024-10-22T02:10:07Z"
        }
    }
    """
    token = token or await get_next_token_for_polling(FEISHU_URL)
    headers = {
        'token': token.strip(),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.get("/v1/api/files/request_policy")
        response.raise_for_status()
        return response.json()['data']


async def upload(token: Optional[str] = None):
    """

    :param token:
    :return:
    """
    token = token or ""
    # headers = {
    #     "Authorization": "OSS STS.NUVNbdQfqTNixCxUTAhdeJToq:bAJE79c9W8nWbsHpY6+wEI+eD+s=",
    #     "x-oss-security-token"
    # }

    async with httpx.AsyncClient(base_url=UPLOAD_BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/v1/api/file/upload")
        response.raise_for_status()
        return response.json()['data']['token']


async def refresh_token(token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)

    params = {
        # 'device_platform': 'web',
        # 'app_id': '3001',
        # 'version_code': '22201',
        # 'uuid': '8c059369-00bf-4777-a426-d9c9b7984ee6',
        # 'device_id': '243713252545986562',
        # 'os_name': 'Mac',
        # 'browser_name': 'chrome',
        # 'device_memory': '8',
        # 'cpu_core_num': '10',
        # 'browser_language': 'zh-CN',
        # 'browser_platform': 'MacIntel',
        # 'screen_width': '1920',
        # 'screen_height': '1080',
        # 'unix': '1729512887000'
    }
    headers = {
        'token': token.strip()
    }
    async with httpx.AsyncClient(base_url=BASE_URL, params=params, headers=headers, timeout=60) as client:
        response = await client.post("/v1/api/user/renewal")
        response.raise_for_status()
        return response.json()['data']['token']


async def create_task(request: VideoRequest, token: Optional[str] = None):
    token = token or ""
    payload = {
        "desc": request.prompt,
        "useOriginPrompt": request.prompt_optimizer,
        "fileList": []
    }
    params = {
        # 'device_platform': 'web',
        # 'app_id': '3001',
        # 'version_code': '22201',
        # 'uuid': '8c059369-00bf-4777-a426-d9c9b7984ee6',
        # 'device_id': '243713252545986562',
        # 'os_name': 'Mac',
        # 'browser_name': 'chrome',
        # 'device_memory': '8',
        # 'cpu_core_num': '10',
        # 'browser_language': 'zh-CN',
        # 'browser_platform': 'MacIntel',
        # 'screen_width': '1920',
        # 'screen_height': '1080',
        # 'unix': '1729512887000'
    }
    headers = {
        'token': token.strip()
        #
        # 'baggage': 'sentry-environment=production,sentry-release=sNSny8g-R6K_t1nySs-NE,sentry-public_key=6cf106db5c7b7262eae7cc6b411c776a,sentry-trace_id=2c8b95f12c6f4fb79cc1da8d09310a1e,sentry-sample_rate=1,sentry-sampled=true',
        # 'priority': 'u=1, i',
        # 'sentry-trace': '2c8b95f12c6f4fb79cc1da8d09310a1e-b213abc0acef8415-1',
        # 'yy': 'e15d3f39ca6abd135bd79555e93b4935',
        # 'Cookie': 'sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229DEadPlORXm1%22%2C%22first_id%22%3A%22191b73294831278-01aaf295e0ad0e-18525637-2073600-191b73294842661%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxYjczMjk0ODMxMjc4LTAxYWFmMjk1ZTBhZDBlLTE4NTI1NjM3LTIwNzM2MDAtMTkxYjczMjk0ODQyNjYxIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiOURFYWRQbE9SWG0xIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%229DEadPlORXm1%22%7D%2C%22%24device_id%22%3A%22191b73294831278-01aaf295e0ad0e-18525637-2073600-191b73294842661%22%7D',
        # 'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        # 'content-type': 'application/json'
    }
    async with httpx.AsyncClient(base_url=BASE_URL, params=params, headers=headers, timeout=60) as client:
        response = await client.post("/api/multimodal/generate/video", json=payload)
        response.raise_for_status()
        return response.json()
    # {
    #     "statusInfo": {
    #         "code": 1000061,
    #         "httpCode": 0,
    #         "message": "上一个视频任务未完成，请稍后再试",
    #         "serviceTime": 1729512914,
    #         "requestID": "82bc8c60-4dc3-4ad0-b5b6-b1836e0c88ab",
    #         "debugInfo": "",
    #         "serverAlert": 0
    #     }
    # }

    # {
    #     "data": {
    #         "id": "304746220940677121"
    #     },
    #     "statusInfo": {
    #         "code": 0,
    #         "httpCode": 0,
    #         "message": "成功",
    #         "serviceTime": 1729513305,
    #         "requestID": "caaf2364-d2ed-45df-b79a-827810a5d58c",
    #         "debugInfo": "",
    #         "serverAlert": 0
    #     }
    # }


async def get_task(task_id="304744496913956870"):
    params = {
        'idList': task_id,
        'device_platform': 'web',
        'app_id': '3001',
        'version_code': '22201',
        'uuid': '8c059369-00bf-4777-a426-d9c9b7984ee6',
        'device_id': '243713252545986562',
        'os_name': 'Mac',
        'browser_name': 'chrome',
        'device_memory': '8',
        'cpu_core_num': '10',
        'browser_language': 'zh-CN',
        'browser_platform': 'MacIntel',
        'screen_width': '1920',
        'screen_height': '1080',
        'unix': '1729512894000'
    }
    headers = {
        'token': token.strip()

        # 'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI5Njg4NjksInVzZXIiOnsiaWQiOiIyMjkwODQ3NTA2MDEzODgwMzciLCJuYW1lIjoi5bCP6J665bi9ODAzNyIsImF2YXRhciI6Imh0dHBzOi8vY2RuLnlpbmdzaGktYWkuY29tL3Byb2QvdXNlcl9hdmF0YXIvMTcwNjI2NzcxMTI4Mjc3MDg3Mi0xNzMxOTQ1NzA2Njg5NjU4OTZvdmVyc2l6ZS5wbmciLCJkZXZpY2VJRCI6IjI0MzcxMzI1MjU0NTk4NjU2MiIsImlzQW5vbnltb3VzIjpmYWxzZX19.zVW_ADmms_QfJqV0YlFQB-WZJWmUrRBdFv2kuY0Fqa4',
        # 'Cookie': 'sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229DEadPlORXm1%22%2C%22first_id%22%3A%22191b73294831278-01aaf295e0ad0e-18525637-2073600-191b73294842661%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxYjczMjk0ODMxMjc4LTAxYWFmMjk1ZTBhZDBlLTE4NTI1NjM3LTIwNzM2MDAtMTkxYjczMjk0ODQyNjYxIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiOURFYWRQbE9SWG0xIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%229DEadPlORXm1%22%7D%2C%22%24device_id%22%3A%22191b73294831278-01aaf295e0ad0e-18525637-2073600-191b73294842661%22%7D',

    }
    async with httpx.AsyncClient(base_url=BASE_URL, params=params, headers=headers, timeout=60) as client:
        response = await client.get("/api/multimodal/video/processing")
        response.raise_for_status()
        return response.json()


if __name__ == '__main__':  # 304752356930580482
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI5NzAyMjIsInVzZXIiOnsiaWQiOiIyNDM3MTMyNTI3OTc2NDA3MDgiLCJuYW1lIjoi5bCP6J665bi9NzA4IiwiYXZhdGFyIjoiaHR0cHM6Ly9jZG4ueWluZ3NoaS1haS5jb20vcHJvZC91c2VyX2F2YXRhci8xNzA2MjY3MzY0MTY0NDA0MDc3LTE3MzE5NDU3MDY2ODk2NTg5Nm92ZXJzaXplLnBuZyIsImRldmljZUlEIjoiMjQzNzEzMjUyNTQ1OTg2NTYyIiwiaXNBbm9ueW1vdXMiOnRydWV9fQ.X3KW00hAhSMk1c7DrXWYR27BROHNbfSiHD7Y-aweA6o"

    #     token = """
    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI5NzA3MzUsInVzZXIiOnsiaWQiOiIyNDM3MTMyNTI3OTc2NDA3MDgiLCJuYW1lIjoi5bCP6J665bi9NzA4IiwiYXZhdGFyIjoiaHR0cHM6Ly9jZG4ueWluZ3NoaS1haS5jb20vcHJvZC91c2VyX2F2YXRhci8xNzA2MjY3MzY0MTY0NDA0MDc3LTE3MzE5NDU3MDY2ODk2NTg5Nm92ZXJzaXplLnBuZyIsImRldmljZUlEIjoiMjQzNzEzMjUyNTQ1OTg2NTYyIiwiaXNBbm9ueW1vdXMiOnRydWV9fQ.htsWC4neM8xaUDEx_XMWVL4TTh7fl8SrW6HU2iWjQuk
    #     """
    # arun(create_task(token))
    #
    # arun(get_task("304931390314479617"))  # 304932228734898178

    arun(get_request_policy())
