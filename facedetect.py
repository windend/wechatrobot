
from wxpy import *
import requests
import base64
import json
import os
from keda import main
bot = Bot(cache_path=True)


def ak(apikey, secret):
    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
        apikey, secret)
    # url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=rYNWIhZt82uu4jcFaUGhLT1K&client_secret=syumQjISxYlGYdUxvzRGMPwYfBrbSuox'
    rep = requests.post(url)
    at = rep.text
    at = json.loads(at)['access_token']
    # print(at)
    if at:
        querystring = {'access_token': at}
        return querystring


def car(image):
    querystring = ak('CMymyvbyK1C7KSW3EeBC2lXf',
                     'TwREuO4FHnXMGbMol2hFE7ywG8Zigymn')
    url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/car'
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'image': image, 'top_num': 5}
    result = requests.post(url=url, headers=header,
                           data=data, params=querystring)
    cars = json.loads(result.text)
    # print('error_code' not in cars and '非车类' not in cars['result'][0].values())
    if 'error_code' not in cars and '非车类' not in cars['result'][0].values():
        l = ['车型:{}\n概率:{}\n年份:{}\n'.format(
            x['name'], format(x['score'], '0.1f'), x['year']) for x in cars['result'] if x['score'] > 0.5]
        if len(l) > 0:
            l.insert(0, '颜色:{}'.format(cars['color_result']))
            return '\n---\n'.join(l)
        else:
            return None
    else:
        return None


def face(image):
    # 替换照片路径
    # with open(image, 'rb') as f:
    #     s = f.read()
    #     image = base64.b64encode(s)
    # url = {
    #     'face': 'https://api-cn.faceplusplus.com/facepp/v3/detect',
    #     'baidu': 'https://aip.baidubce.com/rest/2.0/face/v3/detect'
    # }
    # ak = {
    #     'face': '_Zk_DtUUSy5ZyMsqnq0Rry5psNSEqufN',
    #     'baidu': 'rYNWIhZt82uu4jcFaUGhLT1K'
    # }
    # secret = {
    #     'face': 'iog01_apR846iZ41SLDgUNZI3q5EmC6c',
    #     'baidu': 'syumQjISxYlGYdUxvzRGMPwYfBrbSuox'
    # }
    # querystringface = {
    #     'api_key': ak['face'],
    #     'api_secret': secret['face'],
    #     'return_attributes': 'age,beauty,eyestatus,emotion,gender,skinstatus,race,ethnicity'
    # }
    # # print(querystringface)
    # dataface = {
    #     'image_base64': image
    # }
    # urlface = url['face']
    querystring = ak('rYNWIhZt82uu4jcFaUGhLT1K',
                     'syumQjISxYlGYdUxvzRGMPwYfBrbSuox')
    urls = 'https://aip.baidubce.com/rest/2.0/face/v3/detect'
    header = {'Content-Type': 'application/json'}
    data = {'image': image, 'image_type': 'BASE64', 'max_face_num': 10,
            'face_field': 'age,beauty,expression,faceshape,gender,glasses,race,facetype'}

    result = requests.post(url=urls, headers=header,
                           data=data, params=querystring)
    face = json.loads(result.text)

    if face['error_code'] == 0:
        # print(json.dumps(json.loads(result.text), indent=2))
        config = {
            'male': '男',
            'female': '女',
            'square': '正方形',
            'triangle': '三角形',
            'oval': '椭圆',
            'heart': '心形',
            'round': '圆形',
            'yellow': '黄种人',
            'white': '白种人',
            'black': '黑种人',
            'arabs': '阿拉伯人',
        }

        age = face['result']['face_list'][0]['age']
        face_shape = face['result']['face_list'][0]['face_shape']['type']
        gender = face['result']['face_list'][0]['gender']['type']
        glasses = face['result']['face_list'][0]['glasses']['type']
        race = face['result']['face_list'][0]['race']['type']
        beauty = face['result']['face_list'][0]['beauty']

        print('年龄:{}\n性别:{}\n种族:{}\n颜值:{}\n脸型:{}'.format(
            age, config[gender], config[race], format(beauty, '0.1f'), config[face_shape]))
        text = '年龄:{}\n性别:{}\n种族:{}\n颜值:{}\n脸型:{}'.format(
            age, config[gender], config[race], format(beauty, '0.1f'), config[face_shape])
        return text
    else:
        return '检测不到面部，请重新传入正面照'


@bot.register(except_self=False)
def facedetect(msg):
    try:
        if msg.type == 'Picture':
            msg.reply('请稍等，正在扫描分析')
            img = base64.b64encode(msg.get_file())
            # print(img)
            cars = car(img)
            print(cars)
            if not cars:
                msg.reply_msg('检测不到车型，请重新传入照片')
                text = face(img)
                if len(text) > len('检测不到面部，请重新传入正面照'):
                    msg.reply_msg('识别到人脸,正在扫描分析')
                msg.reply_msg(text)
                paths = main(text)
                msg.reply_file(paths)
                os.remove(paths)
            else:
                msg.reply_msg(cars)
    except Exception as e:
        raise e


embed()
