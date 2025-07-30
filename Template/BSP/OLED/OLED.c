/**
 * @file oled.c
 * @brief TI MSPM0G3507平台OLED显示驱动 (基于I2C通信)
 * @author 移植自STM32平台
 * @date 2024
 * 
 * 支持0.96寸128x64 OLED显示屏 (SSD1306控制器)
 * 通过I2C接口进行通信
 */

#include "oled.h"
#include "oledfont.h"

// 几个变量声明
uint8_t **Hzk;

// 初始化命令数组
uint8_t CMD_Data[] = {
    0xAE, 0x00, 0x10, 0x40, 0xB0, 0x81, 0xFF, 0xA1, 0xA6, 0xA8, 0x3F,
    0xC8, 0xD3, 0x00, 0xD5, 0x80, 0xD8, 0x05, 0xD9, 0xF1, 0xDA, 0x12,
    0xD8, 0x30, 0x8D, 0x14, 0xAF
};

/**
 * @brief 发送初始化命令序列
 */
void WriteCmd(void)
{
    uint8_t i = 0;
    for(i = 0; i < 27; i++) {
        // 使用TI DriverLib I2C函数发送命令
        DL_I2C_startControllerTransfer(OLED_I2C_INST, OLED_I2C_ADDR, 
                                       DL_I2C_CONTROLLER_DIRECTION_TX, 2);
        
        // 发送寄存器地址
        DL_I2C_flushControllerTXFIFO(OLED_I2C_INST);
        DL_I2C_fillControllerTXFIFO(OLED_I2C_INST, OLED_CMD_REG, 1);
        
        // 发送命令数据
        DL_I2C_fillControllerTXFIFO(OLED_I2C_INST, &CMD_Data[i], 1);
        
        // 等待传输完成
        while(DL_I2C_getControllerStatus(OLED_I2C_INST) & DL_I2C_CONTROLLER_STATUS_BUSY_BUS);
    }
}

/**
 * @brief 向OLED发送控制命令
 * @param cmd 命令字节
 */
void OLED_WR_CMD(uint8_t cmd)
{
    uint8_t data[2] = {OLED_CMD_REG, cmd};
    
    DL_I2C_startControllerTransfer(OLED_I2C_INST, OLED_I2C_ADDR, 
                                   DL_I2C_CONTROLLER_DIRECTION_TX, 2);
    
    DL_I2C_flushControllerTXFIFO(OLED_I2C_INST);
    DL_I2C_fillControllerTXFIFO(OLED_I2C_INST, data, 2);
    
    // 等待传输完成
    while(DL_I2C_getControllerStatus(OLED_I2C_INST) & DL_I2C_CONTROLLER_STATUS_BUSY_BUS);
}

/**
 * @brief 向OLED发送显示数据
 * @param data 数据字节
 */
void OLED_WR_DATA(uint8_t data)
{
    uint8_t tx_data[2] = {OLED_DATA_REG, data};
    
    DL_I2C_startControllerTransfer(OLED_I2C_INST, OLED_I2C_ADDR, 
                                   DL_I2C_CONTROLLER_DIRECTION_TX, 2);
    
    DL_I2C_flushControllerTXFIFO(OLED_I2C_INST);
    DL_I2C_fillControllerTXFIFO(OLED_I2C_INST, tx_data, 2);
    
    // 等待传输完成
    while(DL_I2C_getControllerStatus(OLED_I2C_INST) & DL_I2C_CONTROLLER_STATUS_BUSY_BUS);
}
/**
 * @brief 初始化OLED显示屏
 */
void OLED_Init(void)
{ 	
    // 延时200ms等待OLED稳定
    DL_Common_delayCycles(6400000);  // 200ms @ 32MHz
    WriteCmd();
}
/**
 * @brief 清除整个OLED显示屏
 * @note size12 size16字体需要清两行，其他函数有类似情况
 */
void OLED_Clear(void)
{
    uint8_t i, n;		    
    for(i = 0; i < 8; i++)  
    {  
        OLED_WR_CMD(0xb0 + i);  // 设置页地址
        OLED_WR_CMD(0x00);      // 设置列低地址
        OLED_WR_CMD(0x10);      // 设置列高地址
        for(n = 0; n < 128; n++)
            OLED_WR_DATA(0);    // 清除数据
    } 
}

/**
 * @brief 清除指定行
 * @param i 页地址 (0-7)
 */
void OLED_Clearrow(uint8_t i)
{
    uint8_t n;
    OLED_WR_CMD(0xb0 + i);      // 设置页地址
    OLED_WR_CMD(0x00);          // 设置列低地址
    OLED_WR_CMD(0x10);          // 设置列高地址
    for(n = 0; n < 128; n++)
        OLED_WR_DATA(0);        // 清除数据
}
/**
 * @brief 开启OLED显示
 */
void OLED_Display_On(void)
{
    OLED_WR_CMD(0X8D);  // SET DCDC命令
    OLED_WR_CMD(0X14);  // DCDC ON
    OLED_WR_CMD(0XAF);  // DISPLAY ON
}

