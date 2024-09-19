import serial
import time
import csv
from gui_module import show_name_window, show_time_window, show_feedback_window
from random_temp import generate_temperature_data

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


def read_temperature_data(filename):
    with open(filename, "r") as file:
        data = file.readlines()
    return [line.strip().split(", ") for line in data]

# 초기화 시간
time.sleep(1)

# 사용자 이름 입력 창 표시
name = show_name_window()

# 사용자에게 시간 선택 창 표시
selected_time = show_time_window()

filename = generate_temperature_data(f'{name}_masking_result_data.txt')

# selected_time이 None인지 확인
if selected_time is None:
    print("No time interval selected. Exiting the program.")
    exit()

# CSV 파일 생성
csv_file = open(f'{name}_masking_data.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Setpoint', 'Achieved Temperature', 'Time Interval (s)', 'Time to Reach (s)', 'Feedback'])

# 텍스트 파일에서 온도 데이터 읽기
temperature_data = read_temperature_data(filename='test_result.txt')

try:
    for temperature_set in temperature_data:
        for setpoint_str in temperature_set:
            setpoint = float(setpoint_str)
            print(f"\nSetting Setpoint to: {setpoint}C")
            set_setpoint(setpoint)
            
            time.sleep(1)  # Setpoint가 적용되고 온도가 변할 시간을 줌
            
            start_time = time.time()  # 타이머 시작
            
            while True:
                current_temp = set_setpoint(setpoint)
                elapsed_time = time.time() - start_time  # 경과 시간 계산
                
                # 선택된 시간이 지나면 피드백을 받기 위한 조건 확인
                if elapsed_time > selected_time:
                    # 목표 온도에 도달했는지 확인
                    if current_temp is not None and abs(current_temp - setpoint) < 0.5:
                        print(f"Target temperature {setpoint}C reached in {elapsed_time:.2f} seconds!")
                    else:
                        print(f"{selected_time} seconds passed. Current temperature is {current_temp}C.")
                    
                    # 피드백 창 표시
                    feedback_result = show_feedback_window()
                    
                    # 데이터를 CSV 파일에 기록
                    csv_writer.writerow([name, setpoint, current_temp, selected_time, round(elapsed_time, 2), feedback_result])
                    
                    break
            
            time.sleep(1)
finally:
    # 루프가 끝나면 파일과 시리얼 포트를 닫음
    csv_file.close()
    arduino.close()