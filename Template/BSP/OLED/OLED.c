/**
 * @file      OLED.c
 * @brief     SSD1306 OLED显示屏驱动库的实现文件 (软件I2C)
 * @details   实现了通过软件模拟I2C协议驱动OLED的所有函数。
 * @author    Jianing Wang
 * @version   1.1
 * @date      2025-07-31
 */

#include "OLED.h"
#include "OLED_Font.h"
#include <stdint.h>

// 外部依赖一个微秒延时函数，请确保其已在项目中实现
// extern void Delay_us(uint32_t us);
// 如果您的延时函数在AllHeader.h中，请包含它
#include "AllHeader.h"


/********************************************************************************
* *
* 内部I2C通信函数 (Internal I2C Functions)             *
* *
********************************************************************************/

/**
 * @brief  产生I2C起始信号
 * @param  None
 * @retval None
 */
static void I2C_Start(void)
{
    OLED_SDA_Set();
    OLED_SCL_Set();
    OLED_SDA_Clr();
    Delay_us(1); // 延时确保时序稳定
    OLED_SCL_Clr();
}

/**
 * @brief  产生I2C停止信号
 * @param  None
 * @retval None
 */
static void I2C_Stop(void)
{
    OLED_SDA_Clr();
    OLED_SCL_Set();
    OLED_SDA_Set();
}

/**
 * @brief  等待从机（OLED）的ACK应答信号
 * @param  None
 * @retval uint8_t 0: 收到ACK (成功), 1: 未收到ACK (失败)
 */
static uint8_t OLED_I2C_WaitAck(void)
{
    uint8_t ack = 1;      // 默认为无应答
    OLED_SDA_Set();       // 主机释放SDA总线，以便从机可以拉低
    Delay_us(1);
    OLED_SCL_Set();       // 主机拉高SCL，发出时钟信号
    Delay_us(1);
    if (OLED_SDA_Read() == 0) // 读取SDA线，如果为低电平，则表示从机已应答
    {
        ack = 0;
    }
    OLED_SCL_Clr();       // 拉低SCL，完成一次时钟周期
    return ack;
}

/**
 * @brief  通过I2C发送一个字节
 * @param  dat 要发送的字节
 * @retval None
 */
static void OLED_Send_Byte(uint8_t dat)
{
    uint8_t i;
    for (i = 0; i < 8; i++)
    {
        OLED_SCL_Clr(); // 拉低时钟线，准备发送数据位
        if (dat & 0x80) // 从最高位开始发送
        {
            OLED_SDA_Set();
        }
        else
        {
            OLED_SDA_Clr();
        }
        Delay_us(1);
        OLED_SCL_Set(); // 拉高时钟线，从机在此刻读取数据位
        Delay_us(1);
        OLED_SCL_Clr(); // 拉低时钟线，完成一位数据发送
        dat <<= 1;      // 左移一位，准备发送下一位
    }
}

/**
 * @brief  向OLED写入一个字节（内部基础函数）
 * @param  dat  要写入的字节内容
 * @param  mode 模式选择, 0:命令 (OLED_CMD), 1:数据 (OLED_DATA)
 * @retval None
 */
void OLED_WR_Byte(uint8_t dat, uint8_t mode)
{
    I2C_Start();
    OLED_Send_Byte(0x78); // 发送OLED的I2C从机地址
    if (OLED_I2C_WaitAck() != 0) { I2C_Stop(); return; }

    if (mode == OLED_DATA)
    {
        OLED_Send_Byte(0x40); // 写入数据
    }
    else
    {
        OLED_Send_Byte(0x00); // 写入命令
    }
    if (OLED_I2C_WaitAck() != 0) { I2C_Stop(); return; }

    OLED_Send_Byte(dat);
    if (OLED_I2C_WaitAck() != 0) { I2C_Stop(); return; }

    I2C_Stop();
}

/**
 * @brief  向OLED连续写入多个命令
 * @details  通过一次I2C事务发送多个命令，比单个发送效率更高。
 * @param  cmds 指向命令数组的指针
 * @param  len  命令的数量
 * @retval None
 */
