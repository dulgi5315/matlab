import serial
import time

# 시리얼 포트와 baud rate 설정
ser = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyUSB0'는 아두이노가 연결된 포트로 변경해야 합니다
time.sleep(2)  # 시리얼 포트가 안정화될 때까지 대기

try:
    while True:
        if ser.in_waiting >= 3:  # 3바이트가 수신될 때까지 대기
            # 3바이트 읽기
            num1 = ord(ser.read())
            num2 = ord(ser.read())
            num3 = ord(ser.read())
            
            # 수신한 숫자 출력
            print(f"Received numbers: {num1}, {num2}, {num3}")
        
        time.sleep(3)  # 3초 대기 (아두이노의 전송 주기와 맞춤)

except KeyboardInterrupt:
    print("프로그램 종료")
finally:
    ser.close()