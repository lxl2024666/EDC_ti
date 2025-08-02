# 程序2-3: Display_Draw
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
    # 初始化计时
    clock.tick()
    # 先拍照
    img = sensor.snapshot()
    # 字体实践 屏幕: x : 0-800 , y : 0-480 ,字体粗细不错,推荐30,线条推荐1
    img.draw_line(0, 0, 200, 200, color = (200, 100, 100), thickness = 2)
    img.draw_rectangle(200, 200, 200, 200, color = (255, 0, 0), thickness = 2, fill = True)
    img.draw_string_advanced(600, 400, 30 , "字体实践", color = (255, 255, 255))
    img.flood_fill(400, 240, color=(255, 0, 0), threshold=30, invert=False, clear_background=False)

    print(clock.fps())
'''
总结:
!!!!!记得要先拍照sensor.snapshot(),再写字draw,最后展示show_image(img)!!!!!
'''


'''
语法:
1.两大构造函数,是其他函数的编写引用基础
①img=image.Image(path, copy_to_fb=True)  # 表示加载根目录下的图片
②img=image.Image(w, h, format)           # 主动创建一个图像, format:图像格式:GRAYSCALE(灰度),RGB565,RGB888
2.  其实线段类的都可以直接写一个img.line()更方便  0 - 255      线条粗细
①线段:img.draw_line(x0, y0, x1, y1, color = (R, G, B), thickness = 2)      是否填充
②矩形:img.draw_rectangle(x0, y0, w, h, color = (R, G, B), thickness = 2, fill = False)
③画圆:img.draw_circle(x0, y0, R , color = (R, G, B) , thickness = 2, fill = False)
④箭头:和线段相似
⑤十字交叉: img.draw_cross(x, y, color = (255, 255, 255), size = 20, thickness = 2)        强制间隔
⑥字符:img.draw_string(x, y, "Hello 01Studio!", color = (255, 255, 255), scale = 4, mono_space = False)
⑦字符，支持中文:img.draw_string_advanced(x, y, char_size , "人生苦短, 我用Python", color = (255, 255, 255))

'''
