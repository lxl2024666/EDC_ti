# 程序六: 线程
# 2025.7.24

# -----导入模块-----
import time
import _thread              # 导入线程模块

# -----配置相关功能-----
## 定义函数,作为线程导入函数
def func(name): # 又忘记加冒号了
    while True :
        print("hello {}".format(name))
        time.sleep(1)       # 延时1s

## 开启线程
_thread.start_new_thread(func,("1",)) # 线程一
_thread.start_new_thread(func,("2",)) # 线程二

while True:
    time.sleep(0.01)


'''
线程:
1.
一般2~3个最稳，避免内存爆炸
2.
每个线程都要有sleep,否则CPU爆满,卡死系统
3.
避免同时操作同一个变量
4.
如果只有一个参数，一定写成 (param, ) 加逗号
0个:() 1个:(param, ) 2个:(param1, param2) 更多:(1,2,3,...,n)
5.
模版:

1.import _thread
2.def func(param1 , param2 ...)
    # 建立变量
    # while True :
        主程序
        time.sleep(delay) # 一定要睡一会
3._thread.start_new_thread(func,(param1, 2, 3, ...,n))

4.主程序(main)(看做主线程)
    while True:
        ...
## 总结:线程也就是while,记得delay休息
'''
