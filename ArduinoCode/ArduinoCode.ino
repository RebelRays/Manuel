#include <Servo.h> 

Servo Servo_0;
Servo Servo_1;
Servo Servo_2;
Servo Servo_3;

void setup() {
  //Start the serial for debug.
  Serial.begin(9600);
  
  //Attach the servos on pins to the servo object
  Servo_0.attach(4);
  Servo_1.attach(5);
  Servo_2.attach(6);
  Servo_3.attach(7);
  
  //Set the pin 3 to input
  pinMode(3, INPUT);
  
  Serial.print("Servo_3:");
  Serial.println(Servo_3.read());
  Serial.print("Servo_2:");
  Serial.println(Servo_2.read());
  Serial.print("Servo_1:");
  Serial.println(Servo_1.read());
  Serial.print("Servo_0:");
  Serial.println(Servo_0.read());
  
  Servo_0.write(5); //Higher towards ultra sound
  Servo_1.write(5); //smaller closer to ground
  Servo_2.write(120); //The more down to wards ground
  Servo_3.write(176); //The more close
}

bool IsReadingCommand = false;
int ByteNoRead = 0;
int ServoNo = 0;
int incomingByte = 0;
int LastAngle= 0;
int NoOfCommandsExecuted = 0;
String getServoValues()
{
  //String str = String("Hello World..!");

  return  String(Servo_0.read()) + ";" + String(Servo_1.read()) + ";" + String(Servo_2.read()) + ";" + String(Servo_3.read()); 
}
void WriteToServo(int ServoNo, int angle){
  if (ServoNo == 4) {
    Servo_3.write(angle);
  }else if (ServoNo == 3) {
    Servo_2.write(angle);
  }else if (ServoNo == 2) {
    Servo_1.write(angle);
  }else if (ServoNo == 1) {
    Servo_0.write(angle);
  }else{
     Serial.println("Confused, ServoNo = " + String(ServoNo) + ", angle=" + String(angle)  );
  }
}

void loop() {
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    ByteNoRead++;
    if(IsReadingCommand){
      if(ByteNoRead == 3){
          LastAngle = incomingByte;
          Serial.println(LastAngle);
          NoOfCommandsExecuted++;
          WriteToServo(ServoNo, LastAngle);
          ByteNoRead=0;
          IsReadingCommand=false;
      }else{
        ServoNo=incomingByte - '0';
        Serial.println("Setting ServoNo to " + String(ServoNo) + ", from " + String(incomingByte));
      }
    }else{
      if (incomingByte == 'g') {
        Serial.println(getServoValues());
      }else if (incomingByte == 'p') {
        Serial.println("Pong");
      }else if (incomingByte == 'r') {
        Serial.println(String(NoOfCommandsExecuted) + ";" + String(ServoNo) + ";" + String(LastAngle));
      }else if (incomingByte == 's') {
        IsReadingCommand=true;
      }
      else{
        Serial.println("Unknown Command");
        Serial.println(incomingByte);
        Serial.println(String(incomingByte));
      }
    }
  }

}