static void OLED_Write_ContinuousCmd(uint8_t *cmds, uint8_t len)
{
    if (len == 0) return;

    I2C_Start();
    OLED_Send_Byte(0x78);
    if (OLED_I2C_WaitAck() != 0) { I2C_Stop(); return; }

    OLED_Send_Byte(0x00); // 命令模式
    if (OLED_I2C_WaitAck() != 0) { I2C_Stop(); return; }

    for (uint8_t i = 0; i < len; i++) {
        OLED_Send_Byte(cmds[i]);
        if (OLED_I2C_WaitAck() != 0) { I2C_Stop(); return; }
    }
    I2C_Stop();
}

/**
 * @brief  向OLED连续写入多个数据（清屏时使用）
 * @details  此函数在清屏时使用，为了追求最高速度，忽略了ACK检查。
 * @param  data 指向数据数组的指针
 * @param  len  数据的数量
 * @retval None
 */
static void OLED_Write_ContinuousData_NoAck(uint8_t *data, uint16_t len)
{
    if (len == 0) return;

    I2C_Start();
    OLED_Send_Byte(0x78);
    (void)OLED_I2C_WaitAck(); // 忽略ACK检查

    OLED_Send_Byte(0x40);
    (void)OLED_I2C_WaitAck(); // 忽略ACK检查

    for (uint16_t i = 0; i < len; i++) {
        OLED_Send_Byte(data[i]);
        (void)OLED_I2C_WaitAck(); // 忽略ACK检查
    }
    I2C_Stop();
}


/********************************************************************************
* *
* OLED功能函数 (OLED Public Functions)                 *
* *
********************************************************************************/

/**
 * @brief  设置显示颜色反转
 * @param  i 0: 正常显示, 1: 颜色反转 (黑底白字变白底黑字)
 * @retval None
 */
void OLED_ColorTurn(uint8_t i)
{
    if (i == 0)
    {
        OLED_WR_Byte(0xA6, OLED_CMD); // 正常显示
    }
    else
    {
        OLED_WR_Byte(0xA7, OLED_CMD); // 反色显示
    }
}

/**
 * @brief  设置屏幕内容旋转180度
 * @param  i 0: 正常显示, 1: 旋转180度
 * @retval None
 */
void OLED_DisplayTurn(uint8_t i)
{
    if (i == 0)
    {
        OLED_WR_Byte(0xC8, OLED_CMD); // 正常上下扫描
        OLED_WR_Byte(0xA1, OLED_CMD); // 正常左右映射
    }
    else
    {
        OLED_WR_Byte(0xC0, OLED_CMD); // 上下反置
        OLED_WR_Byte(0xA0, OLED_CMD); // 左右反置
    }
}

/**
 * @brief  设置光标（写入指针）的位置
 * @param  x 列坐标 (0-127)
 * @param  y 页坐标 (0-7)
 * @retval None
 */
void OLED_Set_Pos(uint8_t x, uint8_t y)
{
    // 优化：将三个设置坐标的命令通过一次I2C事务发送
    uint8_t cmds[3];
    cmds[0] = 0xb0 + y;                  // 设置页地址 (0xB0-0xB7)
    cmds[1] = ((x & 0xf0) >> 4) | 0x10;  // 设置列地址高4位
    cmds[2] = x & 0x0f;                  // 设置列地址低4位
    OLED_Write_ContinuousCmd(cmds, 3);
}

/**
 * @brief  打开OLED显示
 * @param  None
 * @retval None
 */
void OLED_Display_On(void)
{
    OLED_WR_Byte(0x8D, OLED_CMD); // 设置电荷泵
    OLED_WR_Byte(0x14, OLED_CMD); // 使能电荷泵
    OLED_WR_Byte(0xAF, OLED_CMD); // 点亮屏幕
}

/**
 * @brief  关闭OLED显示 (进入休眠)
 * @param  None
 * @retval None
 */
void OLED_Display_Off(void)
{
    OLED_WR_Byte(0x8D, OLED_CMD); // 设置电荷泵
    OLED_WR_Byte(0x10, OLED_CMD); // 关闭电荷泵
    OLED_WR_Byte(0xAE, OLED_CMD); // 关闭屏幕
}

/**
 * @brief  清空整个OLED屏幕
 * @details  通过连续写入128个0的方式快速清空一页，循环8次清空整个屏幕。
 * @param   None
 * @retval  None
 */
