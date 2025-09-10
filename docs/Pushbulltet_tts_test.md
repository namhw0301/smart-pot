# Pushbullet+ttst 테스트
## 개요
Pushbullet API를 활용하여 물을 주면 보호자에게 메시지를 전송하도록 설계
메시지로 노인의 표정, 물 주기 여부를 전송

## 테스트 실행 결과

    ```python
    # -*- coding: utf-8 -*-
    import os
    from gtts import gTTS
    from playsound import playsound
    from pushbullet import Pushbullet
    
    # Pushbullet API Key
    pb = Pushbullet("o.1iA5k9LnOz6jyaneakU86VEnwHoWOHB9")  # 너의 API 키
    
    print("테스트용 수동 입력 대기 중...")
    
    while True:
        line = input("값을 입력하세요 (1 입력 시 알림 및 음성 출력): ").strip()
    
        if line == "1":
            message = "물이 감지되었습니다!"
    
            # Pushbullet 알림
            pb.push_note("스마트 화분 알림", message)
            print("Pushbullet 알림 전송됨!")
    
            # TTS 음성 출력
            tts = gTTS(text=message, lang='ko')
            tts.save("hello_kor.mp3")
            os.system("mpg321 hello_kor.mp3")
            print("음성 출력 완료!\n")
    
    ```

- 실행 결과
    <img width="2879" height="1694" alt="image" src="https://github.com/user-attachments/assets/26ed4f3a-abcf-489a-b6ec-6e27b0b3f6cc" />

    
<img width="648" height="1348" alt="image" src="https://github.com/user-attachments/assets/22aac902-9dbb-4a39-bc84-42c37567d7a4" />
    

https://github.com/user-attachments/assets/5c63b8c7-5696-4c87-a3f7-69c651dd26ae


    


    

## 기존의 Pushbullet API 코드 문제점

사전 구현 단계에서 보호자의 Pushbullet API Key를 미리 알아야 함+Pushbullet API Key가 수정될 시 새로 설정해야 함

해결책

- Flask 웹서버를 열어서 보호자의 Pushbullet API Key를 입력받도록 한다.
    - Flask: 라즈베리파이에서 실행되는 웹서버. 웹 브라우저(예: 보호자 스마트폰)에서 접속한 사용자가 HTML 페이지를 보고 API Key 같은 데이터를 입력할 수 있게 만들어주는 도구
<img width="659" height="228" alt="image" src="https://github.com/user-attachments/assets/97bb1547-55e2-4251-96ee-a0707060750a" />
- 코드(Flask 서버 코드)
    
- 

```python
from flask import Flask, request, render_template
import json
import os

app = Flask(__name__)

CONFIG_PATH = "config.json"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api_key = request.form["api_key"].strip()

        with open(CONFIG_PATH, "w") as f:
            json.dump({"pushbullet_api_key": api_key}, f)

        return "✅ API Key 저장 완료! 이제 스마트 화분 알림이 가능합니다."

    return render_template("form.html")

@app.route("/check", methods=["GET"])
def check():
    if not os.path.exists(CONFIG_PATH):
        return "❌ 아직 API Key가 저장되지 않았습니다."

    with open(CONFIG_PATH, "r") as f:
        key = json.load(f).get("pushbullet_api_key", "")
        if key:
            return f"✅ 저장된 API Key: {key[:10]}...(생략)"
        else:
            return "❌ API Key가 비어있습니다."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

- 코드(HTML 폼 파일)
```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>스마트 화분 Push 설정</title>
  </head>
  <body>
    <h2>Pushbullet API Key 입력</h2>
    <form method="POST">
      <input type="text" name="api_key" placeholder="o.xxxxxxxxxxxxx" style="width: 300px;"><br><br>
      <button type="submit">저장하기</button>
    </form>
  </body>
</html>
```

-    
    - 실행 결과
    <img width="2876" height="622" alt="image" src="https://github.com/user-attachments/assets/261ec2bf-40fb-48bd-a123-c4fae1122f58" />
    <img width="2869" height="852" alt="image" src="https://github.com/user-attachments/assets/de53f917-d042-41da-83ce-725a81d5b953" />
    <img width="2849" height="510" alt="image" src="https://github.com/user-attachments/assets/dd2080a9-a4cc-462f-8bd3-a0739c8f3541" />
    <img width="1275" height="134" alt="image" src="https://github.com/user-attachments/assets/d83e8c85-255a-497c-9158-0e52e400319c" />
        
    - flask에서 api key를 받아서 pb 설정한 코드
        
        ```python
        # -*- coding: utf-8 -*-
        import os
        import json
        from gtts import gTTS
        from playsound import playsound
        from pushbullet import Pushbullet
        
        # config.json에서 API Key 불러오기
        CONFIG_PATH = "config.json"
        
        if not os.path.exists(CONFIG_PATH):
            print("❌ config.json 파일이 존재하지 않습니다. Flask 웹페이지에서 API Key를 먼저 입력해주세요.")
            exit(1)
        
        with open(CONFIG_PATH, "r") as f:
            api_key = json.load(f).get("pushbullet_api_key", "").strip()
        
        if not api_key:
            print("❌ config.json에 API Key가 비어 있습니다.")
            exit(1)
        
        pb = Pushbullet(api_key)  # JSON에서 불러온 API 키로 Pushbullet 객체 생성
        
        print("테스트용 수동 입력 대기 중...")
        
        while True:
            line = input("값을 입력하세요 (1 입력 시 알림 및 음성 출력): ").strip()
        
            if line == "1":
                message = "물이 감지되었습니다!"
        
                # Pushbullet 알림
                pb.push_note("스마트 화분 알림", message)
                print("Pushbullet 알림 전송됨!")
        
                # TTS 음성 출력
                tts = gTTS(text=message, lang='ko')
                tts.save("hello_kor.mp3")
                os.system("mpg321 hello_kor.mp3")
                print("음성 출력 완료!\n")
        
        ```
        
    
    부팅 시 라즈베리파이의 IP를 우리에게 전송 → 전달받은 IP를 통해 flask 서버 주소를 보호자에게 전달 → 보호자가 서버에 들어가서 Pushbullet API Key 입력
