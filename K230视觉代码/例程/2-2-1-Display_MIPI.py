# 程序2-2-1: Display
# 2025.7.24

# -----导入模块-----
import time , os , sys

from media.sensor import *  # 导入sensor,使用摄像头相关接口
from media.display import * # 导入display模块
from media.media import *   # 导入media模块

# -----配置相关功能-----
# !!!摄像头初始化配置!!!
sensor = Sensor()   # 构建摄像头对象,使用默认设置
sensor.reset()      # 初始化
sensor.set_framesize(width=800,height=480)    # !!!初始化尺寸,通道默认0,其他的也是保持默认!!!
sensor.set_pixformat(Sensor.RGB565) # 设置输出图像格式(像素),通道默认0

#使用IDE缓冲区输出图像,显示尺寸和sensor配置一致。
Display.init(Display.ST7701 , to_ide = True)

MediaManager.init() #初始化media资源管理器

#!!!启动摄像头!!!
sensor.run()

# 初始化时钟对象
clock = time.clock()

while True:
    clock.tick()

    img = sensor.snapshot()

    Display.show_image(img)

    print(clock.fps())
'''
这其实与IDE显示十分像,只是尺寸需要改变,并且尺寸需要小于等于IDE 和  mipi屏(800*480)的min,

截止到现在,我们明白了屏幕的使用配置,初始化-尺寸,通道(默认)与像素-启动

'''


'''
语法:
1.初始化(必须在MediaManager.init()之前调用)  显示设备类型:ST7701(本队的mipi显示屏) 是否同时在IDE(电脑上)显示,仅用于设置为HDMI或MIPI屏显示时使用
Display.init(type = None, width = None, height = None, osd_num = 1, to_ide = False, fps = None)
2.显示图像       显示的图像  起始的(x,y)坐标
Display.show_image(img, x = 0, y = 0, layer = None, alpha = 255, flag = 0)
3.注销显示
Display.deinit() !!!必须在MediaManager.deinit()之前, 在sensor.stop()之后调用!!!

'''

