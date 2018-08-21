import requests
#from fake_useragent import UserAgent
import Logger
from urllib import parse
fake_header = {'user-agent': 'User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11'}
logger_name = 'WeatherGetter'

# 江门城市代码
cityId = "101281101"

# 和风天气的API
HeWeatherParams = {'location': f'CN{cityId}', 'key': '39c53be87abf42688bb594d1dcf9637f'}


def get_he_weather(url):
    return requests.get(url, params=HeWeatherParams, headers=fake_header)


def get_now():
    now_json = get_he_weather('https://free-api.heweather.com/s6/weather/now').json()['HeWeather6'][0]
    Logger.get_logger(logger_name + '_now').debug('Get Now Success!')
    return {
        'update_time':   now_json['update']['loc'],    # 接口更新时间
        'status':        now_json['status'],           # 接口状态
        'temp':          now_json['now']['tmp'],       # 温度
        'weather':       parse.quote(now_json['now']['cond_txt']),  # 天气
        'wind_ang':      now_json['now']['wind_deg'],  # 风向角
        'wind_dir':      parse.quote(now_json['now']['wind_dir']),  # 风向
        'wind_sc':       now_json['now']['wind_sc'],   # 风力
        'wind_spc':      now_json['now']['wind_spd'],  # 风速
        'humidity':      now_json['now']['hum'],       # 相对湿度
        'precipitation': now_json['now']['pcpn'],      # 降水量
        'visibility':    now_json['now']['vis'],       # 能见度
    }


def get_air():
    air_json = get_he_weather('https://free-api.heweather.com/s6/air/now').json()['HeWeather6'][0]
    Logger.get_logger(logger_name + '_air').debug('Get Air Success!')
    return {
        'update_time':    air_json['update']['loc'],         # 接口更新时间
        'status':         air_json['status'],                # 接口状态
        'aqi':            air_json['air_now_city']['aqi'],   # 空气质量指数 AQI
        'main':           air_json['air_now_city']['main'],  # 主要污染物
        'pm10':           air_json['air_now_city']['pm10'],  # PM10
        'pm25':           air_json['air_now_city']['pm25'],  # PM2.5
        'no2':            air_json['air_now_city']['no2'],   # 二氧化氮
        'so2':            air_json['air_now_city']['so2'],   # 二氧化硫
        'co':             air_json['air_now_city']['co'],    # 一氧化碳
        'o3':             air_json['air_now_city']['o3']     # 臭氧
    }


def get_lifestyle():
    # TODO 以更加简洁的方式一次生成dict
    def search_lifestyle_type(lifestyle_dict_in, type_name):
        for item in lifestyle_dict_in:
            if item['type'] == type_name:
                Logger.get_logger(logger_name + '_lifestyle').debug(f'Get item:{str(item)}')
                return [item['brf'], item['txt']]  # 返回指数简介 和 指数详情

    lifestyle_json = get_he_weather('https://free-api.heweather.com/s6/weather/lifestyle').json()['HeWeather6'][0]
    lifestyle_type_list = [
        'comf',   # 舒适度指数
        'cw',     # 洗车指数
        'drsg',   # 穿衣指数
        'flu',    # 感冒指数
        'sport',  # 运动指数
        'trav',   # 旅游指数
        'uv',     # 紫外线指数
        'air',    # 空气污染扩散指数
    ]

    lifestyle_dict = {
        'update_time': lifestyle_json['update']['loc'],  # 接口更新时间
        'status':      lifestyle_json['status'],         # 接口状态
    }

    for lifestyle_type in lifestyle_type_list:
        brf_txt = search_lifestyle_type(lifestyle_json['lifestyle'], lifestyle_type)
        lifestyle_dict[lifestyle_type + '_brf'] = parse.quote(brf_txt[0])
        lifestyle_dict[lifestyle_type + '_txt'] = parse.quote(brf_txt[1])

    Logger.get_logger(logger_name + '_lifestyle').debug('Get Lifestyle Success!')

    return lifestyle_dict


def get_sun_and_moon():
    def get_data_by_date(sun_json, date):
        for item in sun_json:
            if item['date'] == date:
                Logger.get_logger(logger_name + '_sun').debug(f'Get item:{str(item)}')
                return item

    sun_json = get_he_weather('https://free-api.heweather.com/s6/solar/sunrise-sunset').json()['HeWeather6'][0]
    today_date = get_data_by_date(sun_json['sunrise_sunset'], sun_json['update']['loc'][:10])  # 取前9位格式为 YYYY-MM-DD

    Logger.get_logger(logger_name + '_sun').debug('Get Sun Success!')

    return {
        'update_time': sun_json['update']['loc'],  # 接口更新时间
        'status':      sun_json['status'],         # 接口状态
        'sunrise':     today_date['sr'],           # 日升
        'sunset':      today_date['ss'],           # 日落
        # FIXME 丢人!!月升月落写反啦!!
        'moonrise':    today_date['ms'],           # 月升, 不知为何在接口中这两个是换过来的
        'moonset':     today_date['mr'],           # 月落, 不知为何在接口中这两个是换过来的
    }

'''
print(get_now())
print(get_air())
print(get_lifestyle())
print(get_sun_and_moon())
'''
