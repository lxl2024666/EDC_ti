# 程序 电赛-得到各个的圆环轨迹
# 2025.7.30

# -----导入模块-----
import time , os , sys
from media.sensor import *
from media.display import *
from media.media import *

# -----建立变量-----
sensor = None
# -----配置相关功能-----
try:
    print("camera_test")
    # 初始化摄像头
    sensor = Sensor(width=640,height=480)
    sensor.reset()
    sensor.set_framesize(width=640,height=480)
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
        img.lens_corr(strength=0.2)

        #-----核心代码-----

        #寻找色块
        thresholds = [
            (35, 68, -38, 9, -24, 16),       # 红色
        ]
        # 得到二值化数据
        img_blob = img.copy().to_rgb565().binary( thresholds )

        blobs = img_blob.find_blobs( thresholds , False , x_stride = 2 , y_stride = 2 ,\
                               pixels_threshold = 200 )


        for blob in blobs :
            if blob.code() == 1:    # 红色色块
                color = (255, 0, 0)
                print("红色坐标: x={}, y={}".format(blob.cx(), blob.cy()))
            else:
                color = (255, 255, 255)
            img.draw_rectangle(blob.rect(), color = color, thickness = 2, fill = False)
            img.draw_circle(blob.cx(), blob.cy(), 3, color=color)
        #-----尾处理-----

        # 展示图像和帧率
        img.draw_string_advanced(40, 40, 30 , "fps: {}".format(clock.fps()), color = (0, 255, 255))

        # 画面裁切:增加帧率 , 宽和高必须是8的倍数
        #img = img.copy(roi = (296,132,320,256))

        Display.show_image(img)
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


