# 程序五: UART串口通信
# 2025.7.24

# -----导入模块-----
from machine import UART    # 导入UART模块
from machine import FPIOA   # 导入GPIO模块 , 功能引脚映射器,设置引脚的IO用途
import time

# -----配置相关功能-----
## 绑定引脚
fpioa = FPIOA()
fpioa.set_function(11 , FPIOA.UART2_TXD)
fpioa.set_function(12 , FPIOA.UART2_RXD)
## 设置引脚状态
uart = UART(UART.UART2, 115200) # #设置串口号2和波特率,这就够了

## 实现信息传输
# 写
uart.write('uart out')

while True:
    # 读
    text = uart.read(128)
    if text != None:
        print(text)
    time.sleep(0.01)

'''
语法:
1.
           编号(只能用1:t3r4,2:t11r12)   后面的比特率,数据位,奇偶校验,停止位都保持默认
machine.UART(id, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

2.
UART.read(num)

3.
UART.readline(num) # 读取一行，并以一个换行符结束。

4.
UART.write(buf)

5.
UART.deinit()

6.
UART.readinto(buf[, nbytes]) # 将字节读取入buf。若指定nbytes，则最多读取该数量的字节。否则，最多读取len(buf)数量的字节。
'''
