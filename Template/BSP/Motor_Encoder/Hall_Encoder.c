#include "Hall_Encoder.h"

EncoderSpeed encoders[MAXENCODERNUM]; // Array to store encoder data
int numEncoders = 0; // Number of encoders initialized
int LRFlag = 0; // Flag to indicate if left and right encoders are initialized

void EncoderInit(GPTIMER_Regs *Timer, GPTIMER_Regs *realTimer,
	int wheelLength, int ppr)
	//set global variables for encoders
{
	if (numEncoders >= MAXENCODERNUM)
	{
		return; // Maximum number of encoders reached
	}

	encoders[numEncoders].timer = Timer;
	encoders[numEncoders].realTimer = realTimer;
	
	// 初始化QEI模式
	DL_TimerG_setQEIConfig(Timer, DL_TIMER_QEI_MODE_QUADRATURE,
		DL_TIMER_QEI_DIRECTION_COUNTUP, DL_TIMER_QEI_INPUT_INVERTED_DISABLE);
	DL_TimerG_enableQEI(Timer);
	
	// 启动定时器
	DL_TimerG_startCounter(Timer);
	
	// 清除并启动实时定时器中断
	DL_TimerG_clearInterruptStatus(realTimer, DL_TIMER_INTERRUPT_ZERO_EVENT);
	DL_TimerG_enableInterrupt(realTimer, DL_TIMER_INTERRUPT_ZERO_EVENT);
	DL_TimerG_startCounter(realTimer);
	
	encoders[numEncoders].reloadFre = ReloadTime(realTimer);
	encoders[numEncoders].speed = 0; // Initialize speed to 0
	encoders[numEncoders].dis = 0.0; // Initialize distance to 0
	DL_TimerG_setCounterValue(Timer, 0);
  encoders[numEncoders].prev_cnt = DL_TimerG_getCounterValue(Timer); // ��ʼ�� prev_cnt


	EncoderParamInit(&encoders[numEncoders].param, wheelLength, ppr);
	numEncoders++;
	return;
}

void EncoderParamInit(EncoderParam *param, int wheelLength, int ppr)
	//set the parameter of the encoder
{
	if (param == NULL)
	{
		return; // Parameter pointer is NULL
	}
	param->wheelLength = wheelLength; // Set wheel length in mm
	param->ppr = ppr; // Set Pulses Per Revolution
}

void LRInit(GPTIMER_Regs *LTimer, GPTIMER_Regs *RTimer,
			int wheelLength, int ppr, // The last two parameters are for encoder parameters
			GPTIMER_Regs *realTimer)
	//set global variables for left and right encoders
{
	EncoderInit(LTimer, realTimer, wheelLength, ppr);
	EncoderInit(RTimer, realTimer, wheelLength, ppr);
	
	LRFlag = 1; // Set flag to indicate left and right encoders are initialized
}

void UpdateSpeed(int i, GPTIMER_Regs *reload_tim)
	//get the speed of the motor
	//E is the encoder speed struct, reload_tim is the timer used to measure real time
{	
	if (encoders[i].timer == NULL || encoders[i].realTimer == NULL)
	{
		return; // Timer not initialized
	}
	if(reload_tim == encoders[i].realTimer)
	{
		 int16_t current_cnt = DL_TimerG_getCounterValue(encoders[i].timer); // ��ȡ��ǰ����ֵ
        // ��������������Ǳ�ڵ� 16 λ��ʱ�����/����
        // ����ʹ�� 16 λ��ʱ�����Ҽ���ֵ�� int16_t ��Χ��
     encoders[i].speed = (int16_t)(current_cnt - encoders[i].prev_cnt);

     encoders[i].prev_cnt = current_cnt; // ����ǰһ������ֵ�����´ε���ʹ��
     encoders[i].dis += StoDis(encoders[i]);
	}
}

void UpdateAllSpeed(GPTIMER_Regs *reload_tim)
	//update all encoders' speed
{
	for (int i = 0; i < numEncoders; i++)
	{
		UpdateSpeed(i, reload_tim);
	}
}

double StoDis(EncoderSpeed e)
{
	return e.speed * e.param.wheelLength * 1e-3 * PI 
	/ (e.param.ppr * 2);
	// Compute the distance traveled by the wheel
}

//Get wheels' speed with the unit of m/s
//'+' means forwards and '-' means backwards.
//When you are using the code, please connect PE9 to E1A, PE11 to E1B, 
double getSpeed(int index)
{
	return encoders[index].speed * 
		encoders[index].param.wheelLength * 1e-3 * PI * 
		encoders[index].reloadFre / (encoders[index].param.ppr * 2);
		//4.394215799e-3;
		// Left number is computed by (length of the circle) * (frequence of the clock / (leftSpeed add number for every single circle
		// which is (6.6e-2 * pi * (240e6 / ((65535 + 1) * (239 + 1)) / (360 * 2))
}

double getDis(int index)
{
	return encoders[index].dis; // Return the distance traveled by the wheel
	// The distance is already updated in UpdateSpeed function
}

//Functions below are speciafic for left and right encoders
double cSpeed()
{
	if(LRFlag == 0)
	{
		return 0.0; // No left and right encoders initialized
	}
	return (getSpeed(0) + getSpeed(1)) / 2.0; // Average speed of left and right encoders
}
double lSpeed()
{
	if(LRFlag == 0)
	{
		return 0.0; // No left encoder initialized
	}
	return getSpeed(0); // Speed of left encoder
}
double rSpeed()
{
	if(LRFlag == 0)
	{
		return 0.0; // No right encoder initialized
	}
	return getSpeed(1); // Speed of right encoder
}

double lDis()
{
	if(LRFlag == 0)
	{
		return 0.0; // No left encoder initialized
	}
	return getDis(0); // Distance traveled by left wheel
}
double rDis()
{
	if(LRFlag == 0)
	{
		return 0.0; // No right encoder initialized
	}
	return getDis(1); // Distance traveled by right wheel
}

uint32_t ReloadTime(GPTIMER_Regs* tim)
{
	// 获取系统时钟频率 (32MHz)
	uint32_t system_clk = CPUCLK_FREQ;
	
	// 获取定时器的预分频值和重载值
	uint32_t psc = DL_TimerG_getPrescaler(tim);
	uint32_t arr = DL_TimerG_getLoadValue(tim);
	
	// 计算定时器频率
	return system_clk / ((psc + 1) * (arr + 1));
}
