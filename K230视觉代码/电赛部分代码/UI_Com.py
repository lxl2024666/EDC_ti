# 程序 电赛-库函数-UI界面函数
# 2025.8.1
# 声明:main中仅为图像作用,尽量不要保存数据

# ----------尺寸设定----------

# LCD屏幕尺寸
lcd_width = 800
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

# ----------函数定义----------
# ----1.按键检测----
def Key_GetNum(x, y,img ,top_margin = 10 , SetKeyNum = 16 , box_w = box_width , box_h = box_height , box_s = box_spacing):
    left_x = 0            # 左边的x
    right_x = frame_width - box_w # 右边的x
    img.draw_circle(x, y, 15 , color = (255,0, 0) , thickness = 2, fill = True) # 画辅助圆指引按键位置 # *************************
    # 左边列按钮
    if x >= left_x and x < left_x + box_w:
        y -= top_margin  # 去掉顶部边距方便判断
        for idx in range(1, SetKeyNum + 1, 2):  # 按钮编号1,3,5,...,11
            if y >= 0 and y < box_h:
                # 展示按键号码
#                    img.draw_string_advanced(250, 120, 30 , "Key: {}".format(idx), color = (0, 0, 255))
                return idx
            y -= box_spacing  # 判断是否是下一个按键

    # 右边列按钮
    elif x >= right_x and x < right_x + box_w:
        y -= top_margin
        for idx in range(2, SetKeyNum + 2 , 2):  # 按钮编号2,4,6,...,12
            if y >= 0 and y < box_h:
                # 展示按键号码
#                    img.draw_string_advanced(250, 120, 30 , "Key: {}".format(idx), color = (0, 0, 255))
                return idx
            y -= box_spacing  # 判断是否是下一个按键
    # 触摸点不在按钮范围
#        img.draw_string_advanced(250, 120, 30 , "Key: None", color = (0, 0, 255))
    return None

# ----2.字体展示换算----
def Display_Words(img, index, text , top_margin = 10 , num = 15 , font = 25, box_w = box_width , box_h = box_height , box_s = box_spacing):
    # 计算行号（0-5），index范围1-12
    row = (index - 1) // 2

    # 计算y坐标，文字靠近按钮中心向上调整一点
    y = top_margin + row * box_s + box_h // 2 - num # 20 这个数字可更改,凭感觉调节这个数字

    # 判断左右列，左列奇数，右列偶数
    if index % 2 == 1:
        x = box_w // 16     # 经过调整,这个位置还行
    else:
        x = frame_width - box_w * 15 // 16  # 经过调整,这个位置还行

    # 绘制文字
    img.draw_string_advanced(x, y, font, text, color=(255, 255, 255))

# ----3.菜单展示(flag = 2)----
def Draw_Menu(img, box_w = box_width , box_h = box_height , box_s = box_spacing):
    for j in [0, frame_width - box_w]:  # 一共就两个x轴位置:左 , 右
        for i in range(10, frame_height, box_s):
            img.draw_rectangle(j, i, box_w, box_h,color=(255, 255, 255), thickness=3, fill=False)

# ----4.按键加减处理----
def Update_Val(Key_num, var_value, Key_De, Key_Add, step=1 , min_num = 0 , max_num = 255 ):
    if Key_num == None :
        return var_value                         # 不变
    if Key_num == Key_De:                        # 标准减少的键码
        return max( min_num ,var_value - step )  # 减少
    elif Key_num == Key_Add:                     # 标准增加的键码
        return min( max_num ,var_value + step )  # 增加
    else:
        return var_value                         # 不变
