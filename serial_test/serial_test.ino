int r_hour = 0;
int r_min = 0;
int r_sec = 0;

int target_step = 0;
float target_temp[] = {0.0, 0.0, 0.0};

void setup()
{
  Serial.begin(9600);
  randomSeed(analogRead(0));
}

void loop()
{
  // 0.0-99.9 사이의 랜덤한 값 3개 생성
  float num1 = random(0, 1000) / 10.0;
  float num2 = random(0, 1000) / 10.0;
  float num3 = random(0, 1000) / 10.0;
  
  // 문자열로 변환하여 전송 (소수점 1자리까지)
  String dataString = String(num1, 1) + "," + String(num2, 1) + "," + String(num3, 1);
  
  // 시리얼 통신 데이터 처리 추가
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
      dataString = String(r_sec) + "," + "0" + "," + "0";
    }
    // 'T'로 시작하는 정온 설정 명령 처리
    else if (command.startsWith("T"))
    {
      target_temp[0] = command.substring(1).toFloat();
      target_temp[1] = command.substring(1).toFloat();
      target_temp[2] = command.substring(1).toFloat();
      dataString = String(target_temp[0], 1) + "," + String(target_temp[1], 1) + "," + String(target_temp[2], 1);
    }
    // 'S'로 시작하는 단계 설정 명령 처리
    else if (command.startsWith("S"))
    {
      target_step = command.substring(1).toInt();
      dataString = String(target_step) + "," + String(target_step) + "," +String(target_step);
    }
    // 'U'로 시작하는 사용자 설정 온도 명령 처리
    else if (command.startsWith("U"))
    {
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
      dataString = String(target_temp[0], 1) + "," + String(target_temp[1], 1) + "," + String(target_temp[2], 1);
    }
    // 'A'로 시작하는 중지 명령 처리
    else if (command.startsWith("A"))
    {
      dataString = "0,0,0";
    }
  }
  Serial.println(dataString);
  delay(3000);
}