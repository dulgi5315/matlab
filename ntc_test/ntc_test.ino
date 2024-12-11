int ThermistorPin = A0;  
int Vo;  
float R1 = 100000;
float logR1_R2, logR2, R2, T, Tc, Tf;  
float c1 = 0.5365142801e-03, c2 = 2.410906850e-04, c3 = 0.2741993645e-07;  

float R = 100000;
float R_ntc1, R_ntc2, lnR_ntc_R, t, tc;

void setup() {  
Serial.begin(9600);  
}  
  
void loop() {  
  unsigned long current_time = millis();
  Serial.println(current_time);
  // 측정된 전압에서 R값 계산
  Vo = analogRead(ThermistorPin);  
  Serial.println(Vo);
  Serial.println();

  R_ntc1 = R * float(1023 - Vo) / float(Vo);
  Serial.println(R_ntc1);
  Serial.println();

  lnR_ntc_R = log(R_ntc1 / R);
  t = 1.0 / (1.0 / 298.15 + 1.0 / 4000 * lnR_ntc_R);
  tc = t - 273.15;
  Serial.println(tc);
  Serial.println();     
  
  delay(500);  
}  