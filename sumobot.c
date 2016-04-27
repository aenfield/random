#pragma config(Sensor, S3, color3, sensorEV3_Color, modeEV3Color_Reflected)
#pragma config(Sensor, S4, sonar4, sensorEV3_Ultrasonic)
#pragma config(Motor, motorB, leftwheel,     tmotorEV3_Large, PIDControl, encoder)
#pragma config(Motor, motorC, rightwheel,    tmotorEV3_Large, PIDControl, encoder)

void move(int speed) {
	motor[leftwheel] = speed;
	motor[rightwheel] = speed;
}

void turnLeft(int speed) {
	motor[leftwheel] = speed;
}


task main()
{
	// consts for forward/backward
	const int forwardSpeedSlow = -30;
	const int forwardSpeedMed = -60;
	const int forwardSpeedFast = -100;
	const int backwardSpeedSlow = -forwardSpeedSlow;
	const int backwardSpeedMed = -forwardSpeedMed;
	const int backwardSpeedFast = -forwardSpeedFast;

	// distance at which we switch to 'attack', in cm
	const int attackDistance = 30;

	int currentDistance = 0;

	while(true)
	{
		currentDistance = SensorValue[sonar4];

		if (currentDistance > attackDistance)
		{
			// move forward, slowly, to get closer
			move(forwardSpeedSlow);
		}
		else
		{
			// attack!
			move(forwardSpeedFast);
		}

		if (SensorValue[color3] > 40) {
			move(backwardSpeedMed);
			sleep(300);

			turnLeft(forwardSpeedMed);
			sleep(300);
		}

		sleep(50);
	}
}
