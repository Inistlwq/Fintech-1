#coding:utf-8
'''
定义数据库模型
初始化数据库
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Float,Date,ForeignKey,DateTime
from sqlalchemy.orm import relationship
import os
Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stock'

    security = Column(String,primary_key=True)#股票id,主键
    name = Column(String(20))#股票名称
    history = relationship('StockHistory',backref = 'history')

class StockHistory(Base):
    __tablename__ = 'stock_history'

    id = Column(String,primary_key=True)#主键,结构是security+date
    stock = Column(String,ForeignKey('stock.security'))
    date = Column(DateTime)  # 日期
    open = Column(Float)  # 开盘
    close = Column(Float)  # 收盘
    high = Column(Float)  # 最高检
    low = Column(Float)  # 最低价
    volume = Column(Integer)  # 成交量
    price_change = Column(Float)  # 价格变动
    p_change = Column(Float)  # 涨跌幅
    ma5 = Column(Float)  # 5日均价
    ma10 = Column(Float)
    ma20 = Column(Float)
    v_ma5 = Column(Float)  # 5日均量
    v_ma10 = Column(Float)
    v_ma20 = Column(Float)
    turnover = Column(Float)  # 换手率

class HS300s(Base):
    __tablename__ = 'HS300s'

    id = Column(String,primary_key=True)#主键,结构是security+date
    security = Column(String)
    name = Column(String)
    date = Column(DateTime)#日期
    weight = Column(Float)#权重

class Tick_data(Base):
    __tablename__ = 'stock_tick'

    id = Column(String, primary_key=True)  # 主键,结构是security+time
    stock = Column(String, ForeignKey('stock.security'))

    time = Column(DateTime)
    price = Column(Float)
    change = Column(Float)
    volume = Column(Integer)
    amount = Column(Float)
    type = Column(String)

if __name__ =='__main__':
    '''
    在数据库中初始化表
    '''
    DB_name = 'test.sqlite3'
    db_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], DB_name)
    engine = create_engine('sqlite:///%s' % db_path, echo=False, encoding='utf-8')
    Base.metadata.create_all(engine)
    for item in Base.metadata.tables:
        print (item)