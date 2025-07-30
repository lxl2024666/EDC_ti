/*
 * Hall_Encoder_Example.c
 * 
 * 霍尔编码器驱动在TI MSPM0G3507上的使用示例
 * 
 * 使用说明：
 * 1. QEI_0使用TIMG8，连接到PA21(PHA)和PA2(PHB)
 * 2. 可以添加更多的QEI编码器
 * 3. 使用TIMG1作为时间基准定时器
 */

#include "Hall_Encoder.h"

// 定时器中断处理函数
void TIMG1_IRQHandler(void)
{
    // 检查是否是零事件中断
    if (DL_TimerG_getPendingInterrupt(TIMG1) & DL_TIMER_INTERRUPT_ZERO_EVENT) 
    {
        // 更新所有编码器速度
        UpdateAllSpeed(TIMG1);
        
        // 清除中断标志
        DL_TimerG_clearInterruptStatus(TIMG1, DL_TIMER_INTERRUPT_ZERO_EVENT);
    }
}

// 初始化函数示例
void Encoder_Example_Init(void)
{
    // 初始化系统配置
    SYSCFG_DL_init();
    
    // 初始化QEI编码器
    // 参数：轮子直径66mm，编码器360PPR
    EncoderInit(QEI_0_INST, TIMG1, 66, 360);
    
    // 如果有左右编码器，可以使用LRInit
    // LRInit(QEI_0_INST, QEI_1_INST, 66, 360, TIMG1);
    
    // 启用中断
    NVIC_EnableIRQ(TIMG1_INT_IRQn);
}

// 使用示例
void Encoder_Example_Usage(void)
{
    // 获取编码器0的速度 (m/s)
    double speed = getSpeed(0);
    
    // 获取编码器0的累计距离 (m)
    double distance = getDis(0);
    
    // 如果使用了LRInit，可以获取左右轮速度
    if (LRFlag) 
    {
        double left_speed = lSpeed();   // 左轮速度
        double right_speed = rSpeed();  // 右轮速度
        double center_speed = cSpeed(); // 中心速度（平均值）
        
        double left_distance = lDis();  // 左轮距离
        double right_distance = rDis(); // 右轮距离
    }
}

/*
 * 配置说明：
 * 
 * 在SysConfig中需要配置：
 * 1. QEI_0 (TIMG8):
 *    - Mode: QEI (Quadrature Encoder Interface)
 *    - PHA Pin: PA21 (PINCM46)
 *    - PHB Pin: PA2 (PINCM7)
 * 
 * 2. TIMG1:
 *    - Mode: Timer
 *    - Period: 根据需要的采样频率设置（如10ms）
 *    - Enable interrupt
 * 
 * 3. 如果需要更多编码器，可以配置：
 *    - QEI_1 (TIMG9)
 *    - QEI_2 (TIMG10) 等
 */
