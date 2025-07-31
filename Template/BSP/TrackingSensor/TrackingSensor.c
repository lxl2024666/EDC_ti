#include "TrackingSensor.h"
#include "AllHeader.h"

/**
  * @brief  ��ȡ��·ѭ�������������ݲ���䵽�����С�
  * @param  digitalArray: ָ��һ��8��Ԫ�ص�uint8_t�����ָ�룬���ڴ洢���������ݡ�
  * �����е�ÿ��Ԫ�ؽ��洢��Ӧ��������������״̬��0��1����
  * @retval ��
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