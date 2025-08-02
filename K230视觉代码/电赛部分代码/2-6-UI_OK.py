# 程序 电赛-测试-主程序
# 2025.8.2

# 阈值调试
'''
1.开场前:Rect_Gray , real_y_min , real_y_max
2.第②题:测量距离,修改distance(real_x , real)y)
3.第③题:位置改变,但能测量距离,修改distance
4.拔高第①②题,调整矩形阈值,得到圆心

'''
# ----------导入模块----------
import time , os , sys
from media.sensor import *
from media.display import *
from media.media import *
from machine import UART    # 导入UART模块
from machine import Pin     # 导入Pin模块  , 控制一个已经映射好的引脚的输入输出
from machine import FPIOA   # 导入GPIO模块 , 功能引脚映射器,设置引脚的IO用途
from machine import TOUCH   # 触摸系统
#导入自设库
from File_Com import *
from Rect_Com import *
from UI_Com   import *

# --------------------建立变量--------------------
# ----------UI界面相关变量----------
# LCD屏幕尺寸
lcd_width  = 640
lcd_height = 480
# LCD展示尺寸
frame_width = 640
frame_height = 480
# 按键方块(box)尺寸
box_width  = 120
box_height = 40
# 按键方块间隔
top_margin = 10     # 第一个按键距离LCD上部的间隔(留点距离防止误触,并且美观)
box_spacing = 60    # 各个按键之间的上下间隔,记得要小于按键高度 box_height
SetKeyNum = 16      # 设定的按键数目(一般来说12个够用了,并且还宽敞)

# 触摸初始化
tp = TOUCH(0)
flag = 1            # 系统标志位初始化
touch_counter = 0   # 长按时间计时

# ----------摄像头相关变量----------
# 摄像头初始化
sensor = None

# ----------LED调试变量-----------
# 绑定引脚
fpioa = FPIOA()
fpioa.set_function( 2 , FPIOA.GPIO2  )  # Laser对象
fpioa.set_function(21 , FPIOA.GPIO21 )  # Key对象

# 设置引脚状态
Laser = Pin(2  ,  Pin.OUT)
Key   = Pin(21 , Pin.IN , Pin.PULL_UP)

# -----------串口初始化-----------
fpioa = FPIOA()
fpioa.set_function(11 , FPIOA.UART2_TXD)
fpioa.set_function(12 , FPIOA.UART2_RXD)
uart = UART(UART.UART2, 115200) #设置串口号2和波特率,这就够了

# ----------调试参数设置----------
# 一些调试参数
a , b , c , d = 10 , 80 , 10 , 25

LAB_R = [0,0,0,0,0,0]
LAB_Z = [0,0,0,0,0,0]
LAB_test = [0, 100, -127, 128, -127, 128]

Gray_Rect = (44, 192)
Gray_test = [0,100]

# ----------激光位置参数设置----------

frame_w = 640
frame_h = 480

cut_x = 90
cut_y = 0
cut_w = 380
cut_h = 180

# ----------主函数---------------

# 文件存储行数
LAB_R_Line  = 1       # LAB_R的文件存储位置
LAB_Z_Line  = 2       # LAB_Z的文件存储位置
Gray_Line   = 3       # 灰度的文件存储位置
Laser_Line  = 4       # 激光的文件存储位置->real_x , real_y_min , real_y_max
Competition_mode_Line = 5 # 比赛模式设置

mode = 1    #
LAB_Change_Seq = 0  # 调节色块的序列,红色:0 , 紫色:1
state = 1 ; # Laser状态
is_to_ide = False

