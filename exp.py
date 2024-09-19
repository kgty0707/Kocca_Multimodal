import serial
import time
import csv

# 아두이노와 연결
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)

def set_setpoint(setpoint):
    """
    아두이노에 새로운 Setpoint 값을 전달하고 현재 온도를 반환합니다.
    """
    arduino.write(f"{setpoint}\n".encode())
    
    while True:
        line = arduino.readline().decode('utf-8').strip()
        if line:
            print(f"Arduino: {line}")
            if "Temperature" in line:
                try:
                    current_temp = float(line.split()[1].replace('C', ''))
                    return current_temp
                except ValueError:
                    return None
            break

time.sleep(1)  # 초기화 시간

# CSV 파일 생성
csv_file = open('temperature_data.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Setpoint', 'Achieved Temperature', 'Time to Reach (s)', 'Feedback'])

try:
    while True:
        # 사용자가 Setpoint를 입력
        setpoint = input("Enter the desired setpoint temperature (or type 'exit' to quit): ")
        if setpoint.lower() == 'exit':
            break
        
        try:
            setpoint = float(setpoint)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        print(f"\nSetting Setpoint to: {setpoint}C")
        set_setpoint(setpoint)
        
        time.sleep(1)  # Setpoint가 적용되고 온도가 변할 시간을 줌
        
        start_time = time.time()  # 타이머 시작
        
        while True:
            current_temp = set_setpoint(setpoint)
            elapsed_time = time.time() - start_time  # 경과 시간 계산
            
            # 20초가 지나면 피드백을 받기 위한 조건 확인
            if elapsed_time > 20:
                # 목표 온도에 도달했는지 확인
                if current_temp is not None and abs(current_temp - setpoint) < 0.5:
                    print(f"Target temperature {setpoint}C reached in {elapsed_time:.2f} seconds!")
                else:
                    print(f"20 seconds passed. Current temperature is {current_temp}C.")
                
                # 사용자 입력을 받음
                feedback = input("Please provide your feedback on the system's performance: ")
                
                # 데이터를 CSV 파일에 기록
                csv_writer.writerow([setpoint, current_temp, round(elapsed_time, 2), feedback])
                break
        
        time.sleep(1)
finally:
    # 루프가 끝나면 파일과 시리얼 포트를 닫음
    csv_file.close()
    arduino.close()
