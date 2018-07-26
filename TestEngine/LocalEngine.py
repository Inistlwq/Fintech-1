#coding:utf-8
class LocalEngine(object):

    def __init__(self,StateModule,DataModule,TradeModule):
        self._StateModule = StateModule
        self._DataModule = DataModule
        self._TradeModule = TradeModule

    def buy(self,security,volume,price_type='now_price',price=None):
        return  self._TradeModule.buy(security,volume,price_type,price)

    def sell(self,security,volume,price_type='now_price',price=None):
        return self._TradeModule.sell(security,volume,price_type,price)

    @property
    def current_time(self):
        return self._StateModule.current_time