#coding:utf-8
import datetime

def standard_time_input(time):
    '''
    标准化输入的时间
    :param time:
    :return:
    '''
    print(type(time))
    if isinstance(time, datetime.datetime):
        pass
    elif isinstance(time,datetime.date):
        time = datetime.datetime(time)
    elif isinstance(time, str):
        time = datetime.datetime.strptime(time, "%Y-%m-%d")
    else:
        raise TypeError('The time input should be a datetime.timestamp or a string!')
    return time

def standard_trading_section(start = None,end = None,time_length = 60):
    '''
    start 和 end 仅能二选一，输出以开始时间或者结束时间为基准的time_length个时间间隔的交易日区间
    :param start: 起始时间
    :param end: 结束时间
    :param time_length:包含的交易日数量
    :return:输出包含time_length个交易日的起始时间和结束时间
    '''
    if start and end:
        raise ValueError('there can only be a start or a end ,they can not appear both')
    elif start and not end:
        start = standard_time_input(start)
        end = start
        while time_length:
            if end.weekday() == 5 or end.weekday() == 6:
                end = end - datetime.timedelta(days=1)
            else:
                end = end - datetime.timedelta(days=1)
                time_length -= 1
    elif not start and end:
        end = standard_time_input(end)
        start = end
        while time_length:
            if start.weekday() == 5 or start.weekday() == 6:
                start = start - datetime.timedelta(days=1)
            else:
                start = start - datetime.timedelta(days=1)
                time_length -= 1
    else:
        return
    return start,end
