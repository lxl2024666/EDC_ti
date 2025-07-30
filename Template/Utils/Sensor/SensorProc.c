/*
 * SensorProc.c
 *
 *  Created on: 2025-7-24
 *  Author: Qinghan Yang
 *  Description: Source file for sensor processing functions
 */
#include "SensorProc.h"

Coordinate paperCornerC[4];

//以下函数用于处理视觉模块，主要在绘图的时候使用
Coordinate paper_to_camera(Coordinate paper)
{
    paper.x /= PAPERWIDE;
    paper.y /= PAPERHIGHT;
    Coordinate camera;
    camera.x = (paperCornerC[1].x - paperCornerC[0].x) * paper.x 
    + (paperCornerC[3].x - paperCornerC[0].x) * paper.y;
    camera.y = (paperCornerC[1].y - paperCornerC[0].y) * paper.x
    + (paperCornerC[3].y - paperCornerC[0].y) * paper.y;
    return camera;
}

//以下函数用于处理灰度传感器
float Grayscale_Num_To_Theta(int num)
{
    // Convert the sensor number to an angle in degrees
    // The angle is calculated based on the sensor's position
    return RAD_TO_DEG(atan(-(num - (SENSOR_COUNT - 1) / 2.0f) * DisSensor / DisSensorToWheel));
}
 
float thetaGrayscale()
{
    float theta = 0.0f;
    int sum = 0;
    // 计算灰度传感器的偏差而导致的误差值
   for(int i = 0; i < SENSOR_COUNT; i++)
    {
        if(Digital[i] == 0) 
        {
            theta += Grayscale_Num_To_Theta(i);
            sum++;
        }
    }
    return theta / sum;
}

bool Road_detect(int nummin, int nummax)
{
		int sumIRDetect = 0;
		int i = 0;
		while(i < 8){	if(Digital[i]==0) sumIRDetect ++; i++;}
		if(sumIRDetect <= nummax && sumIRDetect >= nummin) 	return 1;
		else return 0;
}
bool half_Detect(){
//三岔路口检测
	return Road_detect(5, 7);
}

bool cross_Roads_Detect(){
//十字路口（丁字路口）检测
	return Road_detect(7, 8);
}