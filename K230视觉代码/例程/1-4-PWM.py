# 程序四: PWM
# 2025.7.24

# -----导入模块-----
from machine import Pin     # 导入Pin模块  , 控制一个已经映射好的引脚的输入输出
from machine import FPIOA   # 导入GPIO模块 , 功能引脚映射器,设置引脚的IO用途
from machine import PWM     # 导入PWM模块
from machine import Timer
import time

# -----配置相关功能-----
## 绑定引脚
fpioa = FPIOA()
fpioa.set_function(42 , FPIOA.PWM0)  # 开发板只引出了0-3四个PWM通道,引脚是固定的

# 初始化PWM: pwm = PWM(channel, freq, duty, enable=False)
LED_PWM = PWM(0,200,50,enable = True)

# -----拓展应用功能-----
# 变量声明
counter = 0

# 建立回调函数
def fun(tim): ### !!!记得加冒号!!!
    global counter
    counter = (counter + 20) % 100
    print(counter)
    LED_PWM.duty(counter)

# 建立定时器
tim = Timer(-1) # 表示开启软件定时器
tim.init(period = 500 , mode = Timer.PERIODIC , callback = fun) # 模式为循环开启,中断函数为fun


while True:
    time.sleep(0.01)

'''
语法:
pwm = machine.PWM(channel, freq, duty, enable=False)
'''