try:
    # ----------函数定义----------
    # ----------函数13: 数据传输运算:高低位----------
    # 得到数据的高位（返回8~15位）
    def get_high_val_of_hex(value):
        return (value >> 8) & 0xFF

    # 得到数据的低位（返回0~7位）
    def get_low_val_of_hex(value):
        return value & 0xFF

    # 用高位和低位组合成一个完整的16位整数
    def get_val_of_hex(high, low):
        return (high << 8) | low
    # ----------函数14: 根据输入的distance得到预期激光发射的real_y值----------
    def get_real_y_distance(dis0, y0, dis1, y1, distance):
        # 计算斜率 k = (y1 - y0) / (dis1 - dis0)
        k = (y1 - y0) / (dis1 - dis0)
        # 计算 real_y = y0 + k * (distance - dis0)
        real_y_expect = y0 + k * (distance - dis0)
        return real_y_expect

    # ----------初始化配置----------
    # 初始化摄像头
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=640,height=480)
    sensor.set_pixformat(Sensor.RGB565)

    Display.init(Display.ST7701, to_ide=is_to_ide)   # 初始化显示器
    MediaManager.init()                         # 初始化媒体管理器
    sensor.run()                                # 启动 sensor
    clock = time.clock()                        # 开始计时帧率

    # ----------从文件读取数据----------
    LAB_Z   = File_Read_Data( LAB_Z_Line) # 从文件读取数据
    LAB_R   = File_Read_Data( LAB_R_Line) # 从文件读取数据
    [real_x , real_y_min , real_y_max] = File_Read_Data( Laser_Line ) # 从文件读取数据
    [Competition_mode] = File_Read_Data(Competition_mode_Line) # 得到比赛模式
    # 第二,三题的距离参数设置初始化
    distance = min( (real_y_min + real_y_max) // 2 , 200 )

    Laser.value(1)
    while True:
        # 计算帧率
        clock.tick()
        os.exitpoint()

        # 拍照
        img = sensor.snapshot(chn=CAM_CHN_ID_0)
        img_clean = img.copy()  # 得到干净的画布

#        # 按键控制激光
        if Key.value() == 0 :
            time.sleep_ms(10)
            if Key.value() == 0 :
                state = not state
                Laser.value(state)
#                print('Key')
                while not Key.value():
                    pass
        #-----UI界面与相关UI功能-----
        points = tp.read()
        # 坐标展示与flag下处理
        if points != () :
#            print(points) # 打印原始数据
            for i in range(len(points)):
#                print('x'+str(i)+'=' , points[i].x , 'y'+str(i)+'=',points[i].y )
                KeyNum = Key_GetNum(points[i].x , points[i].y , img)
#                print('KeyNum: {}'.format(KeyNum))
                # 菜单选择功能,后端实现标志位变化
                # 要记得是先有flag设定UI界面,再有相应界面的功能,所以if 判断(后续实现相关功能)与flag有关
                if (KeyNum == None):
                    continue
                if (flag == 1):
                    pass
                if (flag == 2):
                    if (KeyNum >= 1 and KeyNum <= 5): #这样的原因在于如果不限制其他未定义按键,flag会被任意更改,造成一些问题
                        # 逻辑:按下1,回到主页(flag!=2,UI页面消失),按下2,没变 , 按下其他:去别的功能,反正flag != 2,菜单UI页面自然消失
                        flag = KeyNum
                    else :
                        pass
                if (flag == 3):
                    if (KeyNum == 1 or KeyNum == 2):
                        # 逻辑:按下1,回到主页(flag!=2,UI页面消失),按下2,回到菜单, 按下其他:进行调参
                        # (Key_num, var_value, Key_De, Key_Add, step=1 , min_num = 0 , max_num = 255 ):
                        # real_x , real_y_min , real_y_max
                        flag = KeyNum
                    elif ( KeyNum == 3 or KeyNum == 4):
                        a = Update_Val(KeyNum , a , 3 , 4 , 1 , 0 , 100 )
                    elif (KeyNum >= 5 and KeyNum <= 10):
                        real_x     = Update_Val(KeyNum , real_x     , 5 , 6 , 1 , 0 , 640 )
                        real_y_min = Update_Val(KeyNum , real_y_min , 7 , 8 , 1 , 0 , 480 )
                        real_y_max = Update_Val(KeyNum , real_y_max , 9 ,10 , 1 , 0 , 480 )
                    elif (KeyNum == 11 or KeyNum == 12):
                        distance   = Update_Val(KeyNum , distance   , 11 ,12, 1 , 40 , 200 )
                    elif (KeyNum == 13):
                        if Competition_mode == 1:
                            Competition_mode = 0
                            flag = 2
                        else:
                            Competition_mode = 1
                            flag = 2
                        File_Write_Data(Competition_mode_Line , [Competition_mode] , 'competition.txt') # 写入文件中,形成记忆
                    elif (KeyNum == 15):
                        File_Write_Data(Laser_Line , [real_x , real_y_min , real_y_max ] , 'competition.txt') # 写入文件中,形成记忆
                    else:
                        pass
                if (flag == 4):
                    if (KeyNum == 1 or KeyNum == 2):
                        # 逻辑:按下1,回到主页(flag!=2,UI页面消失),按下2,回到菜单, 按下其他:进行调参
                        flag = KeyNum
                    elif (KeyNum >= 3 and KeyNum <= 14):
                        LAB_test[0] = Update_Val(KeyNum , LAB_test[0] , 3 , 4 , 3 ,  0 , 100)
                        LAB_test[1] = Update_Val(KeyNum , LAB_test[1] , 5 , 6 , 3 ,  0 , 100)
                        LAB_test[2] = Update_Val(KeyNum , LAB_test[2] , 7 , 8 , 3 ,-128, 127)
                        LAB_test[3] = Update_Val(KeyNum , LAB_test[3] , 9 ,10 , 3 ,-128, 127)
                        LAB_test[4] = Update_Val(KeyNum , LAB_test[4] ,11 ,12 , 3 ,-128, 127)
                        LAB_test[5] = Update_Val(KeyNum , LAB_test[5] ,13 ,14 , 3 ,-128, 127)
                    elif (KeyNum == 15):
                        pass
                    elif (KeyNum == 16):
                        if (LAB_Change_Seq == 0):
                            LAB_R = LAB_test.copy()
                            File_Write_Data(LAB_R_Line , LAB_R , 'competition.txt') # 写入文件中,形成记忆
                        if (LAB_Change_Seq == 1):
                            LAB_Z = LAB_test.copy()
                            File_Write_Data(LAB_Z_Line , LAB_Z , 'competition.txt') # 写入文件中,形成记忆
                    else:
                        pass
                if (flag == 5):
                    if (KeyNum == 1 or KeyNum == 2):
                        # 逻辑:按下1,回到主页(flag!=2,UI页面消失),按下2,回到菜单, 按下其他:进行调参
                        flag = KeyNum
                    elif (KeyNum >= 3 and KeyNum <= 6):
                        Gray_test[0] = Update_Val(KeyNum , Gray_test[0] ,3 ,4 ,1 , 0, 100)
                        Gray_test[1] = Update_Val(KeyNum , Gray_test[1] ,5 ,6 ,1 , 0, 100)
                    elif (KeyNum == 7):
                        pass
                    elif (KeyNum == 8):
                        Gray_Rect = Gray_test.copy()
                        # 写入文件中,形成记忆
                        File_Write_Data(Gray_Line , Gray_Rect , 'competition.txt' )
                    else:
                        pass
        # 1.状态选择:长按1秒钟进入UI菜单
        if len(points) > 0 :
            if (flag == 1):
                touch_counter += 1
                if touch_counter > 10:
                    flag = 2
            if (flag == 4):
                touch_counter += 1
                if touch_counter > 5:
                    LAB_Change_Seq = (LAB_Change_Seq + 1) % 2
                    touch_counter = 0
        else:
            touch_counter -= 2
            touch_counter = max(0, touch_counter)
        # 2.Draw画板,所有文字显示都最好在这里完成,并且与flag有关联(if判断)
        if (flag == 2):
            if (Competition_mode == 1):
                img.draw_string_advanced(130, 200, 30 , "基础模式", color = (0, 255, 255))
            else:
                img.draw_string_advanced(130, 200, 30 , "拔高模式", color = (0, 255, 255))
        if (flag == 3):
            # 展示调参数据条
            img.draw_line(real_x, real_y_min, real_x,real_y_max, color = (255,0,0), thickness = 1)
            img.draw_line(0, real_y_min, frame_width, real_y_min , color = (0,0,0), thickness = 2)
            img.draw_line(0, real_y_max, frame_width, real_y_max , color = (0,0,0), thickness = 2)
            img.draw_string_advanced(130, 100, 30 , "distance:" + str(distance), color = (0, 255, 255))
        if (flag == 4):
            img.draw_string_advanced(130, 400, 30 , "LAB_test:" + str(LAB_test), color = (0, 255, 255))
            if ( LAB_Change_Seq == 0 ):
                img.draw_string_advanced(130, 440, 30 , "LAB_R_real:" + str(LAB_R), color = (0, 255, 255))
            if ( LAB_Change_Seq == 1 ):
                img.draw_string_advanced(130, 440, 30 , "LAB_Z_real:" + str(LAB_Z), color = (0, 255, 255))

        if (flag == 5):
            img.draw_string_advanced(130, 400, 30 , "G_test:" + str(Gray_test), color = (0, 255, 255))
            img.draw_string_advanced(130, 440, 30 , "G_Rect:" + str(Gray_Rect), color = (0, 255, 255))

        # 3.UI菜单绘图

        UI_Choose(img , flag)

        if (flag == 4):
            # 先进行图像格式转换:二值化
            img_blob = img.to_rgb565().binary( [LAB_test] ).copy(roi = (box_width , 10 , frame_width - box_width * 2 , frame_height - 100))
            # 贴图,可以开始调灰度了
            img.draw_image(img_blob, box_width, 10)

        if (flag == 5):
            # 先进行图像格式转换,灰度+二值化
            img_rect = img.to_grayscale() # 把图像变为黑白图像
            img_rect = img_rect.binary( [Gray_test] ).copy(roi = (box_width , 10 , frame_width - box_width * 2 , frame_height - 100))
            # 贴图,可以开始调灰度了
            img.draw_image(img_rect, box_width, 10)

        # ------------------------------------主程序-----------------------------------
        if ( flag == 1 ):
            # ----------------功能1: 寻找色块位置----------------
            if(mode == 1):
                # ----------------矩形识别功能--------------------
                # 得到矩形的加权中心
                rect_x_central , rect_y_central = 0 , 0
                # 绘出矩形边框,得到矩形中心参数
                rects = Find_Two_Rects(img_clean.copy() , threshold = 100000 , binary = Gray_Rect ) # 得到两个矩形(满足嵌套关系的最大矩形)
                cor_0 , cor_1 , cor_2 , cor_3 = [0 , 0] , [0 , 0] , [0 , 0] , [0 , 0]
                # 矩形识别并记录数据
                if (rects == []):
                    pass
                else:
                    rect_x_central , rect_y_central = get_perspective_center(img , rects)
                    # 绘制中心
                    img.draw_cross(rect_x_central , rect_y_central, color = (255, 255, 255), size = 3, thickness = 1)
                    # 返回外矩形数据
                    corner = rects[0].corners()
                    cor_0 , cor_1 , cor_2 , cor_3 = corner[0],corner[1],corner[2],corner[3]
                # ----------------色块识别功能--------------------
                # 光斑追踪
                img_Gray = img_clean.copy().to_grayscale()
                max_white = 0     # 最大灰度值
                real_y = 0        # 最亮点y坐标(x已经确定)
                # 基础题: 最开始不打开激光,直接预测激光位置
                if (Competition_mode == 1):
                    real_y = get_real_y_distance(40 , real_y_min , 200 , real_y_max , distance )
                    if ( -10 < rect_x_central - real_x < 10 and -20 < rect_y_central - real_y < 20):
                        state = 1
                    else:
                        state = 0
                else :# 在预期区域内搜索亮光斑,作为激光位置
                    state = 1
                    for y in range( real_y_min, real_y_max ):
                        gray = img_Gray.get_pixel(real_x, y)
                        if gray > max_white:
                            max_white = gray
                            real_y = y
                real_y = int(real_y)
#                print(real_x , real_y)
                # 画圆形展示
                img.draw_circle(real_x, real_y, 3, color=[255, 0, 0])
                # ---------发送数据:0x12 0x10 数据(高低位) 0x5B---------
                # 记录位置->帧头
                data_payload = [0x12 , 0x10]       # 记录色块位置,初始帧:0x12 , 0x10

                # 记录位置->目标值
                data_payload.extend([get_high_val_of_hex(rect_x_central) , get_low_val_of_hex(rect_x_central), get_high_val_of_hex(rect_y_central) , get_low_val_of_hex(rect_y_central)])
                # 记录位置->实际值 :
                data_payload.extend([get_high_val_of_hex(real_x) , get_low_val_of_hex(real_x), get_high_val_of_hex(real_y) , get_low_val_of_hex(real_y)])
                # 记录位置->外矩形坐标 :
                data_payload.extend([ get_high_val_of_hex(cor_0[0])   , get_low_val_of_hex(cor_0[0]) , get_high_val_of_hex(480-cor_0[1])  , get_low_val_of_hex(480-cor_0[1]) ])
                data_payload.extend([ get_high_val_of_hex(cor_1[0])   , get_low_val_of_hex(cor_1[0]) , get_high_val_of_hex(480-cor_1[1])  , get_low_val_of_hex(480-cor_1[1]) ])
                data_payload.extend([ get_high_val_of_hex(cor_2[0])   , get_low_val_of_hex(cor_2[0]) , get_high_val_of_hex(480-cor_2[1])  , get_low_val_of_hex(480-cor_2[1]) ])
                data_payload.extend([ get_high_val_of_hex(cor_3[0])   , get_low_val_of_hex(cor_3[0]) , get_high_val_of_hex(480-cor_3[1])  , get_low_val_of_hex(480-cor_3[1]) ])

#                print(cor_0[0] , cor_0[1] ,cor_1[0] , cor_1[1] ,cor_2[0] , cor_2[1] , cor_3[0] ,cor_3[1]  )

                # 记录位置->帧尾
                data_payload.append(0x5B)
#                print(data_payload)
                uart.write(bytes(data_payload))
                Laser.value(state)
                # ------寻找红色色块------
#                # 红色(圆环)阈值
#                thresholds = [
#                    (22, 53, 10, 68, 11, 47),        # 红色
#                ]
                # 得到圆环色块
#                blobs = img.find_blobs( thresholds , False , x_stride = 1 , y_stride = 1 ,\
#                                       pixels_threshold = 20)
                # 遍历得到圆环的矩形变量
#                for blob in blobs :
#                    if blob.code() == 1:    # 红色色块
#                        color = (255, 0, 0)
#                        print("红色坐标: x={}, y={}".format(blob.cx(), blob.cy()))
#                    else:
#                        color = (255, 255, 255)
#                    img.draw_rectangle(blob.rect(), color = color, thickness = 2, fill = False)
#                    img.draw_circle(blob.cx(), blob.cy(), 3, color=color)
            else:
                # ----------------功能2:*******----------------
                pass


        # ------------------------------------尾处理-----------------------------------
        if (flag != 4 or flag != 5):
            img.draw_string_advanced(250, 40, 30 , "fps: {}".format(clock.fps()), color = (0, 255, 255))

        #img = img.copy(roi = (296,132,320,256))
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
