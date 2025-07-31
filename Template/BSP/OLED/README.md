# OLED显示驱动 - TI MSPM0G3507移植版

## 概述
本驱动程序从STM32平台移植到TI MSPM0G3507平台，支持0.96寸128x64 OLED显示屏(SSD1306控制器)，通过I2C接口进行通信。提供完整的文本显示、数字显示、图形显示和汉字显示功能。

## 硬件支持
- **显示屏**: 0.96寸 128x64 OLED (SSD1306)
- **接口**: I2C (400kHz推荐)
- **电压**: 3.3V
- **分辨率**: 128x64像素
- **显示色彩**: 单色 (蓝色/白色/黄蓝双色)

## 功能特性
- **基本显示**: 清屏、设置位置、开关显示
- **文本显示**: 支持6x8和8x16两种字体
- **数字显示**: 整数显示，支持前导零处理
- **字符串显示**: 支持自动换行
- **汉字显示**: 支持16x16汉字字库 (需要自定义字库)
- **图形功能**: 全屏点亮、指定区域清除

## 硬件连接

### 引脚连接
```
OLED模块    MSPM0G3507    说明
VCC         3.3V          电源正极
GND         GND           电源负极  
SCL         I2C_SCL       I2C时钟线
SDA         I2C_SDA       I2C数据线
```

### 推荐引脚分配
```
功能    引脚      SysConfig配置
SCL     PA28      I2C_0 SCL
SDA     PA31      I2C_0 SDA
```

## SysConfig配置

### I2C配置步骤
1. **添加I2C模块**:
   - 在SysConfig中点击 "+" 按钮
   - 选择 "COMM" -> "I2C"
   - 重命名为 "I2C_0"

2. **I2C基本配置**:
   ```
   Controller Mode: Controller
   Target Address: 0x3C (7-bit) 或 0x78 (8-bit)
   Clock Source: BUSCLK
   Controller Clock Frequency: 400000 (400kHz)
   ```

3. **引脚配置**:
   ```
   SCL Pin: 根据板子选择 (建议PA28)
   SDA Pin: 根据板子选择 (建议PA31)
   Enable Pull-up: ✓ (如果板子没有外部上拉电阻)
   ```

4. **生成代码**:
   - 点击 "Generate" 生成配置代码
   - 确保生成 `ti_msp_dl_config.h`

## API接口

### 初始化函数

#### `OLED_Init()`
```c
void OLED_Init(void);
```
初始化OLED显示屏。

**使用说明:**
- 必须在使用其他函数前调用
- 包含200ms延时等待显示屏稳定
- 自动发送初始化命令序列

### 基本控制函数

#### `OLED_Clear()`
```c
void OLED_Clear(void);
```
清除整个显示屏。

#### `OLED_Clearrow()`
```c
void OLED_Clearrow(uint8_t i);
```
清除指定行。

**参数:**
- `i`: 页地址 (0-7)

#### `OLED_Display_On()` / `OLED_Display_Off()`
```c
void OLED_Display_On(void);
void OLED_Display_Off(void);
```
开启/关闭显示。

#### `OLED_Set_Pos()`
```c
void OLED_Set_Pos(uint8_t x, uint8_t y);
```
设置显示位置。

**参数:**
- `x`: 列坐标 (0-127)
- `y`: 页坐标 (0-7)

### 文本显示函数

#### `OLED_ShowChar()`
```c
void OLED_ShowChar(uint8_t x, uint8_t y, uint8_t chr, uint8_t Char_Size);
```
显示单个字符。

**参数:**
- `x`: 列坐标 (0-127)
- `y`: 页坐标 (0-7)
- `chr`: 要显示的字符
- `Char_Size`: 字体大小 (16或12)

#### `OLED_ShowString()`
```c
void OLED_ShowString(uint8_t x, uint8_t y, const char *chr, uint8_t Char_Size);
```
显示字符串。

