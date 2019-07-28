#include <Servo.h> 

Servo Servo_0;
Servo Servo_1;
Servo Servo_2;
Servo Servo_3;


//Record the data.
int Servo3Angle = 0;

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

void loop() {
  // put your main code here, to run repeatedly:

}
