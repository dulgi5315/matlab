int ThermistorPin = 3;  
int Vo;  
float R1 = 100000;
float logR1_R2, logR2, R2, T, Tc, Tf;  
float c1 = 0.5365142801e-03, c2 = 2.410906850e-04, c3 = 0.2741993645e-07;  
  
void setup() {  
Serial.begin(9600);  
}  
  
void loop() {  
// 측정된 전압에서 R값 계산
  Vo = analogRead(ThermistorPin);  
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR1_R2 = log(R2 / R1);  
  //T = (1.0 / (1 / 293.15 + 1 / 4000 * logR1_R2));
  logR2 = log(R2);

// R값을 이용해 온도 구하기
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));  
  Tc = T - 273.15;  
  Tf = (Tc * 9.0)/ 5.0 + 32.0;   
  Serial.print("Vo: ");
  Serial.print(Vo);      
  Serial.print(" Temperature: ");   
  Serial.print(Tf);  
  Serial.print(" F; ");  
  Serial.print(Tc);  
  Serial.println(" C");     
  
  delay(500);  
}  