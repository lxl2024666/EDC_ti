/**
 * @file      OLED.h
 * @brief     SSD1306 OLED显示屏驱动库的头文件 (软件I2C)
 * @details   本驱动使用软件模拟I2C协议与OLED通信。它提供了OLED初始化、
 * 显示字符、数字、字符串和位图等功能。
 * @author    Jianing Wang
 * @version   1.1
 * @date      2025-07-31
 * @note      - 本驱动依赖于一个提供微秒级延时函数 `Delay_us()` 的延时库。
 * - 使用前，请确保已在SysConfig中配置了SCL和SDA引脚，并在此文件中
 * 正确定义了`OLED_GPIO_PORT`、`OLED_SCL_PIN`和`OLED_SDA_PIN`。
 */

#ifndef __OLED_H__
#define __OLED_H__

#include "ti_msp_dl_config.h" // 引入TI MSPM0的底层库
#include <stdint.h>          // 引入标准整数类型

//==================================================================================
// 用户配置区 (User Configuration)
//==================================================================================

// 定义OLED连接的GPIO端口
// 例如：如果您将SCL和SDA都连接到GPIOA，这里就使用GPIOA
#define OLED_GPIO_PORT      (GPIOA)

// 定义OLED的SCL和SDA引脚 (请与SysConfig中的命名和配置保持一致)
#define OLED_SCL_PIN        (GPIO_OLED_SCL_PIN)
#define OLED_SDA_PIN        (GPIO_OLED_SDA_PIN)


//==================================================================================
// 内部宏定义 (Internal Macros)
//==================================================================================

#define OLED_CMD            (0) // 写命令模式
#define OLED_DATA           (1) // 写数据模式

//----------------------------------------------------------------------------------
// OLED SSD1306 I2C 时钟 SCL 引脚操作
#define OLED_SCL_Set()      (DL_GPIO_setPins(OLED_GPIO_PORT, OLED_SCL_PIN))
#define OLED_SCL_Clr()      (DL_GPIO_clearPins(OLED_GPIO_PORT, OLED_SCL_PIN))

//----------------------------------------------------------------------------------
// OLED SSD1306 I2C 数据 SDA 引脚操作
#define OLED_SDA_Set()      (DL_GPIO_setPins(OLED_GPIO_PORT, OLED_SDA_PIN))
#define OLED_SDA_Clr()      (DL_GPIO_clearPins(OLED_GPIO_PORT, OLED_SDA_PIN))
#define OLED_SDA_Read()     (DL_GPIO_readPins(OLED_GPIO_PORT, OLED_SDA_PIN))


//==================================================================================
// 函数原型声明 (Function Prototypes)
//==================================================================================

/**
 * @brief  OLED驱动初始化
 * @details 初始化GPIO引脚并发送一系列指令来配置OLED模块。
 * @param  None
 * @retval None
 */
void OLED_Init(void);

/**
 * @brief  清空整个OLED屏幕
 * @details 将显存的所有位都设置为0，屏幕将变黑。
 * @param  None
 * @retval None
 */
void OLED_Clear(void);

/**
 * @brief  设置显示颜色反转
 * @param  i 0: 正常显示, 1: 颜色反转 (黑底白字变白底黑字)
 * @retval None
 */
void OLED_ColorTurn(uint8_t i);

/**
 * @brief  设置屏幕内容旋转180度
 * @param  i 0: 正常显示, 1: 旋转180度
 * @retval None
 */
void OLED_DisplayTurn(uint8_t i);

/**
 * @brief  打开OLED显示
 * @param  None
 * @retval None
 */
void OLED_Display_On(void);

/**
 * @brief  关闭OLED显示 (进入休眠)
 * @param  None
 * @retval None
 */
void OLED_Display_Off(void);

/**
 * @brief  在指定位置显示一个ASCII字符
 * @param  x      起始列坐标 (0-127)
 * @param  y      起始页坐标 (0-7 for 16-size font, 0-63 for direct addressing)
 * @param  chr    要显示的ASCII字符
 * @param  sizey  字体大小 (支持 8 和 16)
 * @retval None
 */
void OLED_ShowChar(uint8_t x, uint8_t y, uint8_t chr, uint8_t sizey);

/**
 * @brief  在指定位置显示字符串
 * @param  x      起始列坐标 (0-127)
 * @param  y      起始页坐标 (0-7)
 * @param  chr    指向字符串的指针
 * @param  sizey  字体大小 (支持 8 和 16)
 * @retval None
 */
void OLED_ShowString(uint8_t x, uint8_t y, uint8_t *chr, uint8_t sizey);

/**
 * @brief  显示一个无符号十进制数字
 * @param  x      起始列坐标 (0-127)
 * @param  y      起始页坐标 (0-7)
 * @param  num    要显示的数字 (0-4294967295)
 * @param  len    要显示的数字长度
 * @param  sizey  字体大小
 * @retval None
 */
void OLED_ShowNum(uint8_t x, uint8_t y, uint32_t num, uint8_t len, uint8_t sizey);

/**
 * @brief  在指定位置显示一个16x16的汉字
 * @param  x      起始列坐标 (0-127)
 * @param  y      起始页坐标 (0-7)
 * @param  no     要显示的汉字在字库 `Hzk` 中的索引号
 * @retval None
 */
void OLED_ShowChinese(uint8_t x, uint8_t y, uint8_t no);

/**
 * @brief  显示一幅位图
 * @param  x      图片左上角起始列坐标 (0-127)
 * @param  y      图片左上角起始页坐标 (0-7)
 * @param  sizex  图片的宽度（像素）
 * @param  sizey  图片的高度（像素）
 * @param  BMP    指向位图数据数组的指针
 * @retval None
 */
void OLED_DrawBMP(uint8_t x, uint8_t y, uint8_t sizex, uint8_t sizey, uint8_t BMP[]);

#endif /* __OLED_H__ */