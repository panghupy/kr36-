'''抓取快讯，发布在xiou网上
kr36网址：https://36kr.com/newsflashes
每分钟更新数据库，逻辑如下：爬取２０条快讯，判断id是否在数据库中，没有就添加到数据库，并发表在xiouwang
注：使用前确保本地数据库　kr36_db　存在,表名:News,字段id,title
'''

import requests
import json
import urllib3
import time
from DataTools.tools import MysqlHelper
from NewsAdd import add
import schedule
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def job():
    # url需要拼接的时间戳
    time_mark = str(time.time()).replace('.', '')[:14]

    #
    url = 'https://36kr.com/api/newsflash?per_page=20&_=' + time_mark
    headers = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'acw_tc=276aedd115531411283923949e7f1a46008933ec9cec2b24f2daddbdbb3e94; kr_stat_uuid=Q3SeM25885685; new_user_guidance=true; device-uid=97ec0f20-4b8e-11e9-9234-cb743af39374; download_animation=1; TY_SESSION_ID=ed698e17-ddfd-4aff-bb2d-64c531ae62c2; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22Q3SeM25885685%22%2C%22%24device_id%22%3A%221699e6ce06218c-0e82b8e1663db7-18211c0a-2073600-1699e6ce064793%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%2C%22first_id%22%3A%221699e6ce06218c-0e82b8e1663db7-18211c0a-2073600-1699e6ce064793%22%7D; Hm_lvt_713123c60a0e86982326bae1a51083e1=1553141129,1553141142,1553141286,1553219309; Hm_lvt_1684191ccae0314c6254306a8333d090=1553141129,1553141142,1553141286,1553219309; identity_id=4879195981480050; krnewsfrontss=4d2d74d0091ff60e617fd4166414a28d; M-XSRF-TOKEN=b1d6c2bc4bfa259ca35867342f6532087b4d6898cda1809e7df646596ac26e10; SERVERID=6754aaff36cb16c614a357bbc08228ea|1553234382|1553234382; Hm_lpvt_713123c60a0e86982326bae1a51083e1=1553234384; Hm_lpvt_1684191ccae0314c6254306a8333d090=1553234384',
        'Host': '36kr.com',
        'Referer': 'https://36kr.com/newsflashes',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Tingyun-Id': 'Dio1ZtdC5G4;r=219323143'
    }

    response = requests.get(url=url, headers=headers, verify=False)
    result = json.loads(response.content.decode())
    print(len(result['data']['items']))
    for item in result['data']['items']:
        # 快讯id
        id = item['id']
        # 标题
        title = item['title']
        # 快讯描述,也是我们抓取的内容
        description = item['description']
        # 在这里判断是否应该发表文章
        if is_add(id):
            # 发表快讯并加入数据库
            print('发现新文章')
            print(id, title, description, )
            add(title, content=description)
            write_data(id, title)


# 将发表过的快讯添加到数据库
def write_data(id, title):
    mysqlHelper = MysqlHelper('localhost', 'root', '123456', 'kr36_db')
    mysqlHelper.connect()
    params = [id, title]
    sql = 'insert into News values(%s,%s) '
    count = mysqlHelper.insert(sql, params)
    if count > 0:
        print('成功写入数据库')


# 判断该快讯是否应该发表发表过
def is_add(id):
    '''

    :return: True 可以发表 False 已经发表过，无需再发表
    '''

    mysqlHelper = MysqlHelper('localhost', 'root', '123456', 'kr36_db')
    mysqlHelper.connect()
    params = [id]

    sql = 'select id from News where id =%s'
    result = mysqlHelper.fetchone(sql, params)
    if not result:
        return True
    return False


job()
print('程序开始－－－')
schedule.every(1).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