**参数:**
- `x`: 起始列坐标
- `y`: 起始页坐标
- `chr`: 字符串指针
- `Char_Size`: 字体大小

#### `OLED_ShowNum()`
```c
void OLED_ShowNum(uint8_t x, uint8_t y, unsigned int num, uint8_t len, uint8_t size);
```
显示数字。

**参数:**
- `x`: 起始列坐标
- `y`: 起始页坐标
- `num`: 要显示的数字 (0-4294967295)
- `len`: 显示位数
- `size`: 字体大小

### 汉字显示函数

#### `OLED_ShowCHinese()`
```c
void OLED_ShowCHinese(uint8_t x, uint8_t y, uint8_t no);
```
显示汉字。

**参数:**
- `x`: 起始列坐标
- `y`: 起始页坐标
- `no`: 汉字编号 (对应字库位置)

**注意:** 需要设置全局变量 `Hzk` 指向汉字字库

### 底层通信函数

#### `OLED_WR_CMD()` / `OLED_WR_DATA()`
```c
void OLED_WR_CMD(uint8_t cmd);
void OLED_WR_DATA(uint8_t data);
```
发送命令/数据到OLED。(通常不需要直接调用)

## 使用示例

### 基本使用
```c
#include "oled.h"

void basic_oled_example(void) {
    // 初始化OLED
    OLED_Init();
    
    // 清屏
    OLED_Clear();
    
    // 显示文本
    OLED_ShowString(0, 0, "Hello TI!", 16);
    OLED_ShowString(0, 2, "MSPM0G3507", 16);
    
    // 显示数字
    OLED_ShowNum(0, 4, 12345, 5, 16);
    
    // 保持显示
    while(1) {
        // 主循环
    }
}
```

### 动态数据显示
```c
void dynamic_display_example(void) {
    uint32_t counter = 0;
    
    OLED_Init();
    OLED_Clear();
    OLED_ShowString(0, 0, "Counter:", 16);
    
    while(1) {
        // 清除之前的数字
        OLED_Clearrow(2);
        
        // 显示新数字
        OLED_ShowNum(0, 2, counter, 5, 16);
        
        counter++;
        DL_Common_delayCycles(32000000);  // 1秒延时
    }
}
```

### 温度显示示例
```c
void temperature_display_example(void) {
    float temp = 25.6f;
    uint32_t temp_int, temp_dec;
    
    OLED_Init();
    OLED_Clear();
    OLED_ShowString(0, 0, "Temperature:", 16);
    
    while(1) {
        temp_int = (uint32_t)temp;
        temp_dec = (uint32_t)((temp - temp_int) * 10);
        
        OLED_Clearrow(2);
        OLED_ShowNum(0, 2, temp_int, 2, 16);
        OLED_ShowString(16, 2, ".", 16);
        OLED_ShowNum(24, 2, temp_dec, 1, 16);
        OLED_ShowString(32, 2, "C", 16);
        
        DL_Common_delayCycles(32000000);
    }
}
```

### 菜单显示示例
```c
void menu_display_example(void) {
    const char* menu[] = {"Settings", "Display", "System", "About"};
    uint8_t selected = 0;
    
    OLED_Init();
    
    while(1) {
        OLED_Clear();
        OLED_ShowString(0, 0, "Menu:", 16);
        
        for(uint8_t i = 0; i < 4; i++) {
            if(i == selected) {
                OLED_ShowString(0, i + 2, ">", 12);
            }
            OLED_ShowString(8, i + 2, menu[i], 12);
        }
        
        // 模拟按键切换
        selected = (selected + 1) % 4;
        DL_Common_delayCycles(64000000);
    }
}
```

## 汉字显示配置

### 字库准备
1. **使用取模软件**: 推荐使用PCtoLCD或字模生成器
2. **设置参数**:
   ```
   字体大小: 16x16像素
   取模方式: 逐行式
   字节倒序: 否
   ```

