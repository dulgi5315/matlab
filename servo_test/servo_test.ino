#include <Servo.h>

Servo servo;

int motor = 3;
int angle = -90;

void setup() {
  servo.attach(motor);
  Serial.begin(9600);

  Serial.println("Enter the u or d");
  Serial.println("u = angle + 15");
  Serial.println("d = angle - 15\n");
  
  // put your setup code here, to run once:

}

void loop() {
  if(Serial.available())
  {
    char input = Serial.read();

    if(input == 'u')
    {
      Serial.print("+15");
      for(int i = 0; i < 15; i++)
      {
        angle = angle + 1;
        if(angle >= 90)
          angle = 90;

        servo.write(angle);
        delay(10);
      }
      Serial.print("\t\t");
      Serial.println(angle);
    }
    else if (input == "d")
    {
      Serial.print("\t-15\t");
      for(int i = 0; i < 15; i++)
      {
        angle = angle - 1;
        if(angle <= -90)
          angle = -90;

        servo.write(angle);
        delay(10);
      }
      Serial.println(angle);
    }
    else
    {
      Serial.println("wrong character!!");
    }
  }
  // put your main code here, to run repeatedly:

}
