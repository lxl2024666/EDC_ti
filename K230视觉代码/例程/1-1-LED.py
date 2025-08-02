# 程序一: 点亮板载LED
# 2025.7.23

# -----导入模块-----
from machine import Pin     # 导入Pin模块  , 控制一个已经映射好的引脚的输入输出
from machine import FPIOA   # 导入GPIO模块 , 功能引脚映射器,设置引脚的IO用途
import time

# -----配置相关功能-----
## 绑定引脚
fpioa = FPIOA()
fpioa.help()
fpioa.set_function(50 , FPIOA.GPIO50 )
LED1 = Pin(50 , Pin.OUT)

fpioa.set_function(51 , FPIOA.GPIO51 )
LED2 = Pin(51 , Pin.OUT)

fpioa.set_function(52 , FPIOA.GPIO52 )
LED  = Pin(52 , Pin.OUT)
## 设置引脚状态

LED.value(1)
LED1.value(1)
LED2.value(1)
while True:
    pass


