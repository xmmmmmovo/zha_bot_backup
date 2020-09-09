"""
异步获取天气str
"""
import requests  # 用来get json的
import json  # json解析包
from aiocache import cached  # 缓存
from nonebot.log import logger
import asyncio

weather_api_url = 'https://free-api.heweather.net/s6/weather'
key = ''
is_count_full = False  # 这里是检测sdk是否达到上限了


@cached(ttl=1 * 60 * 60)  # cache for 1 hours
async def get_weather_of_city(city: str) -> dict:
    # 这里简单返回一个字符串
    # 这里使用的是和风天气的api呢亲亲
    # TODO:这里如果用coolq:pro的话就可以带上天气标识符

    param = {
        'location': city,
        'key': key,
    }
    # get_url = weather_api_url + city + key
    # print(get_url)

    data = requests.post(weather_api_url, param)

    if data.status_code != 200:
        return {
            'status': 'error'
        }

    city_weather = json.loads(data.content)['HeWeather6'][0]  # 这里直接转
    logger.debug(type(city_weather))
    # print(city_weather)
    logger.debug(city_weather)
    return city_weather
