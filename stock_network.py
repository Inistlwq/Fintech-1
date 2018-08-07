#coding:utf-8
'''
计算资金流在整个网络中的流动情况
'''
from DB.DataInterface import DataInterface
import networkx as nx
import pandas as pd
#jiang HS300的数据读入内存
d  = DataInterface()
data = {}
for security in d.HS300s().index[:3]:
    data[security] = d.stock_history_data(security)
print (len(data))
#获取交易日列表
trade_date_list = []
for security in data:
    for date in data[security].index:
        if date not in trade_date_list:
            trade_date_list.append(date)
print len(trade_date_list)
df = pd.DataFrame()
print '----------'
for date in trade_date_list:
    temp_mf = 0.
    for security in data:
        if date in data[security].index:
            print data[security].ix[date]['p_change']
            if data[security].ix[date]['p_change'] > 0:
                print data[security].ix[date]['close'],data[security].ix[date]['volume']
                temp_mf += float(data[security].ix[date]['close'])*float(data[security].ix[date]['volume'])
                print temp_mf
            elif data[security].ix[date]['p_change'] < 0:
                print data[security].ix[date]['close'], data[security].ix[date]['volume']
                temp_mf -=  float(data[security].ix[date]['close'])*float(data[security].ix[date]['volume'])
                print temp_mf
    df = df.append(pd.DataFrame({'date':[date],
                                 'mf':[temp_mf]}))
#df = df.set_index(date)
df.to_csv('global_mf.csv')
print df