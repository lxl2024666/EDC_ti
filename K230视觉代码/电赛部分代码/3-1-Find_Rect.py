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

Gray_Rect = [61, 162] # 灰度列表

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

    #-----函数定义-----
    # 从矩形列表中得到两个最大的矩形
    def get_two_largest_rects(rects):
        # 按面积排序，从大到小
        rects_sorted = sorted(rects, key=lambda r: r.w() * r.h(), reverse=True)
        if len(rects_sorted) < 2:
            return None, None  # 少于两个矩形
        return rects_sorted[0], rects_sorted[1]
    # 判断矩形的嵌套关系,只有满足大矩形套小矩形才合格
    def is_rect_inside(outer, inner):
        # 简单方式：检查内矩形四个角是否都在外矩形内部
        outer_x1, outer_y1 = outer.x(), outer.y()
        outer_x2, outer_y2 = outer.x()+outer.w(), outer.y()+outer.h()
        corners = inner.corners()
        for x, y in corners:
            if not (outer_x1 <= x <= outer_x2 and outer_y1 <= y <= outer_y2):
                return False
        return True
    # 总函数1:寻找两个满足嵌套关系的大小矩形
    def Find_Two_Rects(img , threshold = 5000 , binary = Gray_Rect ):
        # 寻找矩形
        img_rect = img.copy().to_grayscale() # 把图像变为黑白图像
        img_rect = img_rect.binary( [ binary ] )
        rects = img_rect.find_rects(threshold = threshold)
        # 判断矩形个数,进行矩形面积排序,应该有且仅有2个
        outer , inner = get_two_largest_rects(rects)
        if outer == None :
            return []
        # 判断矩形嵌套关系
        if (is_rect_inside(outer , inner) == False):
            return []
        return [outer , inner]
    # 总函数2:寻找两个满足嵌套关系的大小矩形并且返回矩形平均中心
    def Get_Two_Rects_Central(img , threshold = 5000 , binary = Gray_Rect ):
        # 寻找矩形
        rects = Find_Two_Rects(img , threshold)
        x_rect_total = 0
        y_rect_total = 0
        if (rects != []):
            for rect in rects:
                corner = rect.corners()
                img.draw_line(corner[0][0], corner[0][1], corner[1][0], corner[1][1], color = (0, 255, 0), thickness = 2)
                img.draw_line(corner[2][0], corner[2][1], corner[1][0], corner[1][1], color = (0, 255, 0), thickness = 2)
                img.draw_line(corner[2][0], corner[2][1], corner[3][0], corner[3][1], color = (0, 255, 0), thickness = 2)
                img.draw_line(corner[0][0], corner[0][1], corner[3][0], corner[3][1], color = (0, 255, 0), thickness = 2)
                x_rect_total += corner[0][0] + corner[1][0] + corner[2][0] + corner[3][0]
                y_rect_total += corner[0][1] + corner[1][1] + corner[2][1] + corner[3][1]
            return x_rect_total // 8 , y_rect_total // 8
        else :
            return 0 , 0
    # 总函数3:寻找两个满足嵌套关系的大小矩形并且返回矩形的对角线中心(一定是矩形中心)
    def get_perspective_center(rects):
        cx_total = 0    # 总x中心
        cy_total = 0    # 总y中心
        for rect in rects :
            corner = rect.corners()
            (x0,y0), (x1,y1), (x2,y2), (x3,y3) = corner  # 假设顺序：左上、右上、右下、左下
            # 直线1
            A1 = y2 - y0
            B1 = x0 - x2
            C1 = x2*y0 - x0*y2
            # 直线2
            A2 = y3 - y1
            B2 = x1 - x3
            C2 = x3*y1 - x1*y3
            # 求交点 (cx, cy)
            det = A1 * B2 - A2 * B1  # 行列式，避免除零
            if det == 0:
                return 0 , 0  # 对角线平行（非四边形），返回None
            # 得到中心
            cx_total += (B1 * C2 - B2 * C1) / det
            cy_total += (A2 * C1 - A1 * C2) / det
            # 绘制矩形图像
            img.draw_line(corner[0][0], corner[0][1], corner[1][0], corner[1][1], color = (0, 255, 0), thickness = 2)
            img.draw_line(corner[2][0], corner[2][1], corner[1][0], corner[1][1], color = (0, 255, 0), thickness = 2)
            img.draw_line(corner[2][0], corner[2][1], corner[3][0], corner[3][1], color = (0, 255, 0), thickness = 2)
            img.draw_line(corner[0][0], corner[0][1], corner[3][0], corner[3][1], color = (0, 255, 0), thickness = 2)
        return int(cx_total // 2), int(cy_total // 2)  # 四舍五入为整数坐标

    while True:
        # 计算帧率
        clock.tick()
        os.exitpoint()

        # 拍照
        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        #-----核心代码-----

        # 测试
        rects = Find_Two_Rects(img , threshold = 500 , binary = Gray_Rect )

        if (rects == []):
            pass
        else:
            cx , cy = get_perspective_center(rects)
            img.draw_cross(cx , cy, color = (255, 255, 255), size = 3, thickness = 1)



#        # 绘出矩形边框
#        rect_x_central , rect_y_central =  Get_Two_Rects_Central(img , 500 , binary = Gray_Rect )


#        # 标出矩形中心
#        if (rect_x_central != 0 and rect_y_central != 0):
#            img.draw_circle(rect_x_central, rect_y_central, 15 , color = (0,255, 0) , thickness = 1, fill = False)

        # 试验
#        rects = Find_Two_Rects(img , threshold = 500 , binary = Gray_Rect)

#        if (rects != []):
#            outer_corners = rects[0].corners()
#            cx , cy = get_perspective_center(outer_corners)
#            if (cx != None ):
#                img.draw_cross(cx , cy, color = (255, 255, 255), size = 20, thickness = 2)







        #-----尾处理-----

        # 展示图像和帧率
        img.draw_string_advanced(40, 40, 30 , "fps: {}".format(clock.fps()), color = (0, 255, 255))

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
