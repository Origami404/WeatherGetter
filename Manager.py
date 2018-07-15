import queue
from apscheduler.schedulers.blocking import BlockingScheduler
import DBWriter
import DataChecker
import WeatherGetter
import Logger


class Scheduler:
    def __init__(self):
        self.todo_queue = queue.Queue(0)
        self.schedule = BlockingScheduler()
        # 获取数据
        self.schedule.add_job(lambda: DataChecker.add_to_queue(self.todo_queue, WeatherGetter.get_now),
                              'interval', seconds=1195)
        self.schedule.add_job(lambda: DataChecker.add_to_queue(self.todo_queue, WeatherGetter.get_air),
                              'interval', seconds=3610)  # 跟其他人错开10秒
        self.schedule.add_job(lambda: DataChecker.add_to_queue(self.todo_queue, WeatherGetter.get_lifestyle),
                              'cron', hour='8,11,18', minute='01,21,41')  # 每天的8, 11, 18点左右求一次
        self.schedule.add_job(lambda: DataChecker.add_to_queue(self.todo_queue, WeatherGetter.get_sun_and_moon()),
                              'cron', hour=4, minute=3)  # 错开3分钟
        # 写入sql
        self.schedule.add_job(lambda: DataChecker.write_sql(self.todo_queue, DBWriter.insert),
                              'interval', seconds=3630)
        # 分割日志
        self.schedule.add_job(Logger.cut_log, 'cron', hour=0, minute=0)


DBWriter.init()
sch = Scheduler()
Logger.get_logger('Manager')\
    .info('Init System successfully! WeatherGetter Beta 1.0 now ready to run! Github@Origami404!')
sch.schedule.start()