# ----5.选择菜单展示----
def UI_Choose(img , flag):
    if (flag == 1):
        pass
    elif (flag == 2):
        Draw_Menu(img)
        Display_Words(img , 1 , "回到主页")
        Display_Words(img , 2 , "回到菜单")
        Display_Words(img , 3 , "调参模式")
        Display_Words(img , 4 , "LAB调节")
        Display_Words(img , 5 , "灰度调节")
    elif (flag == 3):
        Draw_Menu(img)
        Display_Words(img , 1 , "回到主页")
        Display_Words(img , 2 , "回到菜单")
        Display_Words(img , 3 , "a--")
        Display_Words(img , 4 , "a++")
        Display_Words(img , 5 , "real_x--")
        Display_Words(img , 6 , "real_x++")
        Display_Words(img , 7 , "y_min--")
        Display_Words(img , 8 , "y_min++")
        Display_Words(img , 9 , "y_max--")
        Display_Words(img ,10 , "y_max++")
        Display_Words(img ,11 , "distance--")
        Display_Words(img ,12 , "distance++")
        Display_Words(img ,13 , "比赛模式切换")
        Display_Words(img ,15 , "保存数据")
    elif (flag == 4):
        Draw_Menu(img)
        Display_Words(img , 1 , "回到主页")
        Display_Words(img , 2 , "回到菜单")

        Display_Words(img , 3 , "L_Min--")
        Display_Words(img , 4 , "L_Min++")

        Display_Words(img , 5 , "L_Max--")
        Display_Words(img , 6 , "L_Max++")

        Display_Words(img , 7 , "A_Min--")
        Display_Words(img , 8 , "A_Min++")

        Display_Words(img , 9 , "A_Max--")
        Display_Words(img ,10 , "A_Max++")

        Display_Words(img ,11 , "B_Min--")
        Display_Words(img ,12 , "B_Min++")

        Display_Words(img ,13 , "B_Max--")
        Display_Words(img ,14 , "B_Max++")

        Display_Words(img ,15 , "切换LAB")
        Display_Words(img ,16 , "保存LAB")
    else :  # flag == 5
        Draw_Menu(img)
        Display_Words(img , 1 , "回到主页")
        Display_Words(img , 2 , "回到菜单")

        Display_Words(img , 3 , "G_Min--")
        Display_Words(img , 4 , "G_Min++")

        Display_Words(img , 5 , "G_Max--")
        Display_Words(img , 6 , "G_Max++")

        Display_Words(img , 7 , "切换灰度")
        Display_Words(img , 8 , "保存灰度")
# ------------------------------主程序----------------------------------

