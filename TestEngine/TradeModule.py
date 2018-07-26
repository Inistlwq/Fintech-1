#coding:utf-8
class TradeModule(object):
    def __init__(self,StateModule,DataModule):
        self._StateModule = StateModule
        self._DataModule = DataModule

    def tax(self,money):
        pass

    def fee(self,money):
        pass

    def buy(self,security,volume,price_type='now_price',price=None):
        shd = self._DataModule.stock_history_data(security)
        if self._StateModule.current_time not in shd.index:
            return 'fail,stock does not trade today'
        else:
            return '?',shd.loc[self._StateModule.current_time]

    def sell(self,security,volume,price_type='now_price',price=None):
        shd = self._DataModule.stock_history_data(security)
        if self._StateModule.current_time not in shd.index:
            return 'fail,stock does not trade today'
        else:
            return '?', shd[self._StateModule.current_time]