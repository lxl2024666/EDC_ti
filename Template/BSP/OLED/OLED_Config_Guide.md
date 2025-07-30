# OLED显示驱动配置指南 - TI MSPM0G3507平台

## SysConfig配置详细步骤

### 1. 创建I2C配置
1. 打开SysConfig工具
2. 点击左侧 "+" 按钮
3. 选择 "COMM" -> "I2C"
4. 在右侧重命名为 "I2C_0"

### 2. I2C基本参数配置
```
Basic Configuration:
├─ Mode: Controller
├─ Controller Target Address: 0x3C (7-bit address)
├─ Controller Clock Source: BUSCLK  
├─ Controller Clock Frequency: 400000 Hz
└─ Enable Controller Clock Stretching: ✓
```

### 3. I2C高级配置 (可选)
```
Advanced Configuration:
├─ Controller TX FIFO Threshold: BYTES_1
├─ Controller RX FIFO Threshold: BYTES_1  
└─ Controller Arbitration Lost Enable: ✓
```

### 4. 引脚配置
```
Pin Configuration:
├─ SCL Pin: PA28 (可根据实际板子调整)
├─ SDA Pin: PA31 (可根据实际板子调整)
└─ Pin Configuration:
    ├─ Pull-up: Enable (如果没有外部上拉电阻)
    ├─ Open Drain: Enable
    └─ Drive Strength: High
```

### 5. 中断配置 (可选)
```
Interrupt Configuration:
├─ Enable Controller Interrupt: ✓ (如果需要中断方式)
├─ Controller Interrupt Priority: Default
└─ Enabled Interrupts:
    ├─ Transaction Done
    ├─ Transmit FIFO Empty
    └─ NACK
```

## 硬件连接指南

### 标准连接方式
```
OLED SSD1306     MSPM0G3507      说明
VCC/VDD         3.3V            电源正极 (重要：必须是3.3V，不能接5V)
GND             GND             电源负极
SCL             PA28            I2C时钟线 (可配置其他引脚)
SDA             PA31            I2C数据线 (可配置其他引脚)
```

### 上拉电阻
- **内置上拉**: 如果OLED模块没有板载上拉电阻，在SysConfig中启用内置上拉
- **外部上拉**: 推荐使用4.7kΩ电阻连接到3.3V
- **上拉电阻位置**: SCL和SDA线都需要上拉电阻

### 电源注意事项
1. **电压要求**: OLED模块通常工作在3.3V，不要接5V
2. **电流消耗**: 典型20-30mA，最大可达50mA
3. **电源滤波**: 建议在VCC引脚附近加100nF陶瓷电容

## 常用引脚配置表

### MSPM0G3507 LaunchPad引脚
| 功能 | 推荐引脚 | 备选引脚1 | 备选引脚2 | 备选引脚3 |
|------|----------|-----------|-----------|-----------|
| SCL  | PA28     | PA24      | PA14      | PA8       |
| SDA  | PA31     | PA25      | PA15      | PA9       |

### 自定义板引脚选择原则
1. **避免冲突**: 不要与其他外设引脚冲突
2. **布线方便**: 选择物理位置相近的引脚
3. **功能支持**: 确保引脚支持I2C功能

## 代码配置

### 1. 包含头文件
```c
#include "oled.h"
#include "ti_msp_dl_config.h"
```

### 2. 配置检查
确保在 `oled.h` 中的配置与SysConfig一致：
```c
#define OLED_I2C_INST               I2C_0_INST    // 与SysConfig中的名称一致
#define OLED_I2C_ADDR               0x78          // 8位地址格式
```

### 3. 初始化代码
```c
void system_init(void) {
    // SysConfig生成的初始化
    SYSCFG_DL_init();
    
    // OLED初始化
    OLED_Init();
}
```

## I2C地址配置

### 地址格式说明
- **7位地址**: 0x3C (SysConfig中使用)
- **8位地址**: 0x78 (代码中使用，包含R/W位)
- **转换关系**: 8位地址 = 7位地址 << 1

### 常见OLED I2C地址
| 显示屏型号 | 7位地址 | 8位地址 | 说明 |
|------------|---------|---------|------|
| SSD1306    | 0x3C    | 0x78    | 最常见 |
| SSD1306    | 0x3D    | 0x7A    | 地址可变 |
| SH1106     | 0x3C    | 0x78    | 兼容SSD1306 |

### 地址检测方法
```c
// I2C地址扫描代码 (调试用)
void scan_i2c_devices(void) {
    for(uint8_t addr = 0x08; addr < 0x78; addr++) {
        DL_I2C_startControllerTransfer(I2C_0_INST, addr << 1, 
                                       DL_I2C_CONTROLLER_DIRECTION_TX, 1);
        
        if(!(DL_I2C_getControllerStatus(I2C_0_INST) & DL_I2C_CONTROLLER_STATUS_ERROR)) {
            // 找到设备，地址为 addr
        }
    }
}
```

