'''发表快讯,不需要请求头，可以实现自动发送'''
import random
import requests
import json
import time


def add(title, content):
    '''
        info[pid]: 11
        info[ty]: 12
        info[tty]: 0
        info[ttty]: 0
        info[title]: 信息标题title
        info[seokeywords]: 内容关键字－title
        info[seodescription]: 内容简介-content
        info[ftitle]: 转载
        info[hits]: 1500-2000随机
        info[content]: 信息内容content
        info[sendtime]: 2019-03-22 12:32:53
        info[disorder]: 0
        dosubmit: 马上发布
        '''
    url = 'http://xiouhui.com/web_manage/news_add.php?pid=11&ty=12&tty=0&ttty=0'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        # 'Cookie': ' sys_guestid=1552825744; UM_distinctid=1698ba0ffb77a-085c7f08339b19-18211c0a-1fa400-1698ba0ffb8192; PHPSESSID=t31rpg8vkcaf833dru6atdmdl7; CNZZDATA1273247885=1735094777-1552825778-%7C1553234508',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryWoAdkwB4ikRCVH2p',
    }

    form_data = {
        'info[pid]': '11',
        'info[ty]': '12',
        'info[tty]': '0',
        'info[ttty]': '0',
        'info[title]': title,
        'info[seokeywords]': title,
        'info[seodescription]': content,
        'info[ftitle]': '转载',
        'info[hits]': str(random.randint(1500, 2000)),
        'info[content]': content,
        'info[sendtime]': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'info[disorder]': '0',
        'dosubmit': '马上发布'
    }

    result = requests.post(url=url, data=form_data).content.decode()
    print(result)

# add('标题，内容就一点点','我就是内容')
