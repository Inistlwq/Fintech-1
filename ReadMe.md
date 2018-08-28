#海知智能投资接口说明#

#Overview#

Fintech是一套模拟投资系统,基于海知平台的模拟投资系统进行投资。在框架下，可以非常方便的制定模拟投资策略。用户只需要定义每一天需要执行的操作，系统会自动完成日期跳转等复杂的控制过程，同时框架运行在本地，可以很方便的制定高度自由的策略。避免了那些在线编辑的量化网站无法高度自由使用自己定义的库的局限性。
#INSTALL#
框架有一些依赖包,请在运行框架之前安装：
-    tushare(版本不低于1.2.11)
-    bs4(用于支持tushare)
-    xlrd（用于支持tushare）
-    requests(用于支持tushare)
-    sqlalchemy(数据库ORM框架)
-    alembic（与sqlalchemy相对应的migrate框架）
上述框架还会捆绑安装pandas,numpy等常用的科学计算框架。
**注：整个框架的核心数据结构是pandas DataFrame,几乎所有的数据都包裹在DataFrame当中，因此需要使用者熟悉pandas的基本操作。**

**如果你是直接从GitHub克隆的本项目，那么项目将不会自带数据库，需要用户自行初始化数据库**操作步骤如下：
1.  生成数据库
    默认的数据库是python自带的sqlite3文件数据库。由于系统针对的是个人用户，因此sqlite3完全可以满足用户的全部需求，如果想使用其他数据库，请参考sqlalchemy的官方文档，将项目连接至其他数据库

    生成数据库表只需要直接运行DB.moelds.py即可
2.  下载数据
    数据源来自tushare,想要下载数据只需要直接运行DB.launcher.py即可

#Tutorial#

在本节将会从一个最简单的策略开始，为你完整的演示如何完成一个自己的模拟投资策略

##快速开始##

在Fintech框架下，你只需要考虑设计策略每天应该执行什么样的操作，不需要考虑时间跳转等复杂的控制逻辑。
我们先从最简单的策略开始————对于一只股票，如果他过去5天的收盘价均价比昨天的收盘价低，则买入该股票，反之卖出。
在开始编辑策略之前，第一步，我们需要初始化模拟投资引擎。
```python
from TestEngine.TestEngine import Engine
engine = Engine(user_name='***',#海知平台用户名
                password='***',#密码
                core = 'HaiZhi',#选择海知接口作为模拟投资核心引擎
                type = 'HistoryTrading',#选择历史回测模式
                initial_time='2017-01-01',#历史回测开始时间
                end_date='2018-1-1',#历史回测结束时间，默认为今天
                initial_money = 1000000)#初始资金
```
执行上面的代码就可以创建一个新的回测引擎实例。

初始化了引擎之后，我们就可以开始编辑自己的策略了，我们为策略起名tutorial。
**注：在本框架下，策略可以随意起名。但是需要注意，必须声明传入`context`和`engine`两个参数。也就是说，声明传入上述两个参数的函数都可以作为策略被调用运行。**
```python
def tutorial(context,engine):
    print '当前运行时间',context.current_time#打印当前运行时间
    hs300s = context.DataModule.HS300s()#获取沪深300指数
    for security in hs300s.index:#遍历沪深300股票列表里的股票代码
        data = context.DataModule.stock_history_data(security)#获取股票历史交易数据
        if sum(data.iloc[0:5].close)/5 > data.iloc[5].close:
            print security,engine.buy(str(security),volume= 100)
        else:
            print security,engine.sell(str(security),volume= 100)
```

细心的读者会发现，我们为编写的策略传入了两个参数，`context`和`engine`。我们会在今后详细解释这两个参数的作用。
目前我们只需要知道，`context`主要用于数据交互,`engine`主要用于执行股票买卖等操作。

现在我们执行下面的代码运行我们的策略同时将运行的结果输出到历史交割单文件中。得到了历史交割单文件，就可以通过海之平台的历史诊断功能对策略进行评测了！

```python
engine.run_stratagy(tutorial)#运行策略
print engine._core.history_to_csv()#将交割单输出
```
需要注意的是，在运行策略的时候，我们只需要向引擎传入策略名。开始运行之后，引擎会自动在每个历史日期自动运行我们的策略。

##与回测引擎交互

在上述例子中，假设我们不想操作HS300s中所有的300支股票，而是想操作我们选定的一些股票。最简单的实现方式是在策略中声明一个局部变量，这个变量中存储我们想要操作的股票列表，另一种更加高级的实现方式是向引擎传入一个全局变量，这样我们在回测过程中，每一次重新调用策略，策略都可以对这个全局变量进行操作。很显然，这样的方式可以让我们动态的在不同的日期之间保持一些数据。在很多时候，全局变量是不可代替的。

在上一节当中，我们提到过`engine.context`是用来进行数据交互的类。其中，`context.user_data`是一个字典类型，用户可以将自定义的数据保存在`context.user_data`当中，通过这种方式，`context.user_data`会作为回测引擎的全局变量，保证回测策略在不同的交易日之间可以共享一些数据。
下面的代码就是将股票列表传入回测引擎当中的示例。
```python
engine.context.user_data['stock_list'] = ['600848','600847']
```
现在我们在策略中通过直接访问`context.user_data['stock_list']`就能查看到我们之前传入的用户变量。我们可以再策略运行中改变这个变量，也可以在策略开始之前传入用户自定义的变量.想要在策略开始之前存储一写变量，只需要在`engine.run_stratagy()`之前，在`context.user_data`存储数据即可。

