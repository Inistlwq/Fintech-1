#coding:utf-8
from HaiZhiInterface import HaiZhiTestEngine
from DB.DataInterface import DataInterface
from sklearn import svm
from sklearn import preprocessing
import datetime
#初始化回测引擎
security = '600848'
class strategy(object):
    def __init__(self):
        #初始化回测引擎
        self._name = '基于SVM的股价预测策略'
        self._T = HaiZhiTestEngine(user_id='18126352115',  #初始化回测引擎
                                   password='Cloud25683',
                                   type='HistoryTrading')
        self._T.current_time = '2016-01-01'#设定回测开始时间
        self._T.del_stratagy(self._name)
        self._T.create_stratagy(self._name)
        self._T.set_stratagy(self._name)
    @property
    def test_engine(self):
        return self._T

    def data_pre(self):
        windows = 30
        di = DataInterface()
        data = di.stock_history_data(security)
        data = data[:self._T.current_time]
        data = [data.ix[index]['p_change'] for index in data.index]
        #生成训练数据
        X = []
        y = []
        for i in range(1,len(data[1:-windows])):
            if len(data[i:i+windows]) == windows:
                X.append(data[i:i+windows])
                if data[i+windows+1] > 0:
                    y.append(1)
                else:
                    y.append(0)
            else:
                break
        pos = [item for item in y if item ==1]
        neg = [item for item in y if item ==0]
        print len(pos),len(neg)
        #print y
        #生成测试数据
        test_x = [data[0:windows]]
        return X,y,test_x
    def run(self):
        while datetime.datetime.strptime(self._T.current_time,'%Y-%m-%d') < datetime.datetime.today():
            X, y, test_x = s.data_pre()
            print len(X)
            clf = svm.SVC()
            scaler = preprocessing.StandardScaler().fit(X)
            clf.fit(scaler.transform(X),y)
            print self._T.current_time
            if clf.predict(scaler.transform(test_x)) == 1:
                print self._T.buy(code =security,volume=10000,price_type='now_price',date=self._T.current_time)
            else:
                print self._T.sell(code =security,volume=10000,price_type='now_price',date=self._T.current_time)
            self._T.shift_current_time(1)

if __name__ =='__main__':

    s = strategy()
    s.run()
    print s._T.history_to_csv()