# 程序2-2-2: Display
# 2025.7.24

# -----导入模块-----
import time
import os
import sys

from media.sensor import *  # 导入sensor,使用摄像头相关接口
from media.display import * # 导入display模块
from media.media import *   # 导入media模块

# -----配置相关功能-----
# !!!摄像头初始化配置!!!
sensor = Sensor()   # 构建摄像头对象,使用默认设置
sensor.reset()      # 初始化
sensor.set_framesize(width=800,height=480)    # !!!初始化尺寸,通道默认0,其他的也是保持默认!!!
sensor.set_pixformat(Sensor.YUV420SP) # 设置输出图像格式(像素),在YUV420SP下才能使用LAYER_VIDEO1,通道默认0

# 拓展:使用更高效的Display函数显示图像,跳过截屏+展示模式,而是将摄像头直接连到通道

# 函数解释: x , y 把图像显示在屏幕的左上角(0,0)位置     chn:表示从CSI0接收的图像通道获取图像
sensor_bind_info = sensor.bind_info(x=0, y=0, chn=CAM_CHN_ID_0) #绑定摄像头图象到显示层
# 把上一步返回的摄像头图像，显示在指定的显示层上,LAYER_VIDEO1 是主图层（显示视频或摄像头图像）,LAYER_OSD0/OSD1 是叠加图层（文字、框框、识别结果）
Display.bind_layer(**sensor_bind_info, layer=Display.LAYER_VIDEO1)

#使用IDE缓冲区输出图像,显示尺寸和sensor配置一致。
Display.init(Display.ST7701 , to_ide = True)

MediaManager.init() #初始化media资源管理器

#!!!启动摄像头!!!
sensor.run()

# 初始化时钟对象
clock = time.clock()

while True:
    clock.tick()
    _ = sensor.snapshot()  # 加上这句才有图像帧更新，fps 才有效
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
4.
# 摄像头/视频模块的输出 → 直接绑定到某个显示层，然后系统自动帮你持续刷新图像，不需要你每次 snapshot()+show_image()
Display.bind_layer(src=(mod, dev, layer), dstlayer, rect = (x, y, w, h), pix_format, alpha, flag)
                   图像源信息    显示层(VIDEO：视频层，OSD：叠加层（用于显示按钮/UI）)     图层透明度(一般默认255)
建议:
bindinfo = sensor.bind_info()    # 获取绑定信息

**sensor_bind_info 是自动拆包成参数，等价于你手动写 (mod, dev, layer) 等,那么可以省略写src,rect,pix_format
                   然后alpha=255,flag=0为默认值,所以只要**sensor_bind_info 和 layer=Display.LAYER_VIDEO1(要求Sensor像素为YUV420SP)

Display.bind_layer(
    src=bindinfo,
    dstlayer=Display.VIDEO,
    rect=bindinfo.rect,
    pix_format=bindinfo.pix_format,
    alpha=255,
    flag=0
)
!!!!! 必须在 Display.init() 之前 !!!!!

'''

