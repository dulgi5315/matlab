int FSRsensor1 = A0;                           // 센서값을 아나로그 A0핀 설정
int FSRsensor2 = A11;                           // 센서값을 아나로그 A0핀 설정


int value1 = 0;                                       // loop에서 사용할 변수 설정
int value2 = 0;                                       // loop에서 사용할 변수 설정

void setup() 

{

  Serial.begin(9600);                           // 시리얼 통신 설정 (보드레이트 9600)

}


void loop() 

{

  value1 = analogRead(FSRsensor1);     // 센서값을 아나로그로 읽어 value 변수에 저장
  value2 = analogRead(FSRsensor2);     // 센서값을 아나로그로 읽어 value 변수에 저장
  
  Serial.println(value1);                           // 센서값을 시리얼 모니터에 출력
  Serial.println(value2);                           // 센서값을 시리얼 모니터에 출력
  Serial.println();                           // 센서값을 시리얼 모니터에 출력
  

  value1 = map(value1, 0, 1023, 0, 255); // value에 저장된 센서값(0~1023)을 PWM값 0~255의 범위로 변환
  value2 = map(value2, 0, 1023, 0, 255); // value에 저장된 센서값(0~1023)을 PWM값 0~255의 범위로 변환

  delay(100);                                         // 1초의 딜레이

}