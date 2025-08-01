#ifndef CONT_SMOTOR_H
#define CONT_SMOTOR_H

#include "SMotor.h"
#include "pid.h"
#include "Init_SMotor.h"

#define YDIS_MOTOR_O 0.0f // 0.0m
#define XDIS_MOTOR_O -0.6f // -0.6m 以发射台为原点，目标物的原点在发射台左方0.6m处
#define ZDIS_MOTOR_O 1.0f // 1.0m

#define C_PI 3.14159265358979323846f // 圆周率常量 

typedef struct{
    float x; // X轴位置
    float y; // Y轴位置
} Coordinate;

typedef struct{
    float yaw; // 方向角
    float pitch; // 俯仰角
} Attitude;

typedef struct {
    float (*t_to_x)(float t); // 时间到X轴位置的转换函数
    float (*t_to_y)(float t); // 时间到Y轴位置的转换函数
    float init_t; // 初始化时间
} TargetPositionFunctions;

void PID_SMotor_Cont(void); // 控制函数

void SetTargetCenter(void); // 设置目标中心位置函数
void SetTargetCircle(void); // 设置目标圆位置函数

void SetLaserPosition(void);

void Compute_excur(void); // 计算偏差函数 

float getDistance();

#endif // CONT_SMOTOR_H