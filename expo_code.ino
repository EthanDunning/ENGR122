int x=0;
void setup() {
  pinMode(4, INPUT);
  Serial.begin(9600);
  tone(2,38000); 
  pinMode(10, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(8, LOW);
  digitalWrite(7, LOW);
}
 
void loop() {
  int detect=digitalRead(4);
  if(detect==0){
    Serial.println(detect);
    if(x==0){
      Serial.println("on");
    analogWrite(9, 255);  
      digitalWrite(8, HIGH);
      digitalWrite(7, LOW);
      delay(1000);
      x=1;
    }
    if(x==1){
       Serial.println("on");
      digitalWrite(8, LOW);
      digitalWrite(7, LOW);
      delay(3000);
    }
      }
  else{
    Serial.println(detect);
    if(x==1){
       Serial.println("off");
    analogWrite(9, 255);  
    digitalWrite(8, LOW);
    digitalWrite(7, HIGH);
    delay(1000);
    x=0;
    }
    else{
       Serial.println("off");
      digitalWrite(8, LOW);
    digitalWrite(7, LOW);
    }
  }
}
