import serial
from gtts import gTTS
import os
from pushbullet import Pushbullet
from playsound import playsound

# Pushbullet API 키 입력
pb = Pushbullet("o.1iA5k9LnOz6jyaneakU86VEnwHoWOHB9")  # 여기에 키 입력
tts_file = "/tmp/tts.mp3"

# UART1 사용 시: /dev/ttyAMA1
ser = serial.Serial('/dev/ttyAMA1', 9600, timeout=1)

# 판단 기준 반영한 메시지 생성 함수
def make_message(eCO2, lux):
    eCO2 = int(eCO2)
    lux = int(lux)

    msg = f"물이 감지되었습니다. 이산화탄소 농도는 {eCO2}ppm이고 조도는 {lux}입니다."

    if eCO2 >= 800:
        msg += " 환기가 필요합니다."

    if lux <= 50:
        msg += " 커튼을 걷어 햇빛을 들이세요."
    elif lux >= 300:
        msg += " 날씨가 좋으니 잠깐 외출해보시는 건 어떨까요?"

    return msg

print("Raspberry Pi: 센서 데이터 수신 대기 중...")

while True:
    try:
        line = ser.readline().decode().strip()

        if line.startswith("1"):
            parts = line.split(",")
            if len(parts) == 3:
                eCO2 = parts[1]
                lux = parts[2]

                message = make_message(eCO2, lux)
                print(f"[수신] {message}")

                # TTS 변환 및 재생
                tts = gTTS(text=message, lang='ko')
                tts.save(tts_file)
                playsound(tts_file)

                # Pushbullet 알림 전송
                pb.push_note("스마트 화분 알림", message)

    except Exception as e:
        print(f"[ERROR] {e}")
