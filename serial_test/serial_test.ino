void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0));
}

void loop() {
  // 0-99 사이의 랜덤한 숫자 3개 생성
  byte num1 = random(0, 100);
  byte num2 = random(0, 100);
  byte num3 = random(0, 100);
  
  // 바이트 배열로 직접 전송
  Serial.write(num1);
  Serial.write(num2);
  Serial.write(num3);
  
  delay(3000);
}