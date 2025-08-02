# 程序 2-2-Find_Circle
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

        # 寻找圆形
        img_cir = img.to_grayscale() # 把图像变为黑白图像
        img_cir = img_cir.binary( [ (103, 156) ] )

        circles = img_cir.find_circles(threshold=3000, r_min=100,r_max = 200,\
                                       x_stride=3, y_stride=3 ,r_margin=100,\
                                       x_margin=40,  y_margin=40)
        for cir in circles:
            img.draw_circle(cir.x(), cir.y(), cir.r(), color=(255, 0, 0), thickness=2)
            print("圆中心:", cir.x(), cir.y(), "半径:", cir.r())

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
image.find_circles([roi[, x_stride=2[, y_stride=1[, threshold=5000[, x_margin=10[, y_margin=10
                        [, r_margin=10[, r_min=2[, r_max[, r_step=2]]]]]]]]]])

①roi:区域
②x_stride , y_stride : 跳过的像素
③threshold:最小识别面积


'''