/**
 * @brief 关闭OLED显示
 */
void OLED_Display_Off(void)
{
    OLED_WR_CMD(0X8D);  // SET DCDC命令
    OLED_WR_CMD(0X10);  // DCDC OFF
    OLED_WR_CMD(0XAE);  // DISPLAY OFF
}

/**
 * @brief 设置显示位置
 * @param x 列坐标 (0-127)
 * @param y 页坐标 (0-7)
 */		   			 
void OLED_Set_Pos(uint8_t x, uint8_t y) 
{ 	
    OLED_WR_CMD(0xb0 + y);                  // 设置页地址
    OLED_WR_CMD(((x & 0xf0) >> 4) | 0x10);  // 设置列高地址
    OLED_WR_CMD(x & 0x0f);                  // 设置列低地址
} 
/**
 * @brief 全屏点亮 (用于测试)
 */
void OLED_On(void)  
{  
    uint8_t i, n;		    
    for(i = 0; i < 8; i++)  
    {  
        OLED_WR_CMD(0xb0 + i);      // 设置页地址（0~7）
        OLED_WR_CMD(0x00);          // 设置显示位置—列低地址
        OLED_WR_CMD(0x10);          // 设置显示位置—列高地址   
        for(n = 0; n < 128; n++)
            OLED_WR_DATA(1);        // 点亮像素
    }
}

/**
 * @brief 计算m的n次方 (整数运算)
 * @param m 底数
 * @param n 指数
 * @return m的n次方
 */
unsigned int oled_pow(uint8_t m, uint8_t n)
{
    unsigned int result = 1;	 
    while(n--) result *= m;    
    return result;
}

/**
 * @brief 在指定位置显示一个字符，包括部分字符
 * @param x 列坐标 (0~127)
 * @param y 页坐标 (0~7)
 * @param chr 要显示的字符
 * @param Char_Size 字体大小 (16/12)
 */
void OLED_ShowChar(uint8_t x, uint8_t y, uint8_t chr, uint8_t Char_Size)
{      	
    unsigned char c = 0, i = 0;	
    c = chr - ' '; // 得到偏移后的值			
    if(x > 128 - 1) { x = 0; y = y + 2; }
    
    if(Char_Size == 16)
    {
        OLED_Set_Pos(x, y);	
        for(i = 0; i < 8; i++)
            OLED_WR_DATA(F8x16[c * 16 + i]);
        OLED_Set_Pos(x, y + 1);
        for(i = 0; i < 8; i++)
            OLED_WR_DATA(F8x16[c * 16 + i + 8]);
    }
    else 
    {	
        OLED_Set_Pos(x, y);
        for(i = 0; i < 6; i++)
            OLED_WR_DATA(F6x8[c][i]);
    }
}
/**
 * @brief 显示数字
 * @param x 起点列坐标
 * @param y 起点页坐标	 
 * @param num 数值(0~4294967295)
 * @param len 数字的位数
 * @param size2 字体大小
 */
void OLED_ShowNum(uint8_t x, uint8_t y, unsigned int num, uint8_t len, uint8_t size2)
{         	
    uint8_t t, temp;
    uint8_t enshow = 0;						   
    for(t = 0; t < len; t++)
    {
        temp = (num / oled_pow(10, len - t - 1)) % 10;
        if(enshow == 0 && t < (len - 1))
        {
            if(temp == 0)
            {
                OLED_ShowChar(x + (size2 / 2) * t, y, ' ', size2);
                continue;
            }
            else 
                enshow = 1; 
        }
        OLED_ShowChar(x + (size2 / 2) * t, y, temp + '0', size2); 
    }
} 
/**
 * @brief 显示字符串
 * @param x 起始列坐标
 * @param y 起始页坐标
 * @param chr 字符串指针
 * @param Char_Size 字体大小
 */
void OLED_ShowString(uint8_t x, uint8_t y, const char *chr, uint8_t Char_Size)
{
    unsigned char j = 0;
    while (chr[j] != '\0')
    {		
        OLED_ShowChar(x, y, chr[j], Char_Size);
        x += 8;
        if(x > 120) { x = 0; y += 2; }
        j++;
    }
}

/**
 * @brief 显示汉字
 * @param x 起始列坐标
 * @param y 起始页坐标
 * @param no 汉字编号 (对应字库中的位置)
 * @note hzk 用取模软件得出的数组
 */
void OLED_ShowCHinese(uint8_t x, uint8_t y, uint8_t no)
{      			    
    uint8_t t, adder = 0;
    OLED_Set_Pos(x, y);	
    for(t = 0; t < 16; t++)
    {
        OLED_WR_DATA(Hzk[2 * no][t]);
        adder += 1;
    }	
    OLED_Set_Pos(x, y + 1);	
    for(t = 0; t < 16; t++)
    {	
        OLED_WR_DATA(Hzk[2 * no + 1][t]);
        adder += 1;
    }					
}
