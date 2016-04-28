#pragma config(Sensor, S3, colorSensor, sensorEV3_Color, modeEV3Color_Reflected)
#pragma config(Sensor, S4, sonarSensor, sensorEV3_Ultrasonic)
#pragma config(Motor, motorB, leftwheel, tmotorEV3_Large, PIDControl, encoder)
#pragma config(Motor, motorC, rightwheel, tmotorEV3_Large, PIDControl, encoder)

// consts for forward/backward
const int forwardSpeedSlow = -30;
const int forwardSpeedMed = -60;
const int forwardSpeedFast = -100;
const int backwardSpeedSlow = -forwardSpeedSlow;
const int backwardSpeedMed = -forwardSpeedMed;
const int backwardSpeedFast = -forwardSpeedFast;

// threshold for color sensor - we'll consider anything greater than this 'white'
const int whiteThreshold = 40;

// distance at which we switch to 'attack', in cm
const int attackDistance = 40;

// how many ms we reverse before attack, to avoid motor overshooting
const int reverseBeforeAttackTime = 80;

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

void turnRightSharply(int speed) {
	motor[rightwheel] = speed;
	motor[leftwheel] = -speed;
}

void turnLeftSharply(int speed) {
	motor[leftwheel] = speed;
	motor[rightwheel] = -speed;
}

//void fullStop() {
//	motor[leftwheel] = 0;
//	motor[rightwheel] = 0;
//}

int randBoolean() {
	return (rand() % 2);
}


task main()
{
	srand(nSysTime);

	int currentDistance = 0;
	int attackMode = 0;
	int spinDirection = 0;

	// gotta wait
	sleep(3000);

	// then gotta move forward a quarter turn or so
	move(forwardSpeedMed);
	sleep(333);

	while(true)
	{
		currentDistance = SensorValue[sonarSensor];

		if (attackMode == 1)
		{
			move(forwardSpeedFast);

			if (currentDistance > attackDistance) {
				// switch back to search mode
				attackMode = 0
				spinDirection = randBoolean();
			}
		}
		else // search
		{
			if (spinDirection == 0) {
				turnLeftSharply(forwardSpeedFast);
			} else {
				turnRightSharply(forwardSpeedFast);
			}

			if (currentDistance < attackDistance) {
				attackMode = 1;

				// spin back just a bit (?)
				turnLeftSharply(forwardSpeedFast);
				sleep(reverseBeforeAttackTime);
			}
		}

		// watch out for the edge
		if (SensorValue[colorSensor] > whiteThreshold) {
			move(backwardSpeedMed);
			sleep(300);

			if (randBoolean() == 0) {
				turnLeft(forwardSpeedMed);
			} else {
				turnRight(forwardSpeedMed);
			}

			// switch to search mode now that we've hopefully moved off the edge
			attackMode = 0;
			spinDirection = randBoolean();
		}

		sleep(50);
	}
}
