#include <PID_v1.h>

// 핀 정의
const int heaterPin = 10;  // 히터 (또는 펠티어 소자) 제어를 위한 PWM 출력 핀
const int dirPin = 13;     // 펠티어 소자의 방향 핀 (가열 또는 냉각)
const int tempSensorPin = A4;  // 온도 센서 입력 핀
float vout;

// PID 제어 변수
double Setpoint, Input, Output;

// PID 초기 파라미터
double Kp = 5, Ki = 4, Kd = 0;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

void setup() {
  pinMode(heaterPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  Serial.begin(9600);
  Serial.println("Ready");

  // 센서에서 읽은 값으로부터 초기 입력값 설정
  vout = analogRead(tempSensorPin);
  Input = (vout*500)/1023;

  Setpoint = 24;  // 목표 온도 설정 (36도 섭씨)

  myPID.SetMode(AUTOMATIC);  // PID를 자동 모드로 설정

  myPID.SetOutputLimits(-45, 35);  // Output의 최소값과 최대값 설정
}

void loop() {
  vout = analogRead(tempSensorPin);
  Input = (vout*500)/1023;

  myPID.Compute();
  

  if (Output > 1) {
    digitalWrite(dirPin, HIGH);
  } else {
    digitalWrite(dirPin, LOW);
    Output = -Output;
  }

  analogWrite(heaterPin, Output);
  Serial.print("Temperature: ");
  Serial.print(Input);
  Serial.print("C | Peltier Output: ");
  Serial.println(Output);

  Serial.print("Mode: ");
  Serial.println(digitalRead(dirPin) == HIGH ? "Heating" : "Cooling");
  delay(500);
}

double readTemperature() {
  int raw = analogRead(tempSensorPin);
  float temperature  = (raw * 500) / 1023;  // 0-5V 사이의 전압으로 변환
  return temperature;
}
