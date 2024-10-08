import time
from main_program import set_setpoint

def read_file_continuously(filename):
    try:
        while True:
            with open(filename, "r") as file:
                data = file.read().strip()
                print(f"File Content:\n{data}\n")
                
                # 파일에서 읽은 값을 set_setpoint에 전달 (숫자로 변환해서 전달)
                try:
                    setpoint = float(data)  # 파일 내용이 온도 값일 경우, 숫자로 변환
                    current_temp = set_setpoint(setpoint)  # set_setpoint 함수 호출
                    print(f"Setpoint {setpoint}C applied. Current temperature: {current_temp}C")
                except ValueError:
                    print("Invalid data in file, cannot convert to setpoint.")
            
            # 1초 대기
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Program interrupted and stopped.")

filename = "temperature.txt"
read_file_continuously(filename)
