# 程序七: TouchScreen
# 2025.7.24

# -----导入模块-----
from machine import TOUCH
import time

# -----配置相关功能-----
# 实例化TOUCH设备0
tp = TOUCH(0)

while True:
    # 读取数据
    p = tp.read()
    # 进行触摸事件判断
    if p != () :
        print(p) # 打印原始数据
        for i in range(len(p)):
            print('x'+str(i)+'=' , p[i].x , 'y'+str(i)+'=',p[i].y )
    time.sleep_ms(50)

'''
屏幕为800 * 480 , 左上角为原点
语法:
1.
touch = TOUCH(index, rotation) # 1.设备号(0-9) , 2.面板输出坐标旋转，取值[0-3]->0°-270°
2.
TOUCH.read([count]) # 获取触摸数据(count为最多读取的触摸点数,0表示读取全部)
返回tuple(元组)
'''
