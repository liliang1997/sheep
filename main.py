"""
主程序类
@author : lcry
@time : 2022/9/15 12:00
"""
import random
import asyncio
import requests
import sys
# import config
import httpx

import os

# 以下参数根据自己的需要进行修改：
SYS_CONFIG = {
    # 获取到的header中t值,必须修改为自己的
    "header_t": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ0MTU1OTYsIm5iZiI6MTY2MzMxMzM5NiwiaWF0IjoxNjYzMzExNTk2LCJqdGkiOiJDTTpjYXRfbWF0Y2g6bHQxMjM0NTYiLCJvcGVuX2lkIjoiIiwidWlkIjozNzMyODAzOCwiZGVidWciOiIiLCJsYW5nIjoiIn0.z9lpwYbVNPZlRoArxEM1PErDTTclv6vZdXdtkh9XacU",
    # 获取到的header中的user-agent值
    "header_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33",
    # 设定的完成耗时，单位s，默认-1随机表示随机生成1s~1h之内的随机数，设置为正数则为固定
    "cost_time": -1,
    # 需要通关的次数，默认1
    "cycle_count": 200
}


def get(key: str):
    value = os.getenv(key)
    if value is None:
        if key in SYS_CONFIG:
            value = SYS_CONFIG[key]
    return value


map_api = "https://cat-match.easygame2021.com/sheep/v1/game/map_info?map_id=%s"
# 完成游戏接口 需要参数状态以及耗时（单位秒）
finish_api = "https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=%s&rank_time=%s&rank_role=1&skin=1"

header_t = get("header_t")
header_user_agent = get("header_user_agent")
cost_time = get("cost_time")
cycle_count = get("cycle_count")

request_header = {
    "Host": "cat-match.easygame2021.com",
    "User-Agent": header_user_agent,
    "t": header_t
}

"""
调用完成闯关
Parameters:
  state - 状态
  cost_time - 耗时
"""
k = 0

async def finish_game(state, rank_time):
    
    async with httpx.AsyncClient() as client:
        res = await client.get(finish_api % (state, rank_time),headers=request_header)
    # err_code为0则成功
    if res.json()["err_code"] == 0:
        print("状态成功")
    else:
        print(res.json())
        print("请检查t的值是否获取正确!")


async def start(i):
    global cost_time, k
    print(f"...第{i + 1}次开始闯关...")
    if cost_time == -1:
        time = random.randint(1, 3600)
        print(f"第{i+1}次生成随机完成耗时:{time} s")
    try:
        await finish_game(1, time)
        k = k+1
        print(f"...第{i + 1}次完成闯关...")
    except Exception as e:
        print(f"游戏服务器响应超时或崩溃中未及时响应，本次程序运行结束,错误日志: {e}")
        print(f"【第{i+1}失败】")
        
    

async def main():
    print("【羊了个羊一键闯关开始启动】")
    task = [start(i) for i in range(cycle_count)]
    await asyncio.gather(*task)
    print(f"【羊了个羊一键闯关结束】，本轮共尝试{cycle_count}次，完成{k}次")


if __name__ == '__main__':

    asyncio.run(main())

