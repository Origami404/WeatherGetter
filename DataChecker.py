import Logger


class DataInvalidError(Exception):
    fn_name = None

    def __init__(self, fn_name):
        self.fn_name = fn_name


def checked(fn):
    try:
        ret = fn()
        Logger.get_logger('DataChecker_value_check').info(f'In Func: {fn.__name__}, value: {str(ret)}')
    except:
        raise DataInvalidError(fn.__name__)
    if ret['status'] != 'ok':
        raise DataInvalidError(fn.__name__)
    return ret


# 用来模拟静态变量
class LastUpdateTime:
    time = None


# 先判断接口有没有更新再加入队列
# 加入的格式为{表名: {列名: 值 ... }}
def add_to_queue(queue, fn):
    data = checked(fn)
    if not data['update_time'] == LastUpdateTime.time:
        queue.put({fn.__name__[4:]: data})  # 因为是get_xxx, 所以用[4:]去掉get_
        Logger.get_logger('DataChecker_add_to_queue')\
            .info(f'New data! Add to queue, Last time: {LastUpdateTime.time}, This time: {data["update_time"]}')
        LastUpdateTime.time = data['update_time']


def write_sql(queue, insert_fn):
    while not queue.empty():
        data = queue.get()
        table_name = list(data.keys())[0]
        column_list = list(data[table_name].keys())
        column_list.remove('status')
        values_list = list(data[table_name].values())
        values_list.remove('ok')
        insert_fn(table_name, column_list, values_list)


'''
import queue
import WeatherGetter
q = queue.Queue(0)
add_to_queue(q, WeatherGetter.get_now)
print(q.get())
'''
