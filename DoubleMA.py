#coding:utf-8

'''
双均线策略
'''

import pandas as pd
import numpy as np
from TestEngine.TestEngine import Engine

def ma(df,time_length):
    '''
    按照收盘价计算股票的移动平均值
    :param df: 股票历史数据
    :param time_length: 窗口长度
    :return:
    '''
    if time_length > len(df):
        return False
    else:
        df = df[0-time_length:]
        return np.sum(df.close)/time_length

def double_ma(context,engine):
    l = 60
    s = 10
    print '当前运行时间',context.current_time#当前运行时间
    hs300s = context.DataModule.HS300s()#获取沪深300指数
    for security in hs300s.index:
        shd = context.DataModule.stock_history_data(security)
        lma =ma(shd,l)
        sma = ma(shd,s)
        lma_l = ma(shd[:-1],l)
        sma_l = ma(shd[:-1],s)
        if lma and sma and lma_l and sma_l:
            #print lma ,sma ,lma_l ,sma_l
            if lma < sma and lma_l > sma_l:#5日均线超过了60日均线
                print engine.buy(code = str(security),volume=1000)
            elif lma > sma and lma_l < sma_l:#60日均线超过了5日均线
                print engine.sell(code=str(security), volume=1000)

if __name__ =='__main__':
    def history_trading_example():
        '''
        海知平台历史回测样例
        :return:
        '''
        #初始化回测引擎
        engine = Engine(user_name='海知平台测试接口样例',
                        password='Cloud25683',
                        core = 'HaiZhi',
                        type = 'HistoryTrading',
                        initial_time='2017-01-01',
                        #end_date='2018-1-1',
                        initial_money = 1000000)

        engine.run_stratagy(double_ma)

        print engine._core.history_to_csv()

    def realtime_trading_example():
        '''
        海知平台实盘模拟样例
        :return:
        '''
        engine = Engine(user_name='海知平台测试接口样例',
                        password='Cloud25683',
                        core='HaiZhi',
                        type='RealTimeTrading',
                        initial_money=1000000)
        # 运行实盘模拟引擎的策略
        engine.run_stratagy(test)
    #realtime_trading_example()
    #history_trading_example()


    def other():
        #数据准备
        engine = Engine(user_name='海知平台测试接口样例',
                        password='Cloud25683',
                        # core = 'HaiZhi',
                        # type = 'HistoryTrading',
                        initial_time='2017-07-01',
                        #end_date='2018-1-5',
                        initial_money=1000000)

        dm = engine.context.DataModule
        security = '601390'
        name = dm.stock_name(security)
        print engine.context.current_time
        data = dm.stock_history_data(security)
        print data

        #显示数据
        import matplotlib.pyplot as plt
        from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        daysFmt = DateFormatter('%m-%d-%Y')

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot_date(data.index, data.close, '-')

        # format the ticks
        ax.xaxis.set_major_formatter(daysFmt)
        ax.autoscale_view()

        # format the coords message box
        def price(x):
            return '$%1.2f' % x

        ax.fmt_xdata = DateFormatter('%Y-%m-%d')
        ax.fmt_ydata = price
        ax.grid(True)

        fig.autofmt_xdate()
        print name
        plt.title(name)
        plt.show()


    #other()
    history_trading_example()
