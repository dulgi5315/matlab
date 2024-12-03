#include <Servo.h>

Servo servo;

int ntc_sensor_pin = [A0, A1, A2, A3, A4,               //ntc sencor pin
                      A5, A6, A7, A8, A9,
                      A10, A11, A12, A13, A14];
int V0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
float R0 = 100000;
float R1, lnR1, T;
float Tk = [0.0, 0.0, 0.0], Tc = [0.0, 0.0, 0.0];
float c1 = 0.5365142801e-03, c2 = 2.410906850e-04, c3 = 0.2741993645e-07;

int pressure_sensor_1 = A15;  // pressure sensor pin
//int pressure_sensor_2 = A16;

int motor_pin = [3, 4, 5];    // servo motor pin
int init_angle = [0, 0, 0];

int relay_pin = 6;                // relay pin

void setup()
{
  Serial.begin(9600)
  while (!Serial) delay(10);
  
  servo.attach(motor_top)
  servo.attach(motor_mid)
  servo.attach(motor_bot)
  
  pinMode(relay, OUTPUT);
}

void loop()
{
  for (int i = 0; i < 16; i++)
  {
    V0[i] = analogRead(ntc_sensor_pin[i]);
  }
  
  for (int i = 0; i < 16; i++)
  {
    R1 = R0 * (1023.0 / (float)V0[i] - 1.0);
    lnR1 = log(R1 / R0);
    T = (1.0 / (c1 + c2 * lnR1 + c3 * lnR1* lnR1* lnR1));
    if (i >= 0 and i < 5)
    {
      Tk[0] += T;
    }
    else if (i >= 5 and i < 10)
    {
      Tk[1] += T;
    } 
    else
    {
      Tk[2] += T;
    }
  }

  Tc[0] = (Tk[0] / 3) - 273.15;
  Tc[1] = (Tk[1] / 3) - 273.15;
  Tc[2] = (Tk[2] / 3) - 273.15;

  

  delay(100)
}
