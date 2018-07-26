#coding:utf-8
class TradeModule(object):
    def __init__(self,StateModule,DataModule):
        self._StateModule = StateModule
        self._DataModule = DataModule

    def tax(self,money):
        pass

    def fee(self,money):
        pass

    def buy(self):
        print self._StateModule.current_time

    def sell(self):
        print self._StateModule.current_time