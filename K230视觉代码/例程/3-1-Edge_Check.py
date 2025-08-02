# 程序3-1: Edge_Check(边缘检测)
# 2025.7.24

# -----导入模块-----
import time , os , sys

from media.sensor import *  # 导入sensor,使用摄像头相关接口
from media.display import * # 导入display模块
from media.media import *   # 导入media模块
# -----变量声明-----
lcd_width = 800
lcd_height = 480

# -----配置相关功能-----
# 摄像头初始化配置
sensor = Sensor(width=1280, height=960)   # 构建摄像头对象,将摄像头长宽设置为4:3
sensor.reset()          # 初始化
sensor.set_framesize(width=320,height=240)   # 设置帧大小为LCD分辨率(320*240),增加帧率,原分辨率下帧率太低了
sensor.set_pixformat(Sensor.GRAYSCALE) # 设置输出图像格式(像素),该像素适合边缘检测

#使用IDE缓冲区输出图像,显示尺寸和sensor配置!不!一致,毕竟显示部分(给人看)没必要做小。
Display.init(Display.ST7701 ,width = lcd_width, height = lcd_height, to_ide = True) # ,width = lcd_width, height = lcd_height

MediaManager.init() #初始化media资源管理器

# 启动摄像头
sensor.run()

# 初始化时钟对象
clock = time.clock()

while True:
    # 计时+拍照
    clock.tick()
    img = sensor.snapshot()

    # 使用Canny边缘检测器
    img.find_edges(image.EDGE_CANNY , threshold=(50,80))

    # 展示照片+打印帧率
    Display.show_image(img,x=round((lcd_width-sensor.width())/2),y=round((lcd_height-sensor.height())/2))
    print(clock.fps())

'''
语法:
0.
中括号的意思是可写可不写
1.            # threshold: 包含高、低阈值的二元组，默认是（100,200），仅支持灰度图像。
image.find_edges(edge_type[, threshold]) # edge_type: 处理方式:①image.EDGE_SIMPLE②image.EDGE_CANNY(好)

总结:
1.
sensor = Sensor(width=1280, height=960)   # 构建摄像头对象,将摄像头长宽设置为4:3
作用就是表现可执行的尺寸
2.
sensor.set_framesize(width=320,height=240)
通过降低尺寸来保持不错的帧率
3.
Display.init(Display.ST7701 ,width = lcd_width, height = lcd_height, to_ide = True) # ,width = lcd_width, height = lcd_height
初始化展示时仍旧给出正常值




'''
