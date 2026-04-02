# 스마트 화분 시스템 (Smart Flowerpot for Elderly Care)

센서 기반 환경 인식과 표정 분석을 결합하여 독거노인의 정서와 생활 상태를 케어하는 IoT 시스템

---

## Overview

* 기간: 2025.03 ~ 2025.06
* 형태: 전자공학 종합설계 프로젝트
* 역할: 하드웨어 설계 및 센서 통신, 시스템 통합

기존 스마트 화분은 단순 환경 모니터링에 그치는 경우가 많았다.
본 프로젝트에서는 이를 확장하여, **사용자의 상태(표정)와 환경 데이터를 함께 활용하는 케어 시스템**을 목표로 설계하였다.

특히 카메라 사용에 따른 프라이버시 문제를 고려하여, **물 주는 순간에만 카메라가 동작하도록 설계**하였다.

---

## System Architecture

본 시스템은 ESP32와 Raspberry Pi를 분리하여 역할 기반 구조로 설계하였다.

* **ESP32 (Sensor Hub)**

  * 조도, 공기질, 수분 센서 데이터 수집
  * 이벤트 판단 후 Raspberry Pi로 전송

* **Raspberry Pi (Processing Unit)**

  * 카메라 제어 및 이미지 처리
  * 표정 인식 및 AI 기반 메시지 생성
  * TTS 및 알림 전송

* **통신**

  * UART 기반 시리얼 통신 (115200 baud)

데이터 흐름:

Sensor → ESP32 → UART → Raspberry Pi → AI 처리 → 음성/알림 출력

---

## Features

* **물 감지 기반 이벤트 트리거**

  * 물이 감지되면 카메라 촬영 및 표정 분석 수행

* **조도 기반 화분 회전**

  * 일정 누적 조도 이상 시 화분 자동 회전

* **공기질 기반 환기 안내**

  * eCO2 수치 기반 환기 필요 여부 판단

* **TTS 음성 안내**

  * 상황에 맞는 음성 메시지 출력

* **Push 알림 전송**

  * 보호자에게 상태 알림 전송

* **프라이버시 보호 설계**

  * 물 이벤트 발생 시에만 카메라 활성화
  * 물리 스위치 및 LED 상태 표시

---

##  Key Points

* 이벤트 기반 시스템 설계 (Polling 최소화)
* ESP32 ↔ Raspberry Pi 간 UART 통신 구조 설계
* 센서 데이터 기반 의사결정 로직 구현
* 경량 CNN 기반 표정 인식 모델 적용
* 사용자 프라이버시를 고려한 카메라 제어 방식 설계

---

##  Hardware Configuration

* ESP32 DevKitC V4
* Raspberry Pi 5
* Raspberry Pi Camera Module V2
* BH1750 (조도 센서)
* CCS811 (공기질 센서)
* YL-83 (수분 센서)
* DS3231 (RTC 모듈)
* Stepper Motor (화분 회전)

---

##  Data Flow

1. ESP32가 센서 데이터를 주기적으로 수집
2. 특정 조건 만족 시 이벤트 발생

   * waterDetected
   * needVent
   * needSunlight
3. UART를 통해 Raspberry Pi로 전송
4. Raspberry Pi에서 이벤트에 따른 동작 수행

   * 카메라 촬영
   * 표정 분석
   * TTS 출력
   * Push 알림 전송

---

##  AI Model

* 표정 인식 모델

  * 클래스: Angry, Fear, Happy, Sad, Surprise, Neutral
  * 경량 CNN 구조 기반
  * 실시간 처리를 위해 최적화된 모델 사용

---

##  Results

* 센서 기반 이벤트 트리거 정상 동작
* 실시간 표정 인식 및 음성 안내 가능
* 프라이버시 고려 설계 적용
* 환경 변화에 따른 사용자 맞춤형 피드백 제공

---

##  How to Run

1. ESP32에 센서 코드 업로드
2. Raspberry Pi에서 서버 실행
3. UART 연결 확인 (/dev/ttyAMA1)
4. 시스템 실행

---

##  Demo

[영상 보기](./videos/smart_pot_demo.mp4)
---

##  Code

본 프로젝트의 전체 코드는 아래 팀 레포지토리에 정리되어 있다.

[https://github.com/kiseongpark/Capstone_design_final
](https://github.com/kiseongpark/Capstone_design_final)

### Contribution

본인은 센서 처리 및 Raspberry Pi 연동 구조를 중심으로 구현을 담당함.

- ESP32에서 센서 데이터 수집 및 이벤트 판단 로직 구현
- UART 기반으로 Raspberry Pi와 통신 구조 설계
- 물 감지 이벤트 발생 시 카메라 및 표정 인식 트리거 연결

또한 Raspberry Pi 측 코드의 구조를 모듈 단위로 분리하여 유지보수성을 개선.

### 주요 구현 파일

- `sensors.py`  
  → 센서 데이터 처리 및 이벤트 트리거 로직 구현

- `camera_control.py`  
  → 카메라 제어 및 촬영 트리거 처리

- `emotion.py`  
  → 표정 인식 모델 추론 및 결과 처리

- `notifier.py`  
  → TTS 출력 및 Push 알림 전송

- `main.py`  
  → 전체 시스템 흐름 제어

- `config.py`  
  → 센서 임계값 및 시스템 설정 관리

---

##  느낀 점

단순한 센서 시스템을 넘어서, 사용자와 상호작용하는 시스템을 설계하는 과정이 인상 깊었다.
특히 하드웨어와 소프트웨어를 함께 고려해야 하는 점에서 시스템 설계의 중요성을 느낄 수 있었다.

또한 프라이버시와 같은 실제 사용 환경의 문제를 고려하는 것이 기술 구현만큼 중요하다는 것을 경험했다.

---
