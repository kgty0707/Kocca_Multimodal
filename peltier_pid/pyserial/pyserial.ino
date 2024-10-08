#include <PID_v1.h>

// 핀 정의
const int heaterPin = 6;  // 히터 (또는 펠티어 소자) 제어를 위한 PWM 출력 핀
const int dirPin = 7;     // 펠티어 소자의 방향 핀 (가열 또는 냉각)
const int tempSensorPin = A3;  // 온도 센서 입력 핀
float vout;

// PID 제어 변수
double Setpoint, Input, Output;

// PID 초기 파라미터
double Kp = 7, Ki = 6, Kd = 1;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

// 안정화 체크 변수
bool isStable = false;
unsigned long stableStartTime = 0;
const unsigned long stableDelay = 5000;  // 온도가 안정화된 후 5초 동안 유지되면 고정

void setup() {
  pinMode(heaterPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  Serial.begin(9600);
  Serial.println("Ready");

  // 센서에서 읽은 값으로부터 초기 입력값 설정
  vout = analogRead(tempSensorPin);
  Input = (vout*500)/1023;

  Setpoint = 24;  // 목표 온도 설정 (섭씨 24도)

  myPID.SetMode(AUTOMATIC);  // PID를 자동 모드로 설정

  myPID.SetOutputLimits(-75, 65);  // Output의 최소값과 최대값 설정
}

void loop() {
  if (Serial.available() > 0) {
    // 시리얼 통신으로 받은 값을 Setpoint로 설정
    String inputString = Serial.readStringUntil('\n');
    Setpoint = inputString.toFloat();
    Serial.print("New Setpoint: ");
    Serial.println(Setpoint);
    isStable = false;  // 새로운 Setpoint가 설정되면 안정화 체크 초기화
  }

  delay(500);

  vout = analogRead(tempSensorPin);
  Input = (vout*500)/1023;

  if (!isStable) {
    myPID.Compute();  // PID 계산 수행
    
    // 안정화 체크: 일정 범위 내에서 온도가 유지되면 안정화된 것으로 간주
    if (abs(Input - Setpoint) < 0.5) {
      if (stableStartTime == 0) {
        stableStartTime = millis();  // 안정화 시작 시간 기록
      } else if (millis() - stableStartTime >= stableDelay) {
        isStable = true;  // 온도가 안정화되었음
        Serial.println("Temperature stabilized. PID output fixed.");
      }
    } else {
      stableStartTime = 0;  // 안정화 시간 초기화
    }
  }
  
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
