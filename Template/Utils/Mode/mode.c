#include "mode.h"
#include "AllHeader.h"

extern char CircleNum; // Variable to hold the current circle number
//Test function for the mode system


int isturn = 0; // Variable to track if the robot is turning
bool turning = false;

void test_dis(void)//���������Ժ���
{
    while(1)
		{
			LSet(-200);
			RSet(200);
		}
		
}

void test_Cordi(void)//����������Ժ���
{
	YP_SMotor_Init();
    // Implement the functionality for test_Cordi here
	YP_SMotor_SetSpeed(30,10);
	while(1)
	{
		YP_SMotor_UpdateState();
		YP_SMotor_SetSpeed(90,10);
		Delay_ms(10);
	}
}

void test_Circle(void)//Բ���˶����Ժ���
{
	while(1)
	{
		UpdateSInedge();
		getTrackingSensorData(Digital);
		if(!turn_func())
		{
			Break();
			break;
		}
		Delay_ms(10);
		
	}
}

void test_Connect(void)
{
    char message[50];
    while(1)
    {
		Coordinate cor = {0.0f, 0.0f};
        Coordinate paper = {0.1, 0.1}; // Get the center coordinates of the paper
        cor = paper_to_camera(paper);
        sprintf(message, "Camera: (%.2f, %.2f)", cor.x, cor.y); // Format the message
        OLED_ShowString(0, 0, message, 8);
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

void proB_1(void)//�ڶ���
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
			UpdateSInedge();
        if(half_Detect() && (cn * 4 == edge - 1))
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
		SetLaserPosition(); // Set the laser position based on the current mode
    SetTargetCenter(); // Set the target center for the robot
    if(Init())
    {
        PID_SMotor_Cont(); // Call the PID control function for the motor
    }
		 Delay_ms(10); // Delay for 10 milliseconds
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

bool turn_func(void)//�ڶ���
{
    static float nowSInedge = 0; // Variable to track the current sInedge value
    if(half_Detect() && isturn == 0) // Check if the half detection condition is met
    {
        isturn = 1; // Set the isturn flag to indicate that the robot is turning
        nowSInedge = sInedge; // Store the current sInedge value
    }
    if(isturn == 1) // Check if the robot is turning
    {
			float first_dis = DisSensorToWheel * 1e-3 + nowSInedge  - 0.12;
			float second_dis = first_dis+ DEG_TO_RAD(90) * WHEEL_DIS * 1e-3 * 0.995;
        if(sInedge < first_dis) // Check if the sInedge value is less than the threshold �ߵ�Զ�ˣ����������
        {
            LSet(300); // Set the left motor speed to 300//�ߵĲ���ֱ ��������lspeed rspeed
            RSet(300); // Set the right motor speed to 300
            return true; // Return true to indicate that the robot is turning
        }
        else if(sInedge >= first_dis &&
             sInedge < second_dis )//ת��ǶȺܵ͵����
        {
						turning = true;
            LSet(-200); // Set the left motor speed to -300//���ת�䲻��ԭ�أ������
            RSet(200); // Set the right motor speed to 300
            return true; // Return true to indicate that the robot is turning
        }
				
				turning = false;
        sInedge = 0; // Reset the sInedge variable after the turn
        isturn = 0;
        edge++; // Increment the edge variable after the turn
    }
		return false;
		
}

bool Init(void)
{
    if(Laser_error == 1)
    {
        YP_SMotor_SetSpeed(-90, 0); // Set the speed of the motors to -120
        return false; // Return false to indicate initialization failure
    }
    return true; // Return true to indicate successful initialization
}