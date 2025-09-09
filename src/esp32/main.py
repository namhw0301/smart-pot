#include <Wire.h>
#include <BH1750.h>
#include <Adafruit_CCS811.h>

BH1750 lightMeter;
Adafruit_CCS811 ccs;

const int waterPin = 33;  // YL-83 물 센서 핀

void setup() {
  Serial.begin(9600);
  pinMode(waterPin, INPUT);

  Wire.begin();
  lightMeter.begin();

  if (!ccs.begin()) {
    while (1); // CCS811 초기화 실패 시 멈춤
  }

  while (!ccs.available()); // CCS811 준비 대기
}

void loop() {
  int waterDetected = digitalRead(waterPin);

  if (waterDetected == LOW) { // LOW면 물 감지됨
    if (!ccs.readData()) {
      uint16_t eCO2 = ccs.geteCO2();           // 이산화탄소 농도
      uint16_t lux = lightMeter.readLightLevel(); // 조도

      // 포맷: waterDetected(1),eCO2,lux
      Serial.print("1,");
      Serial.print(eCO2);
      Serial.print(",");
      Serial.println(lux);
    }

    delay(5000); // 중복 감지 방지용 지연
  }
}
