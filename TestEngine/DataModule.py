#coding:utf-8
from DB.DataInterface import DataInterface
import datetime
import pandas as pd
class DataModule(object):
    def __init__(self,StateModule):
        self._di = DataInterface()
        self._StateModule = StateModule

    def stocks(self):
        return self._di.stocks()

    def stock_history_data(self,security):
        '''

        :param security:
        :return:
        '''
        data = self._di.stock_history_data(security=security)
        #日期筛选，只返回当前回测时间之前的数据
        before = self._StateModule.current_time
        while True:#pandas的时间切片会出现一些神奇的bug,我也是一脸懵逼
            try:
                before -= datetime.timedelta(days=1)
            except:
                return pd.DataFrame()
            if before in data.index:
                x = data.truncate(before=before)
                y = data[:before]
                if len(x) > len(y):
                    return x
                else:
                    return y

    def HS300s(self,date = None):
        return self._di.HS300s()

if __name__ =='__main__':
    import StateModule
    StateModule = StateModule.StateModule(initial_time = '2018-5-31',initial_money=1000000)
    DM = DataModule(StateModule)
    print DM.stock_history_data('600008')