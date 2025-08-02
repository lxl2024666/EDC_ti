# 程序 2-1-Find_Rect
# 2025.7.25

# -----导入模块-----
import time , os , sys
from media.sensor import *
from media.display import *
from media.media import *

# -----建立变量-----
lcd_width = 800
lcd_height = 480
sensor = None

# -----配置相关功能-----
try:
    print("camera_test")
    # 初始化摄像头
    sensor = Sensor(width=1280, height=960) # width=1280, height=960
    sensor.reset()
    sensor.set_framesize(width=640,height=480) # width=320,height=240
    sensor.set_pixformat(Sensor.RGB565)

    Display.init(Display.ST7701, to_ide=True)   # 初始化显示器
    MediaManager.init()                         # 初始化媒体管理器
    sensor.run()                                # 启动 sensor
    clock = time.clock()                        # 开始计时帧率
    while True:
        # 计算帧率
        clock.tick()
        os.exitpoint()

        # 拍照
        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        #-----核心代码-----

        # 寻找矩形
        img_rect = img.to_grayscale() # 把图像变为黑白图像
        img_rect = img_rect.binary( [ (99, 173) ] )
        rects = img_rect.find_rects(threshold = 5000)
        for rect in rects:
            corner = rect.corners()
            img.draw_line(corner[0][0], corner[0][1], corner[1][0], corner[1][1], color = (0, 255, 0), thickness = 2)
            img.draw_line(corner[2][0], corner[2][1], corner[1][0], corner[1][1], color = (0, 255, 0), thickness = 2)
            img.draw_line(corner[2][0], corner[2][1], corner[3][0], corner[3][1], color = (0, 255, 0), thickness = 2)
            img.draw_line(corner[0][0], corner[0][1], corner[3][0], corner[3][1], color = (0, 255, 0), thickness = 2)

        #-----尾处理-----

        # 展示图像和帧率
        img.draw_string_advanced(40, 40, 30 , "fps: {}".format(clock.fps()), color = (0, 255, 255))

        # 画面裁切:增加帧率 , 宽和高必须是8的倍数
        #img = img.copy(roi = (296,132,320,256))

        #img.compressed_for_ide()    # 伸展图像到正中间
        Display.show_image(img,x=round((lcd_width-sensor.width())/2),y=round((lcd_height-sensor.height())/2))
        print("fps: {}".format(clock.fps()))

except KeyboardInterrupt as e:
    print("用户停止: ", e)
except BaseException as e:
    print(f"异常: {e}")
finally:
    if isinstance(sensor, Sensor):
        sensor.stop()
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()

'''
语法:

'''