##总结

至此，你已经学会如何使用框架最基本的功能进行模拟投资了。不难发现，框架给予了用户很大的自由度，你可以在使用框架的同时使用各种其他第三方库和自定义库，使你的研究更加方便自由！

我们将在下面的内容中详细的介绍框架的数据接口以及交易接口。

#数据接口

在设计策略的过程中，`engine.context.DataModule`是框架的数据接口对象，该对象会返回用户要求的股票历史数据，但是，仅能获得在历史回测交易日之前的数据。在上一节的例子当中，我们的历史回测从2017-1-1开始到2018-1-1结束。那么，当我们的策略运行到2017-5-5日的时候，策略最多只能获取到2017-5-5日之前（不包括2017-5-5）的数据。这样做的目的是防止用户因为自己的设计失误，用未来的数据‘预测’历史。

`engine.context.DataModule`目前主要有以下的函数功能

函数名|函数说明|
:-----|:-----|
DataModule.stocks|返回数据库中所有股票的列表
DataModule.trade_cal|返回数据库中的交易日历def你哦他
DataModule.HS300s|返回数据库中目前的HS300s股票列表
DataModule.stock_history_data|返回数据库中代码为security的股票历史行情
DataModule.stock_name|返回数据库中代码为security的股票历史名称

###`DataModule.stocks()`

  传入参数：无

  返回：

  变量名|变量类型|变量说明|
  :-----|:-----|:-----|
  code|str|股票代码（包括交易所代码后缀）
  security|str|股票数字代码（无股票交易所代码）
  name|str|股票中文名称
  exchange_id|str|交易所代码
  list_date|str|股票上市日期
  delist_date|str|股票退市日期
  list_status|str|股票当前的交易情况（挂牌，停牌，退市）
  is_hs|str|是否沪深港通标的，N否 H沪股通 S深股通

###`DataModule.trade_cal()`

  传入参数：无

  返回：

  变量名|变量类型|变量说明|
  :-----|:-----|:-----|
  exchange_id|str|交易所代码：SSE上交所 SZSE深交所
  cal_date|str|日历日期
  is_open|boolean|是否交易
  pretrade_date|str|上一个交易日

###`DataModule.stock_history_data(security)`
传入参数:

变量名|变量类型|变量说明|
:-----|:-----|:-----|
security|str|股票代码（不包含交易所代码）

返回：

变量名|变量类型|变量说明|
:-----|:-----|:-----|
date|datetime.datetime|交易日期
open|float|开盘价
close|float|收盘价
high|float|最高价
low|float|最低价
pre_close|float|昨收价
change|float|涨跌额
pct_change|float|涨跌幅
vol|float|成交量 （手）
amount|float|成交额 （千元）
turnover_rate|float|换手率
volume_ratio|float|量比
pe|float|市盈率（总市值/净利润）
pe_ttm|float|市盈率（TTM）
pb|float|市净率（总市值/净资产）
ps|float|市销率
ps_ttm|float|市销率（TTM）
total_share|float|总股本 （万）
float_share|float|流通股本 （万）
free_share|float|自由流通股本 （万）
total_mv|float|总市值 （万元）
circ_mv|float|流通市值（万元）

#交易接口
需要注意的是，对于交易接口，无论是实盘模拟还是历史回测，都不需要输入交易的时间．实盘模拟只能在当前日期买卖，历史回测则会在回测引擎的当前日期进行买卖．可以通过`context.current_time`查看回测引擎的当前时间．

目前接口只提供限价买卖（包括历史和实盘），定价买卖还在测试当中．

函数说明：

函数名|函数说明|
:-----|:-----|
engine.buy|现价买入
engine.sell|现价卖出

###`engine.buy(security,volume,price_type='now_price',price=None,date=None,effect_term = 1)`

传入参数：

变量名|变量类型|变量说明|
:-----|:-----|:-----|
security|str|股票代码（不包括交易所代码）
volume|int|交易量（手），必须是100的倍数
price_type|str|交易类型:now_price现价
price|float|交易价格，仅当选择定价交易时可用
effect_term|int|订单有效时长（天），超过将自动扯淡，仅实盘模拟时有效

返回

变量名|变量类型|变量说明|
:-----|:-----|:-----|

###`engine.sell(security,volume,price_type='now_price',price=None,date=None,effect_term = 1)`

传入参数：

变量名|变量类型|变量说明|
:-----|:-----|:-----|
security|str|股票代码（不包括交易所代码）
volume|int|交易量（手），必须是100的倍数
price_type|str|交易类型:now_price现价
price|float|交易价格，仅当选择定价交易时可用
effect_term|int|订单有效时长（天），超过将自动扯淡，仅实盘模拟时有效

返回

变量名|变量类型|变量说明|
:-----|:-----|:-----|