3. **生成字库数组**:
   ```c
   uint8_t chinese_font[][16] = {
       // "你" 的字模数据
       {0x04,0x04,0x04,0x84,0x64,0x1C,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x00},
       {0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x00},
       // 更多汉字...
   };
   ```

4. **使用汉字显示**:
   ```c
   Hzk = (uint8_t**)chinese_font;  // 设置字库指针
   OLED_ShowCHinese(0, 0, 0);      // 显示第一个汉字
   ```

## 显示坐标系统

### 坐标说明
- **列坐标 (X)**: 0-127，对应128个像素列
- **页坐标 (Y)**: 0-7，每页8个像素行
- **像素坐标**: 实际显示为128x64像素

### 页地址映射
```
页0: 像素行 0-7
页1: 像素行 8-15
页2: 像素行 16-23
页3: 像素行 24-31
页4: 像素行 32-39
页5: 像素行 40-47
页6: 像素行 48-55
页7: 像素行 56-63
```

### 字体尺寸
- **6x8字体**: 宽6像素，高8像素 (1页)
- **8x16字体**: 宽8像素，高16像素 (2页)
- **16x16汉字**: 宽16像素，高16像素 (2页)

## 性能参数
| 参数 | 数值 | 说明 |
|------|------|------|
| I2C时钟 | 400kHz | 推荐频率 |
| 初始化时间 | ~200ms | 包含等待时间 |
| 刷新速度 | ~30fps | 全屏刷新 |
| 字符显示 | ~100us | 单个字符 |
| 通信地址 | 0x78 | 8位地址格式 |

## 故障排除

### 常见问题

1. **显示屏无显示**
   - 检查电源连接 (3.3V)
   - 确认I2C接线正确
   - 验证I2C地址 (0x78或0x3C)
   - 检查SysConfig I2C配置

2. **显示内容错乱**
   - 确认I2C时钟频率不要过高
   - 检查I2C上拉电阻 (4.7kΩ推荐)
   - 验证初始化命令序列

3. **部分字符不显示**
   - 检查字库数据是否正确
   - 确认坐标设置是否超出范围
   - 验证字体大小参数

4. **汉字显示异常**
   - 确认字库指针 `Hzk` 已正确设置
   - 检查取模软件参数设置
   - 验证字库数组格式

### 调试方法

1. **I2C通信测试**:
   ```c
   // 发送简单命令测试通信
   OLED_WR_CMD(0xAE);  // 关闭显示
   OLED_WR_CMD(0xAF);  // 开启显示
   ```

2. **全屏测试**:
   ```c
   OLED_On();  // 全屏点亮
   ```

3. **逐行测试**:
   ```c
   for(uint8_t i = 0; i < 8; i++) {
       OLED_Clear();
       OLED_ShowString(0, i, "Test Line", 16);
       DL_Common_delayCycles(32000000);
   }
   ```

## 移植说明

从STM32平台移植的主要更改：
- `#include "i2c.h"` -> `#include "ti_msp_dl_config.h"`
- `HAL_I2C_Mem_Write()` -> `DL_I2C_startControllerTransfer()` + `DL_I2C_fillControllerTXFIFO()`
- `HAL_Delay()` -> `DL_Common_delayCycles()`
- `&hi2c2` -> `OLED_I2C_INST`
- 增加了I2C传输状态等待逻辑

## 扩展功能建议

1. **图形绘制**: 添加点、线、矩形绘制功能
2. **动画效果**: 实现滚动、闪烁等动画效果  
3. **多字体支持**: 添加更多字体尺寸选择
4. **缓冲区模式**: 实现显示缓冲区以提高刷新效率
5. **进度条**: 添加进度条显示功能

## 文件结构
```
BSP/OLED/
├── oled.h              # 头文件定义
├── oled.c              # 驱动实现
├── oledfont.h          # 字体数据
├── OLED_Example.c      # 使用示例
└── README.md           # 本说明文档
```
