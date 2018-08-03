#说明


Fintech是一套模拟投资系统,基于海知平台的模拟投资系统进行投资。在框架下，可以非常方便的制定模拟投资策略。
用户只需要定义每一天需要执行的操作，系统会自动完成日期跳转等复杂的控制过程，同时框架运行在本地，可以很方便
的制定高度自由的策略。避免了那些在线编辑的量化网站无法高度自由使用自己定义的库的局限性。
#tutorial


我们将完整的演示如何完成一个自己的模拟投资策略

注：项目是在pycharm中完成的，引用过程不是很规范，需要在pycharm中运行，否则会出现引用错误。可以通过更改path
修复上述问题

##快速开始

第一步，我们需要初始化模拟投资引擎。
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
初始化了引擎之后，我们就可以编写自己的第一个投资策略了。我们现在编写一个非常简单的策略，加入股票昨日的收盘价
大于过去5日的平均收盘价，则买进；小于则卖出
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
现在让我们运行一下我们的策略
```python
engine.run_stratagy(tutorial)#运行策略
print engine._core.history_to_csv()#将交割单输出
```
需要注意的是，在运行策略的时候，我们只需要向引擎传入策略名。开始运行之后，引擎会自动在每个历史日期运行我们的策略。

不难发现，在框架下，只需要设计策略每天需要执行什么样的策略就可以了，不需要考虑很多复杂的控制逻辑，框架会自动帮你解决这些问题。
现在你已经可以开始设计自己的模拟投资策略了！

##与回测引擎交互

在设计投资策略的过程中，也许会在本地计算出一些数据，需要在回测运行过程中作为全局变量传入。我们将在这一节演示如何与回测引擎进行
数据交互。`engine.context`是用来进行数据交互的类，`context.user_data`是一个字典类型，用户可以将自定义的数据保存在`context.user_data`
中。
```python
engine.context.user_data['stock_list'] = ['600848','600847']
```
现在我们在策略中通过直接访问`context.user_data['stock_list']`就能查看到我们之前传入的用户变量。我们可以再策略运行中改变这个变量，
也可以在策略开始之前传入用户自定义的变量。
#Reference