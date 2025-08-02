# 程序 1-2-Find_Two_Color_Multi
# 模拟2024电赛E题井字棋
# 2025.7.25

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

        #-----核心代码-----

        #寻找色块
        thresholds = [
            (22, 53, 10, 68, 11, 47),       # 红色
            (36, 41, 27, 80, -107, -55),     # 绿色
            (42, 67, 19, 38, -1, 127)        # 紫色
        ]
        blobs = img.find_blobs( thresholds , False , x_stride = 1 , y_stride = 1 ,\
                               pixels_threshold = 20)

        for blob in blobs :
            if blob.code() == 1:    # 红色色块
                color = (255, 0, 0)
                print("红色坐标: x={}, y={}".format(blob.cx(), blob.cy()))
            elif blob.code() == 2:  # 绿色色块
                color = (0, 255, 0)
                print("绿色坐标: x={}, y={}".format(blob.cx(), blob.cy()))
            elif blob.code() == 3:  # 紫色色块
                color = (75, 0, 130)
                print("紫色坐标: x={}, y={}".format(blob.cx(), blob.cy()))
            else:
                color = (255, 255, 255)
            img.draw_rectangle(blob.rect(), color = color, thickness = 2, fill = False)
            img.draw_circle(blob.cx(), blob.cy(), 3, color=color)

        #-----尾处理-----

        # 展示图像和帧率
        img.draw_string_advanced(40, 40, 30 , "fps: {}".format(clock.fps()), color = (0, 255, 255))

        # 画面裁切:增加帧率 , 宽和高必须是8的倍数
        #img = img.copy(roi = (296,132,320,256))

        img.compressed_for_ide()    # 伸展图像到正中间
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