if __name__ == "__main__":

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

    # --------------------建立变量--------------------
    # ----------UI界面相关变量----------
    # 触摸初始化
    tp = TOUCH(0)
    flag = 1            # 系统标志位初始化
    touch_counter = 0   # 长按时间计时

    # ----------摄像头相关变量----------
    # 摄像头初始化
    sensor = None

    # ----------Key和LED调试变量-----------
    fpioa = FPIOA()
    fpioa.set_function(52 , FPIOA.GPIO52 ) # LED对象
    fpioa.set_function(21 , FPIOA.GPIO21 ) # Key对象

    ## 设置引脚状态
    LED = Pin(52 , Pin.OUT)
    Key = Pin(21 , Pin.IN , Pin.PULL_UP)
    # -----------串口初始化-----------
    fpioa = FPIOA()
    fpioa.set_function(11 , FPIOA.UART2_TXD)
    fpioa.set_function(12 , FPIOA.UART2_RXD)
    uart = UART(UART.UART2, 115200) #设置串口号2和波特率,这就够了

    # ----------调试参数设置----------
    # 一些调试参数
    a , b , c , d = 10 , 80 , 10 , 25

    # 数据存储行数
    LAB_R_Line  = 1   # LAB_R的文件存储位置
    LAB_Z_Line  = 2   # LAB_Z的文件存储位置
    Gray_Line   = 3   # 灰度的文件存储位置

    LAB_R = [0,0,0,0,0,0]
    LAB_Z = [0,0,0,0,0,0]
    LAB_test = [0, 100, -127, 128, -127, 128]

    Gray_Rect = [0,100]
    Gray_test = [0,100]

    # ----------激光位置参数设置----------

    frame_w = 640
    frame_h = 480

    cut_x = 90
    cut_y = 0
    cut_w = 380
    cut_h = 180

    mode = 1    # 追踪色块模式
    #mode = 2    # 识别矩形模式
    LAB_Change_Seq = 0  # 调节色块的序列,红色:0 , 紫色:1

    try:
        # ----------初始化配置----------
        # 初始化摄像头
        sensor = Sensor(width=1280, height=960)
        sensor.reset()
        sensor.set_framesize(width=640,height=480)
        sensor.set_pixformat(Sensor.RGB565)

        Display.init(Display.ST7701, to_ide=True)   # 初始化显示器
        MediaManager.init()                         # 初始化媒体管理器
        sensor.run()                                # 启动 sensor
        clock = time.clock()                        # 开始计时帧率

        # ----------从文件读取数据----------
        Gray_Rect = File_Read_Data( Gray_Line)  # 从文件读取数据
        LAB_R     = File_Read_Data( LAB_R_Line) # 从文件读取数据
        LAB_Z     = File_Read_Data( LAB_Z_Line) # 从文件读取数据

        while True:
            # 计算帧率
            clock.tick()
            os.exitpoint()

            # 拍照
            img = sensor.snapshot(chn=CAM_CHN_ID_0)

            #-----UI界面与相关UI功能-----
            points = tp.read()
            # 坐标展示与flag下处理
            if points != () :
                print(points) # 打印原始数据
                for i in range(len(points)):
                    print('x'+str(i)+'=' , points[i].x , 'y'+str(i)+'=',points[i].y )
                    KeyNum = Key_GetNum(points[i].x , points[i].y , img)
                    print('KeyNum: {}'.format(KeyNum))
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
                            flag = KeyNum
                        elif (KeyNum >= 3 and KeyNum <= 10):
                            a = Update_Val(KeyNum , a , 3 , 4 , 2 , -20 )
                            b = Update_Val(KeyNum , b , 5 , 6 , 1)
                            c = Update_Val(KeyNum , c , 7 , 8 , 3)
                            d = Update_Val(KeyNum , d , 9 ,10 , 2)
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
                            Gray_test[0] = Update_Val(KeyNum , Gray_test[0] ,3 ,4 ,3 , 0, 255)
                            Gray_test[1] = Update_Val(KeyNum , Gray_test[1] ,5 ,6 ,3 , 0, 255)
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
            if (flag == 1):
                pass
            if (flag == 2):
                Draw_Menu(img)
                Display_Words(img , 1 , "回到主页")
                Display_Words(img , 2 , "回到菜单")
                Display_Words(img , 3 , "调参模式")
                Display_Words(img , 4 , "LAB调节")
                Display_Words(img , 5 , "灰度调节")

            if (flag == 3):
                Draw_Menu(img)
                Display_Words(img , 1 , "回到主页")
                Display_Words(img , 2 , "回到菜单")
                Display_Words(img , 3 , "a--")
                Display_Words(img , 4 , "a++")
                Display_Words(img , 5 , "b--")
                Display_Words(img , 6 , "b++")
                Display_Words(img , 7 , "c--")
                Display_Words(img , 8 , "c++")
                Display_Words(img , 9 , "d--")
                Display_Words(img ,10 , "d++")

            if (flag == 4):
                Draw_Menu(img)
                Display_Words(img , 1 , "回到主页")
                Display_Words(img , 2 , "回到菜单")

                Display_Words(img , 3 , "L_Min--")
                Display_Words(img , 4 , "L_Min++")

                Display_Words(img , 5 , "L_Max--")
                Display_Words(img , 6 , "L_Max++")

                Display_Words(img , 7 , "A_Min--")
                Display_Words(img , 8 , "A_Min++")

                Display_Words(img , 9 , "A_Max--")
                Display_Words(img ,10 , "A_Max++")

                Display_Words(img ,11 , "B_Min--")
                Display_Words(img ,12 , "B_Min++")

                Display_Words(img ,13 , "B_Max--")
                Display_Words(img ,14 , "B_Max++")

                Display_Words(img ,15 , "切换LAB")
                Display_Words(img ,16 , "保存LAB")

                # 先进行图像格式转换:二值化
                img_blob = img.to_rgb565().binary( [LAB_test] ).copy(roi = (box_width , 10 , frame_width - box_width * 2 , frame_height - 100))
                # 贴图,可以开始调灰度了
                img.draw_image(img_blob, box_width, 10)

            if (flag == 5):
                Draw_Menu(img)
                Display_Words(img , 1 , "回到主页")
                Display_Words(img , 2 , "回到菜单")

                Display_Words(img , 3 , "G_Min--")
                Display_Words(img , 4 , "G_Min++")

                Display_Words(img , 5 , "G_Max--")
                Display_Words(img , 6 , "G_Max++")

                Display_Words(img , 7 , "切换灰度")
                Display_Words(img , 8 , "保存灰度")

                # 先进行图像格式转换,灰度+二值化
                img_rect = img.to_grayscale() # 把图像变为黑白图像
                img_rect = img_rect.binary( [Gray_test] ).copy(roi = (box_width , 10 , frame_width - box_width * 2 , frame_height - 100))
                # 贴图,可以开始调灰度了
                img.draw_image(img_rect, box_width, 10)


            if (flag != 4 or flag != 5):
                img.draw_string_advanced(250, 80, 30 , "flag: {}".format(flag), color = (0, 255, 255))
                img.draw_string_advanced(250, 40, 30 , "fps: {}".format(clock.fps()), color = (0, 255, 255))


            # ------------------------------------尾处理-----------------------------------
            time.sleep_ms(50)
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
1.图像显示重点:
    ①初始化(必备,写在主函数) ②拍照,必备,写在while,这样才能刷新
    ③图像处理:有多种方法,如灰度,彩色,二值化,等转换or显示方法,  多图像还可以进行裁切+贴图
    ④展示图像(Display)
2.贴图:
    先处理:(img是主图,img_rect是贴图,主图作为背景不进行处理,贴图需要处理(模式转换,copy,裁切))
        img_rect = img.to_grayscale() # 把图像变为黑白图像
        img_rect = img_rect.binary( [Gray_test] ).copy(roi = (box_width , 10 , frame_width - box_width * 2 , frame_height - 100)) # roi=(160, 120, 320, 240)

'''






