#include "TrackingSensor.h"
#include "AllHeader.h"

/**
  * @brief  读取八路循迹传感器的数据并填充到数组中。
  * @param  digitalArray: 指向一个8个元素的uint8_t数组的指针，用于存储传感器数据。
  * 数组中的每个元素将存储对应传感器的数字量状态（0或1）。
  * @retval 无
  */
void getTrackingSensorData(uint8_t digitalArray[8])
{
    digitalArray[0] = DL_GPIO_readPins(Tracking_Tracking_1_PORT, Tracking_Tracking_1_PIN);
    digitalArray[1] = DL_GPIO_readPins(Tracking_Tracking_2_PORT, Tracking_Tracking_2_PIN);
    digitalArray[2] = DL_GPIO_readPins(Tracking_Tracking_3_PORT, Tracking_Tracking_3_PIN);
    digitalArray[3] = DL_GPIO_readPins(Tracking_Tracking_4_PORT, Tracking_Tracking_4_PIN);
    digitalArray[4] = DL_GPIO_readPins(Tracking_Tracking_5_PORT, Tracking_Tracking_5_PIN);
    digitalArray[5] = DL_GPIO_readPins(Tracking_Tracking_6_PORT, Tracking_Tracking_6_PIN);
    digitalArray[6] = DL_GPIO_readPins(Tracking_Tracking_7_PORT, Tracking_Tracking_7_PIN);
    digitalArray[7] = DL_GPIO_readPins(Tracking_Tracking_8_PORT, Tracking_Tracking_8_PIN);
}