# Fintech项目说明
---
## 项目总体说明
---
##项目安装说明
1.推荐使用numpy 1.14.5 更高版本的numpy会造成版本之间不匹配的问题
---
## 项目结构
---
## 项目模块说明
#### DB（database）
1.DB（databas）是数据模块，目前项目中使用sqlalchemy作为程序与数据库之间的接口，数据库使用sqlite3存储数据。

1.1**DB 简要说明**

|- models.py #定义数据库scheme
|- lanuch.py #用于初始化化数据库scheme，初始化数据库中的数据
|- DataInterface.py #数据模块外部接口
|- test.sqlite3 #数据库文件（因为目前使用的时文件数据库）

```
注：
    1.项目本身是支持mysql 和oracle数据库的，但是考虑到单机使用，直接使用文件数据库相比之下更加方便。
    2.在初始化数据库时，需要先运行models.py初始化数据库表，在运行launch初始化数据库中的数据
```

2.**DB数据库存储说明**
*股票
```python
class Stock(Base):
    __tablename__ = 'stock'#数据表名称

    security = Column(String,primary_key=True)#股票id,主键
    name = Column(String(20))#股票名称
    history = relationship('StockHistory',backref = 'history')
```
*股票历史数据
```python
class StockHistory(Base):
    __tablename__ = 'stock_history'
    id = Column(String,primary_key=True)#主键,结构是security+date
    stock = Column(String,ForeignKey('stock.security'))
    date = Column(DateTime)  # 日期
    open = Column(Float)  # 开盘
    close = Column(Float)  # 收盘
    high = Column(Float)  # 最高检
    low = Column(Float)  # 最低价
    volume = Integer  # 成交量
    price_change = Column(Float)  # 价格变动
    p_change = Column(Float)  # 涨跌幅
    ma5 = Column(Float)  # 5日均价
    ma10 = Column(Float)
    ma20 = Column(Float)
    v_ma5 = Column(Float)  # 5日均量
    v_ma10 = Column(Float)
    v_ma20 = Column(Float)
    turnover = Column(Float)  # 换手率
```

3.**DB 外部接口说明**

DB的外部文件接口参考DataInterface.py,在使用接口的时候需要先生成接口对象:
```python
di = DataInterface()
```
函数接口说明如下：

*返回数据中所有的股票代码
```python
def stocks(self): #函数返回当前数据库中所有股票的列表，返回的数据格式时pandas.DataFrame
```
*返回某只股票的所有历史数据
```python
stock_history_data(self,security): #传入股票代码，返回数据库中所有的股票数据，返回的数据格式为pandas.DataFrame
```

####海知回测引擎与实盘模拟引擎接口(HaiZhiInterface)
1.1 **简要说明**

|- HaiZhiTestEngine.py #测试引擎总接口，可以选择历史回测或者时实盘模拟
|- HistoryTrading.py #回测引擎接口
|- RealTimeTrading.py #实盘模拟引擎接口

2.2 **接口说明**


