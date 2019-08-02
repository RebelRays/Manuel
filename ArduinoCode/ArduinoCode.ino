#include <Servo.h> 

//How about attach -> run for 0.3s detach?

//2
Servo servos[4];

void setup() {
  //Start the serial for debug.
  Serial.begin(9600);
  
  //Attach the servos on pins to the servo object
  //Servo_0.attach(4);
  //Servo_1.attach(5);
  //Servo_2.attach(6);
  //Servo_3.attach(7);

  //Servo_4.attach(8);
  
  //Servo_4.write(0);
  //delay(3000);
  //Servo_4.write(90);
  Serial.println("setup()");
}

int getPin(int ServoNo){
  if(ServoNo != 3){
    return 4+ServoNo;
  }
  return 8;
}

void attachServo(int ServoNo){
  servos[ServoNo].attach(getPin(ServoNo));
}

void detachServo(int ServoNo){
  servos[ServoNo].detach();
}

int incomingByte = 0;
String getServoValues()
{
  return  String(servos[0].read()) + ";" + String(servos[1].read()) + ";" + String(servos[2].read()) + ";" + String(servos[3].read()); 
}


void loop() {
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if(incomingByte == 'p'){
      Serial.println("Pong");
    }
    else if(incomingByte == 'g'){
      Serial.println(getServoValues());
    }else if((incomingByte >= 's')){

      delay(30);
      if (Serial.available() == 0){
        Serial.println("Error Expected Servo & Angle");
        return;
      }
      incomingByte = Serial.read();
      Serial.println("Reading Servo " + String(incomingByte));

      int ServoNo = incomingByte - '1';
      if(ServoNo>3){
        Serial.println("Error Incorrect ServerNo :" + String(incomingByte));
        return;
      }
      
      delay(30);
      if (Serial.available() == 0){
        Serial.println("Error Expected Angle1");
        return;
      }

     
      incomingByte = Serial.read();
      Serial.println("Reading Angle1 " + String(incomingByte));
      int Angle1 = incomingByte - '0';
      if(Angle1 > 9){
        Serial.println("Error, angle1 value should be between 0 to 9");
        return;
      }

      delay(30);
      if (Serial.available() == 0){
        Serial.println("Error Expected Angle2");
        return;
      }

      incomingByte = Serial.read();
      Serial.println("Reading Angle2 " + String(incomingByte));
      int Angle2 = incomingByte - '0';
      if(Angle2 > 9){
        Serial.println("Error, angle2 value should be between 0 to 9");
        return;
      }

      delay(30);
      if (Serial.available() == 0){
        Serial.println("Error Expected Angle3 ");
        return;
      }

      incomingByte = Serial.read();
      Serial.println("Reading Angle3 " + String(incomingByte));
      int Angle3 = incomingByte - '0';
      if(Angle3 > 9){
        Serial.println("Error, angle3 value should be between 0 to 9");
        return;
      }


      int TotAngel = Angle1*100 + Angle2*10 + Angle3;

      attachServo(ServoNo);
      //servos[ServoNo].write(TotAngel);
      delay(500);
      detachServo(ServoNo);
    }
  }
  delay(10);
}
