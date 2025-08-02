# 程序 识别紫色激光
# 2025.7.30 电赛第一天
# -----导入模块-----
import time , os , sys
from media.sensor import *
from media.display import *
from media.media import *
from machine import UART    # 导入UART模块
from machine import FPIOA   # 导入GPIO模块 , 功能引脚映射器,设置引脚的IO用途

# -----串口初始化-----
fpioa = FPIOA()
fpioa.set_function(11 , FPIOA.UART2_TXD)
fpioa.set_function(12 , FPIOA.UART2_RXD)
uart = UART(UART.UART2, 115200) #设置串口号2和波特率,这就够了

# -----建立变量-----
sensor = None
flag = 1 # 空闲状态 flag = 1 : 激光追踪模式

frame_w = 640
frame_h = 480

cut_x = 90
cut_y = 0
cut_w = 380
cut_h = 180


# -----配置相关功能-----
try:
    # ----------函数1: 得到一种颜色(紫色)的最大色块,返回相应坐标----------
    # 输入图像img , 色块识别容忍度 , 色块面积最小检值 , 绘图颜色 , 搜寻跨度(x,y) , 裁切矩形
    def Find_Max_Blob_Color(img , threshold , pixels_threshold , color = [255,255,255] , x_stride = 1 , y_stride = 1 , \
                            cut_Blob_x = 0 , cut_Blob_y = 0 , cut_Blob_w = frame_w , cut_Blob_h = frame_h ) :
        blobs = img.copy(roi = ( cut_Blob_x , cut_Blob_y , cut_Blob_w , cut_Blob_h )).find_blobs( threshold , False , \
                               x_stride = x_stride , y_stride = y_stride ,pixels_threshold = pixels_threshold )
        if not blobs:
            return 0,0
        else :
            max_size = 0
            max_blob = blobs[0]
            for blob in blobs :
                if blob.pixels() > max_size:
                    max_size = blob.pixels()
                    max_blob = blob
            # 画图的时候注意坐标偏移,因为在cut图中max_blob.位置()返回的是cut的变量
            img.draw_rectangle( (max_blob.x() + cut_Blob_x, max_blob.y() + cut_Blob_y, max_blob.w(), max_blob.h()) , color = color, thickness = 2, fill = False)
            img.draw_circle(max_blob.cx()+cut_Blob_x, max_blob.cy()+ cut_Blob_y, 3, color=color)
            return max_blob.cx(), max_blob.cy()

    # ----------函数2: 返回靶纸圆形中心坐标(***测试中,目前为模拟值***)----------
    def Find_Circle_Central_Loc(img):
        point_x = cut_x + 200
        point_y = cut_y + 120
        img.draw_circle(point_x, point_y, 3, color=[255 , 0 , 0] , fill = True )
        return (point_x) , (point_y)

    # ----------函数集3: 16进制计算------------------
    # 得到数据的高位（返回8~15位）
    def get_high_val_of_hex(value):
        return (value >> 8) & 0xFF

    # 得到数据的低位（返回0~7位）
    def get_low_val_of_hex(value):
        return value & 0xFF

    # 用高位和低位组合成一个完整的16位整数
    def get_val_of_hex(high, low):
        return (high << 8) | low

    # ----------setup----------
    # 初始化摄像头
    sensor = Sensor(width=640,height=480)
    sensor.reset()
    sensor.set_framesize(width=640,height=480)
    sensor.set_pixformat(Sensor.RGB565)

    Display.init(Display.ST7701, to_ide=True)   # 初始化显示器
    MediaManager.init()                         # 初始化媒体管理器
    sensor.run()                                # 启动 sensor
    clock = time.clock()                        # 开始计时帧率

    # ----------loop----------

    while True:
        # 计算帧率
        clock.tick()
        os.exitpoint()

        # 拍照
        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        #-----核心代码-----

        # ----------记录位置---------
        #寻找色块
        thresholds = [
            (23, 45, 18, 79, 9, 67),      # 红色
            (57, 100, -54, 7, -28, 3),      # 紫色
            (54, 76, -64, -21, -25, 75)     # 绿色(待删)
        ]

        # 记录位置->帧头
        data_payload = [0x12 , 0x10]       # 记录色块位置,初始帧:0x12,一共8个位 + 虚拟8位

        # 红色:0  紫色:1  绿色:2(待删)
