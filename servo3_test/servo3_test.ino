#include <Servo.h>

Servo servo_top;
Servo servo_mid;
Servo servo_bot;

int motor_pin[] = {3, 4, 5};    // servo motor pin
int init_angle[] = {0, 0, 0};
int step_angle[] = {0, 23, 46, 69, 92, 115, 138, 161};

void setup() {
  Serial.begin(9600);
  while (!Serial) delay(10);
  
  servo_top.attach(motor_pin[0]);
  servo_mid.attach(motor_pin[1]);
  servo_bot.attach(motor_pin[2]);

}

void loop() {
  servo_top.write(0);
  servo_mid.write(0);
  servo_bot.write(0);
  Serial.println(0);
  delay(1000);

  servo_top.write(23);
  servo_mid.write(23);
  servo_bot.write(23);
  Serial.println(23);
  delay(1000);
  
  servo_top.write(46);
  servo_mid.write(46);
  servo_bot.write(46);
  Serial.println(46);
  delay(1000);
  
  servo_top.write(69);
  servo_mid.write(69);
  servo_bot.write(69);
  Serial.println(69);
  delay(1000);
  
  servo_top.write(92);
  servo_mid.write(92);
  servo_bot.write(92);
  Serial.println(92);
  delay(1000);
  
  servo_top.write(115);
  servo_mid.write(115);
  servo_bot.write(115);
  Serial.println(115);
  delay(1000);
  
  servo_top.write(138);
  servo_mid.write(138);
  servo_bot.write(138);
  Serial.println(138);
  delay(1000);
  
  servo_top.write(161);
  servo_mid.write(161);
  servo_bot.write(161);
  Serial.println(161);
  delay(1000);
  
}