import re
import time
import base64
import requests


# 预先设定好分数的匹配器
FLOAT_COMP = re.compile('(.\..)')


class Score:

    def __init__(self):
        # 小冰颜值页面
        self.web_url = 'http://kan.msxiaobing.com/V3/Portal?task=yanzhi'

        # 图片上传地址
        self.upload_url = 'http://kan.msxiaobing.com/Api/Image/UploadBase64'

        # 分数获取地址
        self.score_url = 'https://kan.msxiaobing.com/Api/ImageAnalyze' \
                         '/Process?service=yanzhi'

        # 服务器返回图片地址
        self.image_url = 'https://mediaplatform.msxiaobing.com{0}'

        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) '
                          'Gecko/20100101 Firefox/33.0',
        }

        # 小冰需要的 cookie
        self.cookies = self.get_cookies()

        # 照片
        self.b64_image = None

    def get_cookies(self):
        """ 获取小冰需要的 cookie """
        cookies = requests.get(self.web_url, headers=self.headers).cookies
        return 'ARRAffinity={0}; cpid={1}; salt={2}'.format(
            cookies['ARRAffinity'], cookies['cpid'], cookies['salt'])

    @staticmethod
    def base64_encoding(image):
        """ 小冰接收 b64 加密的图片 """
        return base64.b64encode(image)

    def get_image_url(self):
        """ 获取照片在服务器中的 url """
        result = requests.post(self.upload_url, headers=self.headers,
                               data=self.b64_image).json()

        return self.image_url.format(result['Url'])

    def get_score(self, form):
        # 获取服务器返回分数 json
        result = requests.post(self.score_url, headers=self.headers, data=form)
        result_json = result.json()
        print(result_json)
        if not isinstance(result_json, dict):
            return None
        if 'content' in result_json.keys():
            return re.findall(FLOAT_COMP, result_json['content']['text'])

    def score(self, person_image):
        """ 获取分数 """
        # 设置照片
        self.b64_image = self.base64_encoding(person_image)

        # 扩展请求头
        extend_headers = {
            'Cookie': self.cookies,
            'Referer': self.web_url,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        self.headers.update(extend_headers)

        # 获取照片在服务器中的地址
        image_url = self.get_image_url()
        form = {'Content[imageUrl]': image_url}

        while True:
            score_text = self.get_score(form)
            print(score_text)

            if score_text is [] or score_text is None:
                time.sleep(30)
                continue
            else:
                return score_text[0]


if __name__ == '__main__':
    score_inst = Score()
    with open('temp.jpg', 'rb') as file:
        print(score_inst.score(file.read()))
