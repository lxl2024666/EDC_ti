# 程序3-2: Line_Check(线段检测)
# 2025.7.24

# -----导入模块-----
import time , os , sys

from media.sensor import *  # 导入sensor,使用摄像头相关接口
from media.display import * # 导入display模块
from media.media import *   # 导入media模块
# -----变量声明-----
lcd_width = 800
lcd_height = 480
enable_lens_corr = False # 设为True可以获得更直的线段,其实也就是调用了一个处理畸变的函数

# -----配置相关功能-----
# 摄像头初始化配置
sensor = Sensor(width=1280, height=960)   # 构建摄像头对象,将摄像头长宽设置为4:3
sensor.reset()          # 初始化
sensor.set_framesize(width=320,height=240)   # 设置帧大小为LCD分辨率(320*240),增加帧率,原分辨率下帧率太低了
sensor.set_pixformat(Sensor.RGB565) # 设置输出图像格式(像素),该像素为彩色更好看

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

    # 处理图像畸变             处理畸变的函数
    if enable_lens_corr : img.lens_corr(1.8)

    # 处理各个线段
    for l in img.find_line_segments(merge_distance = 0 , max_theta_difference = 5):
        img.draw_line(l.line(), color = (255, 100, 100), thickness = 3)
        #print(l)

    # 展示照片+打印帧率
    #img.compressed_for_ide() # 可以用来调节图像大小,类似于放大图像,但是缺点是帧率会腰斩
    Display.show_image(img,x=round((lcd_width-sensor.width())/2),y=round((lcd_height-sensor.height())/2))

    print(clock.fps())


'''
语法:
1.
image.find_line_segments([roi[, merge_distance=0[, max_theta_difference=15]]])
①roi: 识别区域（x,y,w,h），未指定则默认整张图片
②merge_distance: 两条线段间可以相互分开而不被合并的最大像素；
③max_theta_difference: 将少于这个角度值的线段合并
返回一个 image.line 对象的列表(其实类似于返回一个线段结构体),包含了x0,y0,x1,y1,长度,角度等
2.

'''


