import random

def generate_temperature_data(filename):
    # 온도 리스트
    temperatures = [40, 36, 32, 28, 24]

    # 텍스트 파일에 저장할 데이터 리스트
    data_to_save = []

    random.shuffle(temperatures)  # 온도 리스트 전체를 섞음

    # 첫 번째 온도를 고정하고 나머지 온도를 조합
    for first_temp in temperatures:
        remaining_temps = [temp for temp in temperatures if temp != first_temp]  # 나머지 온도들
        random.shuffle(remaining_temps)  # 나머지 온도들 섞기

        # 두 조합의 첫 번째 값에 first_temp를 고정하고, 나머지 네 개의 온도를 조합
        data_to_save.append(f"{first_temp}, {remaining_temps[0]}, {first_temp}, {remaining_temps[1]}, {first_temp}, {remaining_temps[2]}, {first_temp}, {remaining_temps[3]}")

    # 텍스트 파일에 저장
    with open(filename, "w") as file:
        for line in data_to_save:
            file.write(line + "\n")

    print(f"Temperature data has been saved to '{filename}'.")
    return filename
