#coding:utf-8

'''
样例程序，用户只需要设计每天需要进行的操作，不需要考虑各种时间切片问题
注：
在运行测试的过程中，策略讲作为变量传入
本策略在过去5日收盘价的均值大于上一日均值的情况下买入，剩下的时间卖出
'''
from TestEngine.TestEngine import Engine
def test(context,engine):
    print '当前运行时间',context.current_time#当前运行时间
    hs300s = context.DataModule.HS300s()[:3]#获取沪深300指数
    for security in hs300s.index:
        data = context.DataModule.stock_history_data(security)
        try:
            if sum(data.iloc[0:5].close)/5 > data.iloc[5].close:
                print security,engine.buy(str(security),volume= 100)
            else:
                print security,engine.sell(str(security),volume= 100)
        except:
            print security


if __name__ =='__main__':
    def history_trading_example():
        '''
        海知平台历史回测样例
        :return:
        '''
        #初始化回测引擎
        engine = Engine(user_name='海知平台测试接口样例',
                        password='Cloud25683',
                        #core = 'HaiZhi',
                        #type = 'HistoryTrading',
                        initial_time='2018-01-01',
                        end_date='2018-1-5',
                        initial_money = 1000000)
        #运行回测引擎的策略
        print engine.buy('600000',1000)
        engine.run_stratagy(test)

        #讲海知平台的回测交割单输出到csv文件
        #engine._core.history_to_csv()

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
    history_trading_example()
