import json
import requests
import os
import re
import random

# 推送：https://www.pushplus.plus/push2.html
# 天气： http://www.weather.com.cn/weather1d/101010100.shtml#search
def getIPv6Address():
    output = os.popen("ifconfig").read()
    # print(output)
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]


def get_weather(city_code):
    url = 'http://t.weather.sojson.com/api/weather/city/' + city_code
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }

    rep = requests.get(url, headers=header)
    rep.encoding = "utf-8"
    weather = rep.text
    weather = json.loads(weather)

    time = weather['time']  # 时间
    parent = weather['cityInfo']['parent']  # 所属城市
    city = weather['cityInfo']['city']  # 城区
    updateTime = weather['cityInfo']['updateTime']  # 更新时间
    shidu = weather['data']['shidu']  # 湿度
    pm25 = weather['data']['pm25']  # PM2.5
    quality = weather['data']['quality']  # 空气质量
    wendu = weather['data']['wendu']  # 当前温度
    low = weather['data']['forecast'][0]['low']  # 今日最低温
    high = weather['data']['forecast'][0]['high']  # 今日最高温
    week = weather['data']['forecast'][0]['week']  # 星期
    fx = weather['data']['forecast'][0]['fx']  # 风向
    fl = weather['data']['forecast'][0]['fl']  # 风力
    wtype = weather['data']['forecast'][0]['type']  # 天气

    result = '【今日天气预报】' + '\n' \
             + parent + city + "  " + time + "\n" \
             + "更新时间：" + week + "  " + updateTime + "\n" \
             + "当前温度：" + wendu + "℃" + "\n" \
             + "天气：" + wtype + "\n" \
             + "温度范围：" + low + "~" + high + "\n" \
             + "空气湿度：" + shidu + "\n" \
             + "风向：" + fx + "\n" \
             + "风力：" + fl + '\n' \
             + "空气质量：" + quality + '\n' \
             + "PM2.5：" + str(pm25)

    return result


def send_wechat(msg):
    token = 'e309c790f7374c20afc921a0aba55b8b'  # 前边复制到那个token
    title = '每日天气[北京]'
    content = msg
    template = 'html'
    topic = '爱匹敌之v6'
    url = f"http://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}&topic={topic}"
    print(url)
    r = requests.get(url=url)
    print(r.text)


def read_old_ipv6():
    with open("ipv6.txt", "r") as f:
        data = f.readline()
    print(data)
    return data


def write_ipv6(ipv6):
    with open("ipv6.txt", "w") as f:
        f.write(ipv6)  # 自带文件关闭功能，不需要再写f.close()


if __name__ == '__main__':
    city_code = '101010100'

    ipv6 = ""
    try:
        ipv6 = getIPv6Address()
        print(ipv6)
    except Exception as e:
        print('get ipv6 error')

    weather = ""
    try:
        weather = get_weather(city_code)
        print(weather)
    except Exception as e:
        print('get_weather error')
    seed = random.randint(1, 100000)
    msg = '''
    {0}
    
<a href="http://[{1}]:90">点击打开->最新网盘地址</a> 
<p>也可复制以下地址去浏览器打开：</p><p>http://[{1}]:90</p>
<p>幸运随机数{2}</p>
    '''.format(weather, ipv6, seed)
    send_wechat(msg)
