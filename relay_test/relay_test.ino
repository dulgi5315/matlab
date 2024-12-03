int relaypin = 3;

void setup() {
  Serial.begin(9600);
  while (!Serial) delay(10);
  pinMode(relaypin, OUTPUT);
  // put your setup code here, to run once:

}

void loop() {
  digitalWrite(relaypin, HIGH);
  // put your main code here, to run repeatedly:
  delay(5000);

  digitalWrite(relaypin, LOW);
  delay(5000);
}
