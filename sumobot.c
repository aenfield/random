#pragma config(Sensor, S3, colorSensor, sensorEV3_Color, modeEV3Color_Reflected)
#pragma config(Sensor, S4, sonarSensor, sensorEV3_Ultrasonic)
#pragma config(Motor, motorB, leftwheel,     tmotorEV3_Large, PIDControl, encoder)
#pragma config(Motor, motorC, rightwheel,    tmotorEV3_Large, PIDControl, encoder)

void move(int speed) {
	motor[leftwheel] = speed;
	motor[rightwheel] = speed;
}

void turnLeft(int speed) {
	motor[leftwheel] = speed;
}

void turnRight(int speed) {
	motor[rightwheel] = speed;
}

int randBoolean() {
	return (rand() % 2);
}


task main()
{
	srand(nSysTime);

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

	int foo = 0;

	//while(true) {
	//	foo = randBoolean();
	//}

	while(true)
	{
		currentDistance = SensorValue[sonarSensor];

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

		if (SensorValue[colorSensor] > 40) {
			move(backwardSpeedMed);
			sleep(300);

			if (randBoolean() == 0) {
				turnLeft(forwardSpeedMed);
			} else {
				turnRight(forwardSpeedMed);
			}
			sleep(300);
		}

		sleep(50);
	}
}
