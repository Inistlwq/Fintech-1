#coding:utf-8
import sys
import os
project_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
sys.path.append(project_path)

from TestEngine.TestEngine import Engine
import pandas as pd
import numpy as np


def distance(a,b):
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a-b)

def DTW_distance(x,y):
    dtw = np.zeros((len(x)+1,len(y)+1))

    for i in range(0,len(x)+1):
        for j in range(0,len(y)+1):
            dtw[i, j] = float('inf')

    dtw[0,0] = 0

    for i in range(1,len(x)+1):
        for j in range(1,len(y)+1):
            cost = distance(x[i-1],y[j-1])

            dtw[i,j] = cost+np.min([dtw[i-1,j],dtw[i,j-1],dtw[i-1,j-1]])
    return dtw[1:,1:]

if __name__=='__main__':
    engine = Engine(user_name='海知平台测试接口样例',
                    password='Cloud25683',
                    core='HaiZhi',
                    type='HistoryTrading',
                    initial_time='2018-06-4',
                    end_date='2018-1-5',
                    initial_money=1000000, )

    dm = engine.context.DataModule

    x = dm.stock_history_data('000001')[:10]
    z = dm.stock_history_data('000002')[:10]
    y = dm.stock_history_data('000004')[:10]

    x = pd.Series(list(x['pct_change']), index=x.index)
    y = pd.Series(list(y['pct_change']), index=y.index)
    z = pd.Series(list(z['pct_change']), index=z.index)

    print x.corr(y)
    print DTW_distance(x,y)

    print x.corr(z)
    print DTW_distance(x,z)

    print y.corr(z)
    print DTW_distance(y,z)


