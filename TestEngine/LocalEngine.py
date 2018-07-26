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

    def history_to_csv(self, file_name = '交割单(local)'):
        trade_log = self._StateModule.trade_log
        trade_log = trade_log.reset_index()
        trade_log = trade_log[['timestamp',
                             'security',
                             'name',
                             'operation',
                             'price_order',
                             'price_deal',
                             'volume',
                             'fund_deal',
                             'fee',
                             'tax',
                             'other_fee',
                             'security_holding',
                             'happen_fund',
                             'fund_remain']]
        # 转换列表名
        trade_log = trade_log.rename(columns={'timestamp': '成交时间',
                                              'security': '代码',
                                              'name': '名称',
                                              'operation': '操作',
                                              'price_order': '委托价',
                                              'price_deal': '成交价',
                                              'volume': '成交量',
                                              'fund_deal': '成交金额',
                                              'fee': '手续费',
                                              'tax': '印花税',
                                              'other_fee': '其他杂费',
                                              'security_holding': '证券余额',
                                              'happen_fund': '发生金额',
                                              'fund_remain': '现金余额'})

        trade_log.to_csv('%s.csv'%file_name, sep=",", index=False, encoding='utf-8')