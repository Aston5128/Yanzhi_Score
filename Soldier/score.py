# -*- coding:utf-8 -*-


import re
import time
import base64
import settings
import requests
import datetime
import subprocess

# 预先设定好分数的匹配器
FLOAT_COMP = re.compile(r'(.\..)')


class Score:
    # 小冰颜值页面
    web_url = 'http://kan.msxiaobing.com/V3/Portal?task=yanzhi'

    # 图片上传地址
    upload_url = 'http://kan.msxiaobing.com/Api/Image/UploadBase64'

    # 分数获取地址
    score_url = 'https://kan.msxiaobing.com/Api/ImageAnalyze' \
                '/Process?service=yanzhi'

    def __init__(self):
        # 服务器返回图片地址
        self.image_url = 'https://mediaplatform.msxiaobing.com{0}'

        # 请求头，同时适用与所有请求
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) '
                          'Gecko/20100101 Firefox/33.0',
            'Referer': self.web_url,
        }

        # 将 Cookie 添加到请求头中
        self.headers.update({'Cookie': self.get_cookies()})

        # base64 编码后的照片
        self.b64_image = None

    def get_cookies(self):
        """ 获取并构建小冰需要的 cookie """
        cookies = requests.get(self.web_url, headers=self.headers).cookies
        return 'ARRAffinity={0}; cpid={1}; salt={2}'.format(
            cookies['ARRAffinity'], cookies['cpid'], cookies['salt'])

    @staticmethod
    def base64_encoding(image):
        """ 小冰接收 b64 加密的图片 """
        return base64.b64encode(image)

    def get_image_url(self):
        """ 上传照片并获取照片在服务器中的 url """
        result = requests.post(self.upload_url, headers=self.headers,
                               data=self.b64_image).json()

        return self.image_url.format(result['Url'])

    def get_score(self, form):
        """ 获取服务器返回分数 json 以及被禁时的处理 """
        result = requests.post(self.score_url, headers=self.headers, data=form)
        result_json = result.json()

        # 如果服务器返回的 json 不是我们需要的，返回信息结尾的单词表示被 ban 的时长
        if not isinstance(result_json, dict):
            print(result_json, datetime.datetime.now())   # 输出异常信息
            if result_json.endswith('Hour.'):
                # 当设定关机字段为 True 时，被限一天后自动关机
                if settings.SHUTDOWN:
                    subprocess.call(settings.SHUTDOWN_COMMAND)
                time.sleep(86300)
            elif result_json.endswith('Day.'):
                time.sleep(3400)
            else:
                time.sleep(30)

            return 'ban'
        if 'content' in result_json.keys():
            temp_str = result_json['content']['text']
            print(temp_str)
            return re.findall(FLOAT_COMP, temp_str)

    def score(self, person_image):
        """ 获取分数 """
        # 设置照片
        self.b64_image = self.base64_encoding(person_image)

        # 获取照片在服务器中的地址
        image_url = self.get_image_url()
        form = {'Content[imageUrl]': image_url}

        times_count = 0                                     # 防止小冰误识别
        while True:
            # 获取分数
            score_text = self.get_score(form)

            if not score_text:
                print('No Score，Retry...')
                if times_count > 3:
                    return -1.0                             # 小冰未识别
                times_count += 1
            elif score_text is 'ban':
                continue
            else:
                return score_text[0]
