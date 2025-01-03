#include <Servo.h>

Servo servo_top;
Servo servo_mid;
Servo servo_bot;

// ntc sensor pin
int ntc_sensor_pin[] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11};

int Vo;
float R = 100000;
float R_ntc, lnR_ntc_R, Tk;
float Tc[] = {0.0, 0.0, 0.0};

int target_step = 0;
float target_temp[] = {0.0, 0.0, 0.0};

int pressure_sensor_R = A12;  // pressure sensor pin
int pressure_sensor_L = A13;

int motor_pin[] = {3, 4, 5};    // servo motor pin
int init_angle[] = {0, 0, 0};
int angle[] = {0, 0, 0};
int step_angle[] = {0, 23, 46, 69, 92, 115, 138, 161};

int relay_pin = 6;                // relay pin

int r_hour = 0;
int r_min = 0;
int r_sec = 0;

void setup()
{
  Serial.begin(9600);
  while (!Serial) delay(10);
  
  servo_top.attach(motor_pin[0]);
  servo_mid.attach(motor_pin[1]);
  servo_bot.attach(motor_pin[2]);
  
  pinMode(relay_pin, OUTPUT);

  // 릴레이 OFF
  digitalWrite(relay_pin, LOW);
}

void loop()
{
  unsigned long current_time = millis();

  // 시리얼 통신 데이터 처리
  if (Serial.available() > 0)
  {
    String command = Serial.readStringUntil('\n');
    
    // 'R'로 시작하는 예약 명령 처리
    if (command.startsWith("R") && command.length() == 5)
    {
      // 시간과 분 파싱
      r_hour = command.substring(1, 3).toInt();
      r_min = command.substring(3, 5).toInt();
      
      // 시간과 분을 초로 변환하여 저장
      r_sec = (r_hour * 3600) + (r_min * 60);
    }
    // 'T'로 시작하는 정온 설정 명령 처리
    else if (command.startsWith("T"))
    {
      // 릴레이 ON
      digitalWrite(relay_pin, HIGH);

      target_temp[0] = command.substring(1).toFloat();
      target_temp[1] = command.substring(1).toFloat();
      target_temp[2] = command.substring(1).toFloat();
    }
    // 'S'로 시작하는 단계 설정 명령 처리
    else if (command.startsWith("S"))
    {
      // 릴레이 ON
      digitalWrite(relay_pin, HIGH);

      target_step = command.substring(1).toInt();
            
      // 서보 모터 각도 설정
      servo_top.write(step_angle[target_step - 1]);
      servo_mid.write(step_angle[target_step - 1]);
      servo_bot.write(step_angle[target_step - 1]);

      target_temp[0] = 0.0;
      target_temp[1] = 0.0;
      target_temp[2] = 0.0;
    }
    else if (command.startsWith("U"))
    {
      // 릴레이 ON
      digitalWrite(relay_pin, HIGH);

      String temp_str = command.substring(1);
      int idx = 0;
      int start = 0;
      int comma_idx;
            
      // 콤마로 구분된 온도값 파싱
      while ((comma_idx = temp_str.indexOf(',', start)) != -1 && idx < 3)
      {
        target_temp[idx++] = temp_str.substring(start, comma_idx).toFloat();
        start = comma_idx + 1;
      }
      // 마지막 온도값 처리
      if (idx < 3)
      {
        target_temp[idx] = temp_str.substring(start).toFloat();
      }
    }
    // 'X'로 시작하는 중지 명령 처리
    else if (command.startsWith("A"))
    {
      // 릴레이 OFF
      digitalWrite(relay_pin, LOW);

      // 서보 모터 초기 위치로 복귀
      servo_top.write(init_angle[0]);
      servo_mid.write(init_angle[1]);
      servo_bot.write(init_angle[2]);
            
      // 변수 초기화
      target_step = 0;
      for(int i = 0; i < 3; i++)
      {
        target_temp[i] = 0.0;
      }
      r_hour = 0;
      r_min = 0;
      r_sec = 0;
    }
  }
  
  for (int i = 0; i < 12; i++)
  {
    Vo = analogRead(ntc_sensor_pin[i]);
    R_ntc = R * float(1023 - Vo[i]) / float(Vo[i]);
    lnR_ntc_R = log(R_ntc / R);
    Tk = 1.0 / (1.0 / 298.15 + 1.0 / 4000 * lnR_ntc_R);
    
    if (i >= 0 and i < 4)
    {
      Tc[0] += (Tk - 273.15);
    }
    else if (i >= 4 and i < 8)
    {
      Tc[1] += (Tk - 273.15);
    } 
    else
    {
      Tc[2] += (Tk - 273.15);
    }
  }

  Tc[0] = (Tc[0] / 4);
  Tc[1] = (Tc[1] / 4);
  Tc[2] = (Tc[2] / 4);

   //PID 제어
  if (target_temp[0] != 0.0 && target_temp[1] != 0.0 && target_temp[2] != 0.0)
  {
    nxt_angle[0] = angle[0] + PID();
    nxt_angle[1] = angle[1] + PID();
    nxt_angle[2] = angle[2] + PID();

    servo_top.write(nxt_angle[0]);
    servo_mid.write(nxt_angle[1]);
    servo_bot.write(nxt_angle[2]);

    angle[0] = nxt_angle[0];
    angle[1] = nxt_angle[1];
    angle[2] = nxt_angle[2];
  }

  // 문자열로 변환하여 전송
  String tempString = String(Tc[0], 1) + "," + String(Tc[1], 1) + "," + String(Tc[2], 1);
  Serial.println(tempString);

  for (int i = 0; i < 3; i++)
  {
    Tk[i] = 0.0;
  }

  delay(100);
}