# 程序2-1: Sensor
# 2025.7.24

# -----导入模块-----
import time
import os   # 保存图像到SD卡、自动读取文件，再加上 os 就行
import sys  # 复杂模块化程序，再考虑用 sys

from media.sensor import *  # 导入sensor,使用摄像头相关接口
from media.display import * # 导入display模块
from media.media import *   # 导入media模块

# -----配置相关功能-----
# !!!摄像头初始化配置!!!
sensor = Sensor()   # 构建摄像头对象,使用默认设置
sensor.reset()      # 初始化
sensor.set_framesize(sensor.FHD)    # 初始化尺寸,通道默认0,其他的也是保持默认
sensor.set_pixformat(Sensor.RGB565) # 设置输出图像格式(像素),通道默认0

#使用IDE缓冲区输出图像,显示尺寸和sensor配置一致。
Display.init(Display.VIRT, sensor.width(), sensor.height())

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
语法:

https://wiki.01studio.cc/docs/canmv_k230/machine_vision/camera

1.     # ID默认CSI2 , 宽(默认1920) 高(默认1080) 最大帧率(默认30)
sensor = Sensor(id,[width, height, fps])
2.
sensor.reset() # 复位和初始化摄像头
3.
sensor.set_framesize(framesize = FRAME_SIZE_INVAILD, [width, height],chn = CAM_CHN_ID_0, alignment=0, **kwargs)
①framesize和 [width, height]只使用其中一种方式设置设置尺寸,前者理解为设置好的宏定义,后者自定义
②设置通道,一般用0和2
4.                 设置图像像素格式
sensor.set_pixformat(pixformat, chn = CAM_CHN_ID_0)
5.
sensor.run()
6.
sensor.snapshot(chn = CAM_CHN_ID_0) # 使用相机拍摄一张照片，并返回 image 对象

clock对象,用于计算帧率
clock=time.clock() # 构建时钟对象
clock.tick()       # 开始追踪,启动运行时间
clock.fps()        # 停止追踪,并且返回帧率(fps)

'''

