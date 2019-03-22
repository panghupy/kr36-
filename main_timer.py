'''主程序：定时器,实现每半小时运行一次爬虫程序并发表不重复文章'''

import schedule
from kr36_spider import job

schedule.every(2).minutes.do(job)
while True:
    schedule.run_pending()
