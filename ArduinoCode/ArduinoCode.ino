#include <Servo.h> 

//2
Servo Servo_0;
Servo Servo_1;
Servo Servo_2;
Servo Servo_3;

int MovingServoNo = 0;
int PreciouseServoAngle = 0;
int AimForAngles[4];
Servo servos[4];

void setup() {
  //Start the serial for debug.
  Serial.begin(9600);
  
  //Attach the servos on pins to the servo object
  Servo_0.attach(4);
  Servo_1.attach(5);
  Servo_2.attach(6);
  Servo_3.attach(7);
  servos[0] = Servo_0;//{Servo_0, Servo_1, Servo_2, Servo_3};
  servos[1] = Servo_1;
  servos[2] = Servo_2;
  servos[3] = Servo_3;
  //Set the pin 3 to input
  //pinMode(3, INPUT);
  
  Serial.print("setup()");
  //Serial.print("Servo_3:");
  //Serial.println(Servo_3.read());
  //Serial.print("Servo_2:");
  //Serial.println(Servo_2.read());
  //Serial.print("Servo_1:");
  //Serial.println(Servo_1.read());
  //Serial.print("Servo_0:");
  //Serial.println(Servo_0.read());
  
  //90;180;70;172
  Servo_0.write(87); //Higher towards ultra sound
  delay(500);
  Servo_1.write(175); //smaller closer to ground
  delay(500);
  Servo_2.write(67); //The more down to wards ground
  delay(500);
  Servo_3.write(170); //The more close

  AimForAngles[0]=90;
  AimForAngles[1]=177;
  AimForAngles[2]=70;
  AimForAngles[3]=176;

  Servo_0.write(90); //Higher towards ultra sound
  delay(300);
  Servo_1.write(177); //smaller closer to ground
  delay(300);
  Servo_2.write(70); //The more down to wards ground
  delay(300);
  Servo_3.write(176); //The more, the more up
  Serial.print("setup_complete()");
}




bool LoadedServoNo = false;
bool IsReadingCommand = false;
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
    //Serial.println("Serial.read = " + String(incomingByte));

    if(IsReadingCommand){
      if(LoadedServoNo){
          LastAngle = incomingByte;
          Serial.println(LastAngle);
          NoOfCommandsExecuted++;

          AimForAngles[ServoNo-1]=LastAngle;
          //WriteToServo(ServoNo, LastAngle);
          IsReadingCommand=false;
          LoadedServoNo=false;
      }else{
        ServoNo=incomingByte;// - '0';
        LoadedServoNo=true;
        //Serial.println("Setting ServoNo to " + String(ServoNo) + ", from " + String(incomingByte));
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
        LoadedServoNo=false;
      }
    }
  }else{
    //Time to move
    for(int i=0;i<4;i++){
      int currentAngle = servos[i].read();
      if(AimForAngles[i] != currentAngle){
        servos[i].write(AimForAngles[i]);
        delay(500);
        if(currentAngle == servos[i].read()){ //Stuck --> accept it
          Serial.println("Not Moving: Servo No: " + i);
          AimForAngles[i] = currentAngle;
          servos[i].write(currentAngle);
        }
      }
    }
  }
  delay(10);
}