void OLED_Clear(void)
{
    // 静态缓冲区，避免在栈上重复创建大数组，提高效率
    static uint8_t clear_buf[128] = {0};

    for (uint8_t i = 0; i < 8; i++)
    {
        OLED_Set_Pos(0, i);
        // 使用特殊优化的无ACK检查连续写入函数，以达到最快清屏速度
        OLED_Write_ContinuousData_NoAck(clear_buf, 128);
    }
}

/**
 * @brief  在指定位置显示一个ASCII字符
 * @param  x      起始列坐标 (0-127)
 * @param  y      起始页坐标 (0-7 for 16-size font)
 * @param  chr    要显示的ASCII字符
 * @param  sizey  字体大小 (支持 8 和 16)
 * @retval None
 */
void OLED_ShowChar(uint8_t x, uint8_t y, uint8_t chr, uint8_t sizey)
{
    uint8_t c = chr - ' '; // 计算字符在字库数组中的偏移量
    uint16_t i = 0;
    uint8_t sizex = sizey / 2; // 字符宽度通常是高度的一半
    uint16_t char_bytes;       // 一个字符所占的总字节数

    if (sizey == 8)
    {
        char_bytes = 6; // 6x8 字体
        OLED_Set_Pos(x, y);
        for (i = 0; i < char_bytes; i++)
        {
            OLED_WR_Byte(asc2_0806[c][i], OLED_DATA);
        }
    }
    else if (sizey == 16)
    {
        char_bytes = 16; // 8x16 字体
        // 8x16字体占2页，需要分别设置位置并写入
        OLED_Set_Pos(x, y); // 写第一页 (上半部分)
        for (i = 0; i < 8; i++)
        {
            OLED_WR_Byte(asc2_1608[c][i], OLED_DATA);
        }
        OLED_Set_Pos(x, y + 1); // 写第二页 (下半部分)
        for (i = 8; i < 16; i++)
        {
            OLED_WR_Byte(asc2_1608[c][i], OLED_DATA);
        }
    }
    else
    {
        // 其他字号可在此添加
        return;
    }
}

/**
 * @brief  计算m的n次方 (内部使用)
 * @param  m 底数
 * @param  n 指数
 * @retval uint32_t 计算结果
 */
static uint32_t oled_pow(uint8_t m, uint8_t n)
{
    uint32_t result = 1;
    while (n--) result *= m;
    return result;
}

/**
 * @brief  显示一个无符号十进制数字
 * @param  x      起始列坐标 (0-127)
 * @param  y      起始页坐标 (0-7)
 * @param  num    要显示的数字 (0-4294967295)
 * @param  len    要显示的数字长度
 * @param  sizey  字体大小
 * @retval None
 */
void OLED_ShowNum(uint8_t x, uint8_t y, uint32_t num, uint8_t len, uint8_t sizey)
{
    uint8_t t, temp;
    uint8_t enshow = 0; // 用于处理前导零的标志
    for (t = 0; t < len; t++)
    {
        temp = (num / oled_pow(10, len - t - 1)) % 10;
        if (enshow == 0 && t < (len - 1))
        {
            if (temp == 0)
            {
                // 如果是前导零，则显示空格
                OLED_ShowChar(x + (sizey / 2) * t, y, ' ', sizey);
                continue;
            }
            else
            {
                enshow = 1; // 一旦遇到非零数字，开始正常显示
            }
        }
        OLED_ShowChar(x + (sizey / 2) * t, y, temp + '0', sizey);
    }
}

/**
 * @brief  在指定位置显示字符串
 * @param  x      起始列坐标 (0-127)
 * @param  y      起始页坐标 (0-7)
 * @param  chr    指向字符串的指针
 * @param  sizey  字体大小
 * @retval None
 */
void OLED_ShowString(uint8_t x, uint8_t y, uint8_t *chr, uint8_t sizey)
{
    uint8_t j = 0;
    while (chr[j] != '\0')
    {
        OLED_ShowChar(x, y, chr[j], sizey);
        x += sizey / 2; // 根据字体宽度移动x坐标
        j++;
    }
}

