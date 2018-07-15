import logging
import os
import datetime
import sys
import tarfile
import shutil


class Static:
    __my_format = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')

    file_handler = logging.FileHandler(os.getcwd() + '/WeatherGetter.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(__my_format)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(__my_format)

    logger_cache = {}


def get_logger(name):
    if name in Static.logger_cache:
        return Static.logger_cache[name]
    else:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(Static.file_handler)
        logger.addHandler(Static.stdout_handler)
        Static.logger_cache[name] = logger
        return logger


# TODO 改好看一点
def cut_log():
    # 因为预订是4:30 切割log文件, 所以要获得昨天的日期
    base_name = f'WeatherGetter-{datetime.date.today() + datetime.timedelta(-1)}'
    old_path = f'{os.getcwd()}/{base_name}'

    os.rename('WeatherGetter.log', f'{base_name}.log')  # 按时间重命名
    compress_log()  # 压缩
    make_logs_folder()  # 测试有没有文件夹, 没有就创建
    shutil.move(f'{old_path}.tar.gz', f'{os.getcwd()}/logs/{base_name}.tar.gz')  # 旧日志移动到./logs
    get_logger('Logger_cut_log').debug('Has cut log file, and I am the first!')  # 然后打一条日志每天抢第一(滑稽)


def compress_log():
    time = datetime.date.today() + datetime.timedelta(-1)
    with tarfile.open(f'./WeatherGetter-{time}.tar.gz', 'w:gz') as tar:
        tar.add(f'WeatherGetter-{time}.log')


def make_logs_folder():
    path = os.getcwd() + '/logs'
    if not os.path.exists(path):
        os.makedirs(path)
