#define SERIAL_BAUD_RATE 9600

#include <Wire.h>
#include <Servo.h>

unsigned long myTime;
Servo myservo;
float distance;
float kp = 0.0;
float ki = 0.0;
float kd = 0.0;
float proportional = 0.0;
float integral = 0.0;
float derivative = 0.0;
float previousError = 0.0;
float distance_point = 0.0;
float output= 0.0;
int servo_zero = 0;
int t = 200;
float errors = 0;

int last_added = 0;

char commands[256];
void (*functions[256]) (float);

auto test(float) -> void;
auto start(float) -> void;

auto map(char, void (*func)(float) ) -> void;

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  myservo.attach(9);
  myservo.write(95);
  pinMode(A0,INPUT);

  map('T',test);
  map('S',start);
  map('s', [](float val){distance_point = val;});
  map('z',[](float val){servo_zero = val;});
  map('d',[](float val){kd = val;});
  map('i',[](float val){ki = val;});
  map('p',[](float val){kp = val;});

  myTime = millis();
}

void loop() {
  while(!Serial.available()) {}
  
  auto val = Serial.parseInt();
  auto command = Serial.read();
  auto checksum = Serial.parseInt();

  if (checksum == val ^ command){
    functions[commands[command]](*((float *)&val));
    Serial.println("ACK");
  } else {
    Serial.println("NACK");
  }
}

auto map(char comm, void (*func)(float)) -> void {
  commands[comm] = last_added;
  functions[last_added++] = func;
}

auto get_dist(int n) -> float {
  long sum=0;
  for(int i=0;i<n;i++){
    sum=sum+analogRead(A0);
  }  
  float adc=sum/n;

  float distance_cm = 17569.7 * pow(adc, -1.2062);
  return(distance_cm);
}

auto PID() -> void {
  proportional = distance-distance_point;
  integral = integral+proportional*0.1;
  derivative=(proportional-previousError)/0.1;
  output=kp*proportional+ki*integral+kd*derivative;
  previousError=proportional;
  myservo.write(servo_zero+output);
}

auto test(float val) -> void {
  long tm = millis() + ((long)val * 1000);
  while(millis() < tm) {
    if (millis() > myTime+t) {
      distance = get_dist(100); 
      myTime = millis();
      PID();
      Serial.print(distance);
      Serial.print(" : ");
      Serial.print(proportional);
      Serial.print(" : ");
      Serial.println(output);
    }
  }
}

auto start(float val) -> void {
  long time = millis() + 10000;
  float errors = 0;
  long counter = 0;
  while(millis() < time + 3000) {
    if (millis() > myTime+t) {
      distance = get_dist(100); 
      myTime = millis();
      PID();
    }
    if(millis() > time) {
      errors += abs(previousError);
      counter++;
    }
  }
  
  float mae = errors/(float)counter;

  Serial.print("MAE: ");
  Serial.println(mae);
}