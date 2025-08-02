# 程序三: 定时器与中断
# 2025.7.24

# -----导入模块-----
from machine import Pin     # 导入Pin模块  , 控制一个已经映射好的引脚的输入输出
from machine import FPIOA   # 导入GPIO模块 , 功能引脚映射器,设置引脚的IO用途
from machine import Timer   # 导入定时器模块
import time                 #

# -----配置相关功能-----
# 变量设置
counter = 0

# 初始化LED
fpioa = FPIOA()
fpioa.set_function(52 , FPIOA.GPIO52 )

# 设置引脚状态
LED = Pin(52 , Pin.OUT)

# 定义函数
def fun(tim): ### !!!记得加冒号!!!
    global counter
    counter = counter + 1
    print(counter)
    LED.value(counter % 2)

# 建立定时器
tim = Timer(-1) # 表示开启软件定时器
tim.init(period = 1000 , mode = Timer.PERIODIC , callback = fun) # 周期为1s,模式为循环开启,中断函数为fun

# 循环建立
while True:
    time.sleep(0.01)

'''
语法:
tim.init(mode, freq, period, callback)
'''
