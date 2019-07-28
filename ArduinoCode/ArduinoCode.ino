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
  //Servo_3.write(177);
  //Servo_2.write(85);
}

bool IsReadingCommand = false;
int ByteNoRead = 0;
byte ServoNo = 0;
bool readServo = false;
int incomingByte;

//get all servos -> g
//set to angle b servo0 -> s0b


String getServoValues()
{
  //String str = String("Hello World..!");

  return  String(Servo_0.read()) + ";" + String(Servo_1.read()) + ";" + String(Servo_2.read()) + ";" + String(Servo_3.read()); 
}
void WriteToServo(byte ServoNo, byte incomingByte){
  if (incomingByte == '4') {
    Servo_2.write(incomingByte);
  }
}

void loop() {
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    ByteNoRead++;
    if(IsReadingCommand){
      if(ByteNoRead == 3){
          int read = incomingByte;
          Serial.println(read);
          WriteToServo(ServoNo, incomingByte);
          ByteNoRead=0;
          IsReadingCommand=false;
      }else{
        ServoNo=incomingByte;
      }
    }else{
      if (incomingByte == 'g') {
        Serial.println(getServoValues());
      }else{
        IsReadingCommand=true;
      }
    }
  }

}
