# 程序 5-1-Cal_Distance
# 2025.7.26

# -----导入模块-----
import time , os , sys
from media.sensor import *
from media.display import *
from media.media import *

# -----建立变量-----
sensor = None
object_width_cm = 3.2 # 物体的实际宽度
focal_length_pixels = 775 # 焦距,自己测

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

        # -----定义函数-----
        # 1. 得到最大的色块
        def find_max_blob(blobs):
            max_size = 0
            for blob in blobs:
                if (blob.pixels() > max_size):
                    max_blob = blob
                    max_size = blob.pixels()
            return max_blob
        # 2. 返回实际距离
        def cal_distance(object_width_pixels , object_width_cm , focal_length_pixels ):
            return object_width_cm * focal_length_pixels / object_width_pixels



        # -----核心代码-----

        #寻找色块
        thresholds = [
            (0, 100, 25, 127, -22, 127),       # 红色
            (31, 50, -46, -16, 3, 42)       # 绿色
        ]
        blobs = img.find_blobs( thresholds , False , x_stride = 1 , y_stride = 1 ,\
                               pixels_threshold = 200)
        # 框出色块
        for blob in blobs :
            if blob.code() == 1:    # 红色色块
                color = (255, 0, 0)
                print("红色坐标: x={}, y={}".format(blob.cx(), blob.cy()))
            elif blob.code() == 2:  # 绿色色块
                color = (0, 255, 0)
                print("绿色坐标: x={}, y={}".format(blob.cx(), blob.cy()))
            else:
                color = (255, 255, 255)
            img.draw_rectangle(blob.rect(), color = color, thickness = 2, fill = False)
            img.draw_circle(blob.cx(), blob.cy(), 3, color=color)
        # 得到距离
        if (blobs):
            max_blob = find_max_blob(blobs)
            object_width_pixels = max_blob.w()
            #
            print(object_width_pixels)

            distance_cm = cal_distance(object_width_pixels , object_width_cm , focal_length_pixels )

            img.draw_string_advanced(250, 80, 30 , "真实距离: {}".format(distance_cm), color = (0, 255, 255))
        else :
            pass

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


