#coding:utf-8
'''
定义数据库模型
初始化数据库
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Float,Date,ForeignKey,DateTime,Boolean,BigInteger
from sqlalchemy.orm import relationship
import os
Base = declarative_base()

class Trade_calendar(Base):
    __tablename__ = 'trade_calendar'

    id = Column(String,primary_key=True)

    exchange_id = Column(String)
    cal_date = Column(Date)
    isopen = Column(Boolean)
    pretrade_date = Column(Date)

class Stock(Base):
    __tablename__ = 'stock'

    code = Column(String,primary_key=True)#股票id,主键

    security = Column(String)
    name = Column(String(20))#股票名称
    exchange_id = Column(String)
    list_date =  Column(Date)
    delist_date = Column(Date)
    list_status = Column(String)
    is_hs = Column(String)
    history = relationship('StockHistory',backref = 'history')
    tick_data = relationship('Tick_data',backref = 'tick_data')

class StockHistory(Base):
    __tablename__ = 'stock_history'

    id = Column(String,primary_key=True)#主键,结构是ts_code+date

    stock = Column(String,ForeignKey('stock.security'))

    date = Column(DateTime)  # 日期
    open = Column(Float)  # 开盘
    close = Column(Float)  # 收盘
    high = Column(Float)  # 最高检
    low = Column(Float)  # 最低价
    price_change = Column(Float)  # 价格变动
    pct_change = Column(Float)  # 涨跌幅
    volume = Column(Integer)  # 成交量
    amount = Column(Float)

    turnover_rate = Column(Float)
    volume_ratio = Column(Float)
    pe = Column(Float)
    pe_ttm = Column(Float)
    pb = Column(Float)
    ps = Column(Float)
    ps_ttm = Column(Float)
    total_share = Column(Float)
    float_share = Column(Float)
    free_share = Column(Float)
    total_mv = Column(Float)
    circ_mv = Column(Float)

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
    import settings
    c = settings.ConfigModule()
    print c.settings
    db_path = c.settings['DB']['db_path']
    engine = create_engine('sqlite:///%s' % db_path, echo=False, encoding='utf-8')
    Base.metadata.create_all(engine)
    for item in Base.metadata.tables:
        print (item)