/**
 * @brief  在指定位置显示一个16x16的汉字
 * @param  x      起始列坐标 (0-127)
 * @param  y      起始页坐标 (0-7)
 * @param  no     要显示的汉字在字库 `Hzk` 中的索引号
 * @retval None
 */
void OLED_ShowChinese(uint8_t x, uint8_t y, uint8_t no)
{
    uint8_t i;
    uint16_t addr = no * 32; // 每个汉字占32字节

    // 16x16汉字占2页，需要分别设置位置并写入
    OLED_Set_Pos(x, y); // 写第一页 (上半部分)
    for (i = 0; i < 16; i++)
    {
        OLED_WR_Byte(Hzk[no][i], OLED_DATA);
    }
    OLED_Set_Pos(x, y + 1); // 写第二页 (下半部分)
    for (i = 16; i < 32; i++)
    {
        OLED_WR_Byte(Hzk[no][i], OLED_DATA);
    }
}

/**
 * @brief  显示一幅位图
 * @param  x      图片左上角起始列坐标 (0-127)
 * @param  y      图片左上角起始页坐标 (0-7)
 * @param  sizex  图片的宽度（像素）
 * @param  sizey  图片的高度（像素）
 * @param  BMP    指向位图数据数组的指针 (数据格式为纵向取模)
 * @retval None
 */
void OLED_DrawBMP(uint8_t x, uint8_t y, uint8_t sizex, uint8_t sizey, uint8_t BMP[])
{
    uint16_t j = 0;
    uint8_t i, m;
    uint8_t page_count = sizey / 8 + ((sizey % 8) ? 1 : 0); // 计算图片占用的页数

    for (i = 0; i < page_count; i++)
    {
        OLED_Set_Pos(x, i + y);
        for (m = 0; m < sizex; m++)
        {
            OLED_WR_Byte(BMP[j++], OLED_DATA);
        }
    }
}

/**
 * @brief  OLED驱动初始化
 * @details  向OLED发送一串初始化指令来配置其工作模式。
 * @param  None
 * @retval None
 */
void OLED_Init(void)
{
    // GPIO初始化应在外部完成 (例如通过SysConfig)
    // Delay_ms(100); // 如果需要上电延时，可以在此添加

    OLED_WR_Byte(0xAE, OLED_CMD); //--关闭显示
    OLED_WR_Byte(0x40, OLED_CMD); //--设置起始行地址
    OLED_WR_Byte(0xB0, OLED_CMD); //--设置起始页地址
    OLED_WR_Byte(0xC8, OLED_CMD); //--行扫描方向：从上到下
    OLED_WR_Byte(0xA1, OLED_CMD); //--列映射：从左到右
    OLED_WR_Byte(0xA6, OLED_CMD); //--正常显示（非反显）
    OLED_WR_Byte(0xA8, OLED_CMD); //--设置多路复用率
    OLED_WR_Byte(0x3F, OLED_CMD); //--1/64 duty
    OLED_WR_Byte(0xD3, OLED_CMD); //--设置显示偏移
    OLED_WR_Byte(0x00, OLED_CMD); //--无偏移
    OLED_WR_Byte(0xD5, OLED_CMD); //--设置时钟分频
    OLED_WR_Byte(0x80, OLED_CMD); //--默认分频比
    OLED_WR_Byte(0xD9, OLED_CMD); //--设置预充电周期
    OLED_WR_Byte(0xF1, OLED_CMD);
    OLED_WR_Byte(0xDA, OLED_CMD); //--设置COM引脚硬件配置
    OLED_WR_Byte(0x12, OLED_CMD);
    OLED_WR_Byte(0xDB, OLED_CMD); //--设置VCOMH反压值
    OLED_WR_Byte(0x40, OLED_CMD);
    OLED_WR_Byte(0x8D, OLED_CMD); //--设置电荷泵
    OLED_WR_Byte(0x14, OLED_CMD); //--使能电荷泵
    OLED_WR_Byte(0x20, OLED_CMD); //--设置寻址模式
    OLED_WR_Byte(0x02, OLED_CMD); //--页寻址模式

    OLED_Clear();                 // 清屏
    OLED_WR_Byte(0xAF, OLED_CMD); //--开启显示
}