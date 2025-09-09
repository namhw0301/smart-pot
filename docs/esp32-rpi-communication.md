# ESP32와 Raspberry Pi간 통신

## 하드웨어 연결
- GND 연결: 라즈베리파이 GND(핀 6번) → EPS32 GND핀
- 라즈베리파이 수신: 라즈베리파이 GPIO27(핀 8번, TXD) → EPS32 GPIO 16핀(UART 2 RXD)
- 라즈베리파이 송신: 라즈베리파이 GPIO28(핀 10번, RXD) → EPS32 GPIO 17핀(UART 2 TXD)
    
    esp32 uart 0은 usb 연결이므로 쓰면 x, 라즈베리파이 uart0은 실험 결과 uart 통신 시도할때마다 오류 발생 → 각각 uart2, uart1 사용으로 수정
- I2C 연결
    - SDA: 공기질, 조도 센서의 SDA와 EPS32의 GPIO21(SDA)
    - SCL: 공기질, 조도 센서의 SCL과 EPS32의 GPIO22(SCL)

## 라즈베리파이 설정
   - uart 1(ttyAMA1) 설정
   1. config.txt 수정
       
       ```cpp
       sudo nano /boot/firmware/config.txt
       ```
       
       들어가서 
       
       ```cpp
       [all]
       enable_uart=1
       dtoverlay=uart1
       ```
       
       로 수정
       
   2. 리부트
      ```cpp
      sudo reboot
      ```
