int FSRsensor = A0;                           // 센서값을 아나로그 A0핀 설정

int value = 0;                                       // loop에서 사용할 변수 설정

void setup() 

{

  Serial.begin(9600);                           // 시리얼 통신 설정 (보드레이트 9600)

}


void loop() 

{

  value = analogRead(FSRsensor);     // 센서값을 아나로그로 읽어 value 변수에 저장

  Serial.println(value);                           // 센서값을 시리얼 모니터에 출력

  value = map(value, 0, 1023, 0, 255); // value에 저장된 센서값(0~1023)을 PWM값 0~255의 범위로 변환

  delay(100);                                         // 1초의 딜레이

}