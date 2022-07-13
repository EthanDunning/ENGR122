
int x=0;

void setup() {
  Serial.begin(9600);
  tone(2,38000); 
  pinMode(4, INPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(10, OUTPUT);
  digitalWrite(8, LOW);
  digitalWrite(7, LOW);
}
 
void loop() {
  int detect=digitalRead(4);
  
  Serial.println(detect);
  if(detect==0){

    if(x==0){
      Serial.println("A");
      Serial.println("on");
      digitalWrite(7, LOW);
      digitalWrite(8, HIGH);
      analogWrite(10, 255);  
      delay(1000);
      x=1;
    }
    if(x==1){
      Serial.println("B");
      Serial.println("on");
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      delay(3000);
    }
  }

  else{
    if(x==1){
    Serial.println("C");
    Serial.println("off");
    analogWrite(10, 255);  
    digitalWrite(8, LOW);
    digitalWrite(7, HIGH);
    delay(1000);
    x=0;
    }
    else{
      Serial.println("D");
      Serial.println("off");
      digitalWrite(8, LOW);
      digitalWrite(7, LOW);
    }
  }
}
