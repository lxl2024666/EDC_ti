# 程序 电赛-库函数:文件操作
# 2025.8.1

# --------------------函数定义--------------------

# ----1.文件打开并读取数据(仅限于列表,后面的功能后面再开发)------
# 读取文件某一行数据,使用List接收数据,读取第Line行(line>0)
def File_Read_Data(line , path = "competition.txt"):
    # 读取文件
    try:
        f = open('/sdcard/' + path , 'r')
        lines = f.readlines()
        f.close()
    except:
        return []
    # 读取数据
    if len(lines) >= line:
        line_str = lines[line - 1].strip()     # 去除换行符,下为例子
        str_list = line_str.split(',')         # ['123', '456']
        int_list = [int(s) for s in str_list]  # [123, 456]
        return int_list
    return []

# ----2.文件打开并修改文件数据(仅限于列表,后面的功能后面再开发)------
# 读取文件某一行数据,使用List接收数据,读取第Line行(line>0)
def File_Write_Data(line, list_change , path = 'competition.txt'):
    # 尝试打开文件
    try:
        with open('/sdcard/' + path, 'r') as f:
            lines = f.readlines()
    except:
        lines = []
    # 预建立插入数据列表
    new_line = ','.join([str(i) for i in list_change]) + '\n'
    # 替换或扩展内容
    if line <= len(lines):
        lines[line - 1] = new_line
    else:
        while len(lines) < line - 1:
            lines.append('\n')
        lines.append(new_line)
    # 写入数据
    try:
        with open('/sdcard/' + path , 'w') as f:
            for line_str in lines:
                f.write(line_str)
    except Exception as e:
        print("文件写入异常:", e)
        return False
    return True

# 示例程序
import time
if __name__ == "__main__":
    # 示例数据
    a = 1
    b = 1
    while True :
        # 变量初始化
        a += 1
        b += 2
        list1 = []
        list2 = [ a , b ]
        # 读数据
        list1 = File_Read_Data(1 , path = "File_test.txt")
        # 写数据
        File_Write_Data(1, list2 , path = "File_test.txt")
        # 打印结果
        print("list1:")
        print(list1)
        print("list2:")
        print(list2)
        # 休息
        time.sleep_ms(500)
