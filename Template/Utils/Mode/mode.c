#include "mode.h"
#include "AllHeader.h"

extern char CircleNum; // Variable to hold the current circle number
//Test function for the mode system
const float turn_radius = 0.3; // Define the turn radius
const float turn_speed = 0.3; // Define the turn speed

int isturn = 0; // Variable to track if the robot is turning

#define DEBUG // Uncomment to enable debug mode
#define TLCS 80 //转弯时左轮的速度
#define TRCS 360 //转弯时右轮的速度
#define TURN_TIME 800 //转弯时间如果转弯角度不够合适调节这个
void test_dis(void)//编码器测试函数
{
    sInedge = 0; // Reset the sInedge variable
    while(sInedge < 1.0f) // Continue until the distance traveled is less than 1.0
    {
        LSet(100); // Set the left motor speed to 100
        RSet(100);
        UpdateSInedge(); // Update the sInedge variable with the current speed
        Delay_ms(10); // Delay for 10 milliseconds
    }
    Break(); // Stop the motors when the distance is reached
}

void test_Cordi(void)//步进电机测试函数
{
	YP_SMotor_Init();
    // Implement the functionality for test_Cordi here
	YP_SMotor_SetSpeed(30,10);
	while(1)
	{
		YP_SMotor_UpdateState();
		YP_SMotor_SetSpeed(30,10);
		Delay_ms(10);
	}
}

void test_Circle(void)//圆形运动测试函数
{
	while(1)
	{
		LSet(TLCS);
		RSet(TRCS);
	}
}

void test_Connect(void)
{
    char message[50];
    while(1)
    {
        sprintf(message, "LE: %d, RE: %d", Laser_error, Rect_error);
        OLED_ShowString(0, 0, message, 8); // Display the error messages on the OLED
        sprintf(message, "LL0: %d, LL1: %d", Laser_Loc[0], Laser_Loc[1]);
        OLED_ShowString(0, 1, message, 8); // Display the laser location on the OLED
    }
}

void test_track(void)
{
    // Test the track function with a linear velocity of 0.3
    while(1)
    {
		getTrackingSensorData(Digital);
        lineWalking_low();
        if(empty_Detect()) // Check if the empty detection condition is met
        {
            Break(); // Break the loop if the condition is met
            return; // Exit the function
        }
    }
}

void proB_1(void)
{
    int cn = SetCircleNum(CircleNum);
    #ifdef MODE_DEBUG
    char debug_message[50];
    sprintf(debug_message, "CircleNum: %d", cn);
    OLED_ShowString(0, 0, debug_message, 8); // Display the circle number on the OLED
    #endif
    while(1)
    {
		getTrackingSensorData(Digital);
        if(half_Detect() && (cn * 4 == edge))
        {
            Break(); // Break the loop if the condition is met
            return; // Exit the function
        }
        if(!turn_func()) // Check if the robot is turning
        {
            lineWalking_low(); // Call the track function with a linear velocity of 0.3
        }
		Delay_ms(10);
    }
}

void proB_2_3(void)
{
    #ifdef MODE_DEBUG
    OLED_ShowString(0, 0, "ProB2/3", 8); // Display the mode name on the OLED
    #endif
	YP_SMotor_Init();
	while(1){
    if(Init())
    {
        PID_SMotor_Cont(); // Call the PID control function for the motor
        Delay_ms(10); // Delay for 10 milliseconds
    }
	}
}

void proH_1(void)
{
    #ifdef MODE_DEBUG
    OLED_ShowString(0, 0, "ProH1", 8); // Display the mode name on the OLED
    #endif
    int cn = SetCircleNum(CircleNum);
    YP_SMotor_Init();
    while(1)
    {
		getTrackingSensorData(Digital);
        UpdateSInedge(); // Update the sInedge variable with the current speed

		if(half_Detect() && (cn * 4 == edge)) // Check if the half detection condition is met
        {
            Break(); // Break the loop if the condition is met
            return; // Exit the function
        }
        if(!turn_func()) // Check if the robot is turning
        {
            lineWalking_low(); // Call the track function with a linear velocity of 0.3
        }
        SetLaserPosition(); // Set the laser position based on the current mode
        SetTargetCenter(); // Set the target center for the robot
        Compute_excur();
        PID_SMotor_Cont(); // Call the PID control function for the motor
        Delay_ms(10); // Delay for 10 milliseconds   
        // Implement the functionality for ProH1 here
    }
}

void proH_2(void)
{
    #ifdef MODE_DEBUG
    OLED_ShowString(0, 0, "ProH2", 8); // Display the mode name on the OLED
    #endif
    YP_SMotor_Init();
    while(1)
    {
        getTrackingSensorData(Digital);
        UpdateSInedge(); // Update the sInedge variable with the current speed

        if(half_Detect() && (4 == edge)) // Check if the half detection condition is met
        {
            Break(); // Break the loop if the condition is met
            return; // Exit the function
        }
        if(!turn_func()) // Check if the robot is turning
        {
            lineWalking_low(); // Call the track function with a linear velocity of 0.3
        }
        SetLaserPosition(); // Set the laser position for the robot
        SetTargetCircle(); // Set the target circle for the robot
        Compute_excur();
        PID_SMotor_Cont(); // Call the PID control function for the motor
        Delay_ms(10); // Delay for 10 milliseconds   
        // Implement the functionality for ProH1 here
    }

}

int SetCircleNum(char num)
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

bool turn_func(void)
{
    static uint32_t starttime = 0;
		if(tick < starttime + 1000 && isturn)
		{
			LSet(TLCS);
			RSet(TRCS);
			return true;
		}
		isturn = 0;
    if(half_Detect() && isturn == 0)
    {
        #ifdef DEBUG
    char debug_message[50];
    sprintf(debug_message, "Edge: %d, isturn: %d", edge, isturn);
    OLED_ShowString(0, 0, debug_message, 8); // Display the edge and turning status on the OLED
        #endif
        edge ++; // Increment the edge variable
        isturn = 1; // Set the turning flag
				starttime = tick;
			return true;
    }
		return false;
}

bool Init(void)
{
    if(Laser_error == 1)
    {
        YP_SMotor_SetSpeed(-120, 0); // Set the speed of the motors to -120
        return false; // Return false to indicate initialization failure
    }
    return true; // Return true to indicate successful initialization
}