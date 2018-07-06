#-*- coding: utf-8 -*-
import requests
import re
import time
import hashlib
import base64
import struct
import json

URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"
APPID = "5b2bddde"
API_KEY = "9912cb7ba27ac02f4fdcd440a500fa97"
# API_KEY = "998a60e0dfab4f5e924831111198d712"


def getHeader():
    curTime = str(int(time.time()))
    params = json.dumps({
        "auf": "audio/L16;rate=16000",
        "aue": AUE,
        "voice_name": "xiaoyan",
        "speed": "50",
        "volume": "50",
        "pitch": "50",
        "engine_type": "intp65",
        "text_type": "text"
    }).encode()
    paramBase64 = base64.b64encode(params).decode()
    # print(paramBase64)
    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode())
    checkSum = m2.hexdigest()
    # print(checkSum)
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'X-Real-Ip': '127.0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    # print(header)
    return header


def getBody(text):
    data = {'text': text}
    return data


def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    return file


text = '科大讯飞是中国最大的智能语音技术提供商'


def main(text):
    r = requests.post(URL, headers=getHeader(),
                      data=getBody(text))
    contentType = r.headers['Content-Type']
    if contentType == "audio/mpeg":
        sid = r.headers['sid']
        if AUE == "raw":
            paths = writeFile('{}.wav'.format(sid), r.content)
        else:
            paths=writeFile('audio/{}.mp3'.format(sid), r.content)
        # print("success, sid = " + sid)
        return paths
    else:
        print(r.text)
        return r.text