## 性能优化配置

### I2C速度配置
```
标准模式:  100kHz  - 最稳定，兼容性最好
快速模式:  400kHz  - 推荐设置，性能与稳定性平衡  
高速模式:  1MHz    - 最快，可能需要调试
```

### SysConfig性能设置
```
Controller Clock Frequency: 400000  (400kHz推荐)
FIFO Threshold: 1 Byte             (减少中断频率)
DMA Enable: 可选                    (大数据量传输时启用)
```

## 调试配置

### 1. 添加调试宏
```c
// 在oled.h中添加
#define OLED_DEBUG_ENABLE    1

#if OLED_DEBUG_ENABLE
#define OLED_DEBUG(x)   printf x
#else  
#define OLED_DEBUG(x)
#endif
```

### 2. I2C状态检查
```c
void check_i2c_status(void) {
    uint32_t status = DL_I2C_getControllerStatus(OLED_I2C_INST);
    
    if(status & DL_I2C_CONTROLLER_STATUS_ERROR) {
        OLED_DEBUG(("I2C Error occurred\n"));
    }
    
    if(status & DL_I2C_CONTROLLER_STATUS_BUSY_BUS) {
        OLED_DEBUG(("I2C Bus is busy\n"));
    }
}
```

### 3. 通信测试函数
```c
bool test_oled_communication(void) {
    // 发送显示开关命令测试通信
    OLED_WR_CMD(0xAE);  // 关闭显示
    OLED_WR_CMD(0xAF);  // 开启显示
    
    // 检查是否有错误
    uint32_t status = DL_I2C_getControllerStatus(OLED_I2C_INST);
    return !(status & DL_I2C_CONTROLLER_STATUS_ERROR);
}
```

## 常见配置错误

### 1. 地址配置错误
**错误现象**: OLED无显示，I2C通信失败
**解决方法**: 
- 确认SysConfig中使用7位地址 (0x3C)
- 确认代码中使用8位地址 (0x78)

### 2. 时钟频率过高
**错误现象**: 显示内容错乱，通信不稳定
**解决方法**: 
- 降低I2C时钟到400kHz或更低
- 检查上拉电阻阻值 (推荐4.7kΩ)

### 3. 引脚配置冲突
**错误现象**: I2C初始化失败，编译错误
**解决方法**: 
- 检查引脚是否被其他模块占用
- 使用SysConfig检查引脚冲突

### 4. 上拉电阻问题
**错误现象**: I2C时序不正确，通信失败
**解决方法**: 
- 启用内置上拉或添加外部上拉电阻
- 检查上拉电阻阻值 (2.2kΩ-10kΩ)

## 测试程序

### 1. 基本通信测试
```c
void test_basic_communication(void) {
    OLED_Init();
    
    if(test_oled_communication()) {
        printf("OLED communication OK\n");
    } else {
        printf("OLED communication failed\n");
    }
}
```

### 2. 显示功能测试
```c
void test_display_functions(void) {
    OLED_Init();
    OLED_Clear();
    
    // 测试字符显示
    OLED_ShowString(0, 0, "Test", 16);
    
    // 测试数字显示
    OLED_ShowNum(0, 2, 12345, 5, 16);
    
    // 测试清屏
    DL_Common_delayCycles(64000000);  // 2秒
    OLED_Clear();
}
```

### 3. 性能测试
```c
void test_display_performance(void) {
    uint32_t start_time, end_time;
    
    start_time = DL_Common_getTick();
    
    // 全屏刷新测试
    for(int i = 0; i < 100; i++) {
        OLED_Clear();
        OLED_ShowString(0, 0, "Performance Test", 16);
    }
    
    end_time = DL_Common_getTick();
    
    printf("100 screen updates took %d ms\n", end_time - start_time);
}
```

## 配置文件模板

### sysconfig项目文件 (.syscfg)
```javascript
// I2C配置模板
const I2C = scripting.addModule("/ti/driverlib/I2C", {}, false);
I2C.$name = "I2C_0";
I2C.basicControllerStandardBusSpeed = "Fast";
I2C.basicTargetAddress = 0x3C;
I2C.basicControllerClkFreq = 400000;
I2C.peripheral.$assign = "I2C0";
I2C.peripheral.sdaPin.$assign = "PA31";
I2C.peripheral.sclPin.$assign = "PA28";
```

### 配置验证清单
- [ ] SysConfig中I2C模块已添加并命名为"I2C_0"
- [ ] I2C地址设置为0x3C (7位)
- [ ] I2C时钟频率设置为400kHz
- [ ] SCL/SDA引脚已正确配置
- [ ] 上拉电阻已启用或外接
- [ ] 电源连接正确 (3.3V)
- [ ] 代码中包含ti_msp_dl_config.h
- [ ] OLED_I2C_INST宏定义正确
- [ ] 初始化代码调用SYSCFG_DL_init()和OLED_Init()
