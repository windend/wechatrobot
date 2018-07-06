
import requests
import json
from lxml import etree
# from urllib import parse


# def onQQMessage(bot, contact, member, content):
#     if contact.mark == '好友备注' or contact.mark == '好友备注':
#         data = {'key': '21cafabfc62e4c2ab823327ba1797ac5', 'info': content}
#         data2 = {'key': 'fed5bf39c3a94eec9075bcc70580e066', 'info': content}

#         tuling = requests.request(
#             method='post', url='http://www.tuling123.com/openapi/api', data=data)
#         autoreply = json.loads(tuling.text)
#         autoreply.pop('code')
#         for x in autoreply.values():
#             bot.SendTo(contact, x)

def shorturlRe(url):
    req = requests.get(url=url)
    html = etree.HTML(req.text)
    return html.xpath('//script')[1].xpath('text()')[0].split('var')[3].split(";")[0].split("'")[1]


def onQQMessage(bot, contact, member, content):
    url = 'https://pub.alimama.com/items/search.json'
    page = 1
    size = 50
    header = {'accept': 'application/json, text/javascript, */*; q=0.01',
              'accept-encoding': 'gzip, deflate, br',
              'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
              'Host': 'pub.alimama.com',
              'referer': 'http://pub.alimama.com/promo/search/index.htm?q=%E8%B7%AF%E7%94%B1&_t=1527140719231',
              'Cookie': 't=65a3f118f0d5d43c7fe117a8be08f817; cookie2=13fd1221dec3ea9763637418957b893b; v=0; _tb_token_=33be65ded35eb; cna=SS6EEzNgDwsCAd73tCd2fBcM; undefined_yxjh-filter-1=true; alimamapwag=TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfNCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY2LjAuMzM1OS4xODEgU2FmYXJpLzUzNy4zNg%3D%3D; cookie32=f3baeec7c052461cbe5eb16eee1db478; alimamapw=Rw8HDVJeAQlDDVFYXF5cV19YPQcBUVJQUQZRCQMMBw4DVVQJVwQDBlUEAQZXX1UIVFJT; cookie31=MTMyNDQwMDk1LHM4Mzg0ODE4JTQwYWxpbWFtYSwxMTczNTkwNjJAYWxpbWFtYS5jb20sVEI%3D; login=U%2BGCWk%2F75gdr5Q%3D%3D; taokeisb2c=; account-path-guide-s1=true; rurl=aHR0cDovL3B1Yi5hbGltYW1hLmNvbS8%2Fc3BtPWEyMTl0Ljc2NjQ1NTQuYTIxNHRyOC45LjJlMjAzNWQ5dFdKVE44; 132440095_yxjh-filter-1=true; apushfab5c63114239d725bd0105e1b8e4eaa=%7B%22ts%22%3A1527140884215%2C%22heir%22%3A1527140728008%2C%22parentId%22%3A1527140709470%7D; isg=BEZGCQKXYVfeTzWwL8e04rPtlzoID4tlcvwS2zBrhGlVM_BNhTZNc6eFDm__v4J5',
              'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
              'x-requested-with': 'XMLHttpRequest'}
    # print(content)
    if contact.mark == '邱小刀'or contact.mark == '我是谁':
        # print(content.startswith('【'))
        if content.startswith('【'):
            # print(len(content.split(' ')))
            if len(content.split(' ')) > 5:
                content = content.split(' ')[0].split('】')[1]
                content = shorturlRe(content)
                # print(content)
            else:
                content = content.split('】')[0].split('【')[1]
        preload = {'q': content,
                   '_t': '1527074885336',
                   'toPage': page,
                   'queryType': '0',
                   'sortType': '1',
                   'auctionTag': '',
                   'perPageSize': size,
                   # 'shopTag': 'yxjh',
                   'shopTag': '',
                   't': '1527078218120',
                   '_tb_token_': '33be65ded35eb',
                   'pvid': '10_222.240.118.0_745_1527078217613'}
        # print(preload)
        taobao = requests.get(url=url, params=preload)
        taobao = json.loads(taobao.text)
        # print(taobao)
        text = '无法找到对应的物品或链接，请重新输入'
        try:
            title = taobao['data']['pageList'][0]['title'].replace(
                '<span class=H>', '/玫瑰').replace('</span>', '/玫瑰')
            msale = taobao['data']['pageList'][0]['biz30day']
            reservePrice = taobao['data']['pageList'][0]['reservePrice']
            zkPrice = taobao['data']['pageList'][0]['zkPrice']
            returnFee = taobao['data']['pageList'][0]['tkCommFee']
            picurl = 'https:{}'.format(
                taobao['data']['pageList'][0]['pictUrl'])
            returnFee = taobao['data']['pageList'][0]['tkCommFee']
            link = taobao['data']['pageList']

            if not link or not content:
                bot.SendTo(contact, text)
            else:
                bot.SendTo(contact, '{}\n月售:{}\n原价:{}\n折后价:{}\n可获得返利:{}￥\n链接:{}'.format(
                    title, msale, reservePrice, zkPrice, returnFee, link[0]['auctionUrl']))
        except TypeError as e:
            bot.SendTo(contact, text)
