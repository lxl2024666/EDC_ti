#include "mode.h"
#include "AllHeader.h"

extern char CircleNum; // Variable to hold the current circle number
//Test function for the mode system
const float turn_radius = 0.3; // Define the turn radius
const float turn_speed = 0.3; // Define the turn speed

#define DEBUG // Uncomment to enable debug mode
void test_dis(void)//���ĸ��ս��������
{

}

void test_Cordi(void)//���趨λ���������
{
	YP_SMotor_Init();
    // Implement the functionality for test_Cordi here
	YP_SMotor_SetSpeed(30,10);
}

void test_Circle(void)//����Բ���˶�
{
	while(1)
	{if(!turn_func())
    {
        Break(); // Break the loop if the robot is not turning
        return; // Exit the function
    }
		Delay_ms(10);
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
    int cn = 2;//SetCircleNum(CircleNum);
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
    if(!Init())
    {
		YP_SMotor_SetSpeed(0, 0); // Set the speed of the motors to zero
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
    
    while(1)
    {
		getTrackingSensorData(Digital);
   

		if(half_Detect() && (cn * 4 == edge + 1)) // Check if the half detection condition is met
        {
            Break(); // Break the loop if the condition is met
            return; // Exit the function
        }
        if(!turn_func()) // Check if the robot is turning
        {
            track(0.3); // Call the track function with a linear velocity of 0.3
        }
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
        if(half_Detect() && (4 == edge + 1)) // Check if the half detection condition is met
        {
            Break(); // Break the loop if the condition is met
            return; // Exit the function
        }
        if(!turn_func()) // Check if the robot is turning
        {
            lineWalking_low(); // Call the track function with a linear velocity of 0.3
        }
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
    static int isturn = 0; // Variable to track if the robot is turning
		static uint32_t starttime = 0;
        #ifdef DEBUG
    char debug_message[50];
    sprintf(debug_message, "Edge: %d, isturn: %d", edge, isturn);
    OLED_ShowString(0, 0, debug_message, 8); // Display the edge and turning status on the OLED
        #endif
		if(tick < starttime + 1000 && isturn)
		{
			LSet(90);
			RSet(350);
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
    
    return false; // Return false to indicate initialization failure
}