#coding:utf-8
import pandas as pd

class TradeModule(object):
    def __init__(self,StateModule,DataModule):
        self._StateModule = StateModule
        self._DataModule = DataModule

    def tax(self,money):
        tax = money *0.001
        return tax
    def fee(self,money):
        fee = money * 0.0003
        return round(fee, 3)

    def buy(self,security,volume,price_type='now_price',price=None):
        #读入股票数据
        shd = self._DataModule.stock_history_data(security)
        if self._StateModule.current_time not in shd.index:#当日不可交易
            return 'fail,stock does not trade today'
        else:#当日可以交易,按照收盘价交易
            #统计交易数据
            name = self._DataModule.stock_name(security)
            buy_price = shd.loc[self._StateModule.current_time]['close']
            cost = buy_price*volume
            if cost > self._StateModule.current_money:
                return '购买失败，现金不足'
            fee = self.fee(cost)
            tax = 0
            other_fee = 0
            security_holding = self._StateModule.security_holding(security)
            #填写交割单
            temp = pd.DataFrame({'timestamp':[self._StateModule.current_time],
                               'security':[security],
                                'name':[name],
                                'operation':['买入'],
                               'price_order':[buy_price],
                               'price_deal':[buy_price],
                                 'volume': [volume],
                               'fund_deal':[cost],
                               'fee':[fee],
                               'tax':[tax],
                               'other_fee':[0],
                               'security_holding':[security_holding+volume],
                               'happen_fund':[0-cost-fee-tax-other_fee],
                               'fund_remain':[self._StateModule.current_money-cost-fee-tax-other_fee]})
            temp = temp.set_index('timestamp')
            self._StateModule.trade_log = self._StateModule.trade_log.append(temp)
            #更新StateModule
            self._StateModule.current_money -= (cost+fee+tax+other_fee)
            #print self._StateModule.trade_log
            return '购买成功'
    def sell(self,security,volume,price_type='now_price',price=None):
        # 读入股票数据
        shd = self._DataModule.stock_history_data(security)
        if self._StateModule.current_time not in shd.index:  # 当日不可交易
            return 'fail,stock does not trade today'
        else:  # 当日可以交易,按照收盘价交易
            if volume > self._StateModule.security_can_trade(security):
                return '卖出失败，股票持仓不足'
            # 统计交易数据
            name = self._DataModule.stock_name(security)
            buy_price = shd.loc[self._StateModule.current_time]['close']
            cost = buy_price * volume
            fee = self.fee(cost)
            tax = self.tax(cost)
            other_fee = 0
            security_holding = self._StateModule.security_holding(security)
            # 填写交割单
            temp = pd.DataFrame({'timestamp': [self._StateModule.current_time],
                                 'security': [security],
                                 'name': [name],
                                 'operation': ['卖出'],
                                 'price_order': [buy_price],
                                 'price_deal': [buy_price],
                                 'volume': [volume],
                                 'fund_deal': [cost],
                                 'fee': [fee],
                                 'tax': [tax],
                                 'other_fee': [0],
                                 'security_holding': [security_holding - volume],
                                 'happen_fund': [cost - fee - tax - other_fee],
                                 'fund_remain': [self._StateModule.current_money + cost - fee - tax - other_fee]})
            temp = temp.set_index('timestamp')
            self._StateModule.trade_log = self._StateModule.trade_log.append(temp)
            # 更新StateModule
            self._StateModule.current_money -= (cost + fee + tax + other_fee)
            # print self._StateModule.trade_log
            return '卖出成功'