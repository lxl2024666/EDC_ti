#include "mode.h"
#include "AllHeader.h"

extern char CircleNum; // Variable to hold the current circle number
//Test function for the mode system
const int turn_radius = 0.3; // Define the turn radius
const int turn_speed = 0.3; // Define the turn speed
void test_dis(void)//在四个拐角输出距离
{

}

void test_Cordi(void)//在设定位置输出坐标
{

}

void test_Circle(void)//测试圆周运动
{
    runCircle(turn_radius, turn_speed, 360, LEFT); // Run a circle with defined radius, speed, and angle in left direction
}
void proB_1(void)
{
    int cn = SetCircleNum(CircleNum);//未实现
    int isturn = 0; // Variable to track if the robot is turning
    while(1)
    {
        if(half_Detect() && isturn == 0)//注意不要忘记给detect加延时
        {
            isturn = 1; // Set the turning flag
        }
        if(isturn == 1 && !empty_Detect())//注意不要忘记给detect加延时
        {
            isturn = 0; // Reset the turning flag
        }
        if()
        track(0.3);
    }
}

void proB_2_3(void)
{

}

void proH_1(void)
{

}

void proH_2(void)
{

}

int CircleNum(char num)
{
    // Convert the character to an integer
    if (num >= '0' && num <= '9') {
        return num - '0'; // Convert character to integer
    } else {
        sprintf(error_message, "Invalid CircleNum input: %c\n", num);
        error_handler();
        return -1; // Invalid input
    }
}