#        data_payload.extend(Find_Max_Blob_Color(img , [ thresholds[0] ] , pixels_threshold = 20 , color = [255,  0,   0] ,\
#                    cut_Blob_x = cut_x , cut_Blob_y = cut_y , cut_Blob_w = cut_w , cut_Blob_h = cut_h ))

        # 记录位置->目标值 : target_x  target_y
        target_x , target_y = Find_Circle_Central_Loc(img)
        data_payload.extend([get_high_val_of_hex(target_x) , get_low_val_of_hex(target_x), get_high_val_of_hex(target_y) , get_low_val_of_hex(target_y)])

        # 记录位置->实际值 : real_x  real_y
        real_x  ,real_y = Find_Max_Blob_Color(img , [ thresholds[0] ] , pixels_threshold = 20 , color = [128,  0, 128] ,\
                            cut_Blob_x = cut_x , cut_Blob_y = cut_y , cut_Blob_w = cut_w , cut_Blob_h = cut_h )

        data_payload.extend([get_high_val_of_hex(real_x) , get_low_val_of_hex(real_x), get_high_val_of_hex(real_y) , get_low_val_of_hex(real_y)])

        data_payload.extend([0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0x00 , 0x00])

        # 记录位置->帧尾
        data_payload.append(0x5B)

        # 裁切区域
        img.draw_rectangle(cut_x , cut_y, cut_w , cut_h , [255,255,255], thickness = 2, fill = False)

        # 打印展示
        #print(data_payload[0] , target_x , target_y , real_x ,real_y , data_payload[5] )
        print(data_payload)
        # ----------串口帧通信---------

        # 读取指令  激光位置返回帧:    0x12  target_x  target_y  real_x  real_y  0x5B
        text = uart.read(128)
        # 接收相关指令,执行相关命令
        uart.write(bytes(data_payload))         # 传输激光信息
        # 延时休息
        time.sleep(0.01)

        #---------尾处理---------
        # 展示图像和帧率
        img.draw_string_advanced(40, 40, 30 , "fps: {}".format(clock.fps()), color = (0, 255, 255))
        # 画面裁切:增加帧率 , 宽和高必须是8的倍数
        #img = img.copy(roi = (296,132,320,256))

#        img.compressed_for_ide()    # 伸展图像到正中间

#        img_cut = img.copy(roi = ( 80 , 0 , 560 , 240 ) ).to_grayscale()
#        img.draw_image(img_cut , 80 , 0)

        Display.show_image(img)
#        print("fps: {}".format(clock.fps()))

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
    1. 接线,先接CanMV再STM32
    2. STM32_TX == PA9  ----- 12 == CanMV_RX(上)
       STM32_RX == PA10 ----- 11 == CanMV_TX(下)
    3. STM32传输信息来时,text == b'一个字母' , 所以STM32也是发送一个字母
    4. CanMV发送信息去时,uart.write(bytes(列表)) , STM32接受到的就是一串数组,都是16进制
'''
'''

#        for blob in blobs :
#            if blob.code() == 1:    # 红色色块
#                color = (255, 0, 0)
#                print("红色坐标: x={}, y={}".format(blob.cx(), blob.cy()))
#            elif blob.code() == 2:  # 绿色色块
#                color = (0, 255, 0)
#                print("绿色坐标: x={}, y={}".format(blob.cx(), blob.cy()))
#            elif blob.code() == 3:  # 紫色色块
#                color = (75, 0, 130)
#                print("紫色坐标: x={}, y={}".format(blob.cx(), blob.cy()))
#            else:
#                color = (255, 255, 255)
#            img.draw_rectangle(blob.rect(), color = color, thickness = 2, fill = False)
#            img.draw_circle(blob.cx(), blob.cy(), 3, color=color)
'''
