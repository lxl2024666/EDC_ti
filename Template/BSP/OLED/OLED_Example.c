/**
 * @file OLED_Example.c
 * @brief TI MSPM0G3507平台OLED显示屏使用示例
 * @author 移植自STM32平台
 * @date 2024
 * 
 * 本文件演示如何在TI MSPM0G3507平台上使用0.96寸OLED显示屏
 * 包括文本显示、数字显示、图形显示等功能
 */

#include "oled.h"
#include "ti_msp_dl_config.h"

// 示例汉字字库 (需要使用取模软件生成)
uint8_t chinese_font_example[][16] = {
    // "你" 的字模数据 (示例，需要实际取模)
    {0x04,0x04,0x04,0x84,0x64,0x1C,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x00},
    {0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x00},
    
    // "好" 的字模数据 (示例，需要实际取模)
    {0x10,0x10,0x10,0x10,0x10,0x10,0x10,0xFF,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x00},
    {0x04,0x04,0x04,0x04,0x04,0x04,0x04,0xFF,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x00}
};

/**
 * @brief OLED基本功能测试
 */
void OLED_Basic_Test(void)
{
    // 初始化OLED
    OLED_Init();
    
    // 清屏
    OLED_Clear();
    
    // 显示字符串
    OLED_ShowString(0, 0, "TI MSPM0G3507", 16);
    OLED_ShowString(0, 2, "OLED Test", 16);
    
    // 延时2秒
    DL_Common_delayCycles(64000000);
    
    // 清屏
    OLED_Clear();
    
    // 显示数字
    OLED_ShowString(0, 0, "Number:", 16);
    OLED_ShowNum(60, 0, 12345, 5, 16);
    
    // 显示小字体
    OLED_ShowString(0, 3, "Small Font Test", 12);
    
    // 延时2秒
    DL_Common_delayCycles(64000000);
}

/**
 * @brief OLED数字显示测试
 */
void OLED_Number_Display_Test(void)
{
    uint32_t counter = 0;
    
    OLED_Clear();
    OLED_ShowString(0, 0, "Counter Test:", 16);
    
    while(counter < 100)
    {
        // 显示计数器
        OLED_ShowNum(0, 2, counter, 3, 16);
        
        counter++;
        DL_Common_delayCycles(16000000);  // 500ms延时
    }
}

/**
 * @brief OLED字符串滚动显示测试
 */
void OLED_Scroll_Display_Test(void)
{
    const char* messages[] = {
        "Message 1",
        "Message 2", 
        "Message 3",
        "Message 4",
        "Message 5"
    };
    
    uint8_t msg_count = sizeof(messages) / sizeof(messages[0]);
    uint8_t current_msg = 0;
    
    OLED_Clear();
    OLED_ShowString(0, 0, "Scroll Test:", 16);
    
    while(1)
    {
        // 清除显示区域
        OLED_Clearrow(2);
        OLED_Clearrow(3);
        
        // 显示当前消息
        OLED_ShowString(0, 2, messages[current_msg], 16);
        
        current_msg = (current_msg + 1) % msg_count;
        
        DL_Common_delayCycles(32000000);  // 1秒延时
    }
}

/**
 * @brief OLED多行显示测试
 */
void OLED_Multi_Line_Test(void)
{
    OLED_Clear();
    
    // 在不同行显示不同内容
    OLED_ShowString(0, 0, "Line 0: Hello", 12);
    OLED_ShowString(0, 1, "Line 1: World", 12);
    OLED_ShowString(0, 2, "Line 2: TI", 12);
    OLED_ShowString(0, 3, "Line 3: MSPM0", 12);
    OLED_ShowString(0, 4, "Line 4: Test", 12);
    OLED_ShowString(0, 5, "Line 5: 12345", 12);
    OLED_ShowString(0, 6, "Line 6: OLED", 12);
    OLED_ShowString(0, 7, "Line 7: End", 12);
    
    DL_Common_delayCycles(96000000);  // 3秒延时
}

/**
 * @brief OLED汉字显示测试 (需要配置字库)
 */
void OLED_Chinese_Display_Test(void)
{
    // 设置汉字字库指针
    Hzk = (uint8_t**)chinese_font_example;
    
    OLED_Clear();
    
    // 显示汉字 (需要实际字库支持)
    OLED_ShowString(0, 0, "Chinese Test:", 16);
    // OLED_ShowCHinese(0, 2, 0);  // 显示第一个汉字
    // OLED_ShowCHinese(16, 2, 1); // 显示第二个汉字
    
    DL_Common_delayCycles(64000000);  // 2秒延时
}

/**
 * @brief OLED完整功能演示
 */
void OLED_Full_Demo(void)
{
    // 1. 基本功能测试
    OLED_Basic_Test();
    
    // 2. 数字显示测试
    OLED_Number_Display_Test();
    
    // 3. 多行显示测试
    OLED_Multi_Line_Test();
    
    // 4. 汉字显示测试
    OLED_Chinese_Display_Test();
    
    // 5. 滚动显示测试 (无限循环)
    OLED_Scroll_Display_Test();
}

/**
 * @brief OLED温度显示示例 (模拟数据)
 */
void OLED_Temperature_Display_Example(void)
{
    float temperature = 25.6f;  // 模拟温度
    uint32_t temp_int, temp_dec;
    uint32_t counter = 0;
    
    OLED_Clear();
    OLED_ShowString(0, 0, "Temperature:", 16);
    
    while(1)
    {
        // 模拟温度变化
        temperature = 25.0f + (counter % 100) * 0.1f;
        
        temp_int = (uint32_t)temperature;
        temp_dec = (uint32_t)((temperature - temp_int) * 10);
        
        // 清除之前的温度显示
        OLED_Clearrow(2);
        
        // 显示温度
        OLED_ShowNum(0, 2, temp_int, 2, 16);
        OLED_ShowString(16, 2, ".", 16);
        OLED_ShowNum(24, 2, temp_dec, 1, 16);
        OLED_ShowString(32, 2, "C", 16);
        
        counter++;
        DL_Common_delayCycles(32000000);  // 1秒更新一次
    }
}

/**
 * @brief OLED菜单显示示例
 */
void OLED_Menu_Display_Example(void)
{
    const char* menu_items[] = {
        "1. Settings",
        "2. Display",
        "3. System", 
        "4. About"
    };
    
    uint8_t current_item = 0;
    uint8_t menu_count = sizeof(menu_items) / sizeof(menu_items[0]);
    
    while(1)
    {
        OLED_Clear();
        OLED_ShowString(0, 0, "Main Menu:", 16);
        
        // 显示菜单项
        for(uint8_t i = 0; i < menu_count; i++)
        {
            if(i == current_item)
            {
                OLED_ShowString(0, i + 2, ">", 12);
                OLED_ShowString(8, i + 2, menu_items[i], 12);
            }
            else
            {
                OLED_ShowString(8, i + 2, menu_items[i], 12);
            }
        }
        
        // 模拟按键切换 (实际使用中应该读取按键输入)
        current_item = (current_item + 1) % menu_count;
        
        DL_Common_delayCycles(64000000);  // 2秒切换一次
    }
}
