# 程序二: 按键
# 2025.7.24

# -----导入模块-----
from machine import Pin     # 导入Pin模块  , 控制一个已经映射好的引脚的输入输出
from machine import FPIOA   # 导入GPIO模块 , 功能引脚映射器,设置引脚的IO用途
import time

# -----配置相关功能-----
## 绑定引脚
fpioa = FPIOA()
fpioa.set_function(52 , FPIOA.GPIO52 ) # LED对象
fpioa.set_function(21 , FPIOA.GPIO21 ) # Key对象

## 设置引脚状态
LED = Pin(52 , Pin.OUT)
Key = Pin(21 , Pin.IN , Pin.PULL_UP)

# -----实现相关操作-----
state = 0

while True:
    if Key.value() == 0 :
        time.sleep_ms(10)
        if Key.value() == 0 :
            state = not state
            LED.value(state)
            print('Key')

            while not Key.value():
                pass
