# FMS - 자동화 시스템 관리 프로그램 UI 개선 프로젝트
오픈소스 기초 프로젝트, 자동화 시스템 관리 프로그램 UI 개선 프로젝트 Repo.

### 프로젝트 소개
본 프로젝트는 25학년도 1학기 오픈소스기초프로젝트 과목에서 시작한 프로젝트입니다. 
자율 주행이라는 주제에 맞춰, 자율 주행 로봇의 관제시스템의 개발을 기획하게 되었습니다. 
일반적인 관제시스템의 배치는 매우 복잡하고 어려워 다루기 어려운 경우가 많습니다. 
이에 저희는 관제시스템의 UI/UX를 개선하여 비전공자도 쉽게 로봇을 다룰 수 있도록 하는 관제 시스템 개발을 기획하였습니다.

이 사이트에서는
로봇의 동선과 로봇의 상태를 한 눈에 확인할 수 있고,
명령어를 통해 로봇에게 명령을 내릴 수 있습니다.
또한 로봇이 어떤 명령을 받고 어떤 작업을 했는지 로그를 통해 확인가능합니다.
추가로 위험요소를 경고 알림을 통해 알립니다.
![mainpage](https://github.com/user-attachments/assets/de93598f-bc43-409f-a7ed-a06e79d62f48)


# 설치 방법
front-end
```
$cd front-end
$npm install
```
package*.json 의존성 파일에 의한 자동 설치


back-end
```
$pip install -r requirements.txt
```
https://www.mongodb.com/try/download/community
설치 후 MongoDB compass 를 이용하거나 터미널로 MongoDB서버를 실행

# 의존성

✅**BackEnd**
```bash
Flask 3.1.0  
flask-cors 6.0.0  
Flask-SQLAlchemy 3.1.1  
SQLAlchemy 2.0.36  
flask-socketio 5.5.1  
pymongo 4.13.0  
```

✅**FrontEnd**
```
axios 1.9.0  
chart.js 3.9.1  
inject 1.0.0-beta2  
pinia 3.0.3  
provide 0.1.3  
socket.io-client 4.8.1  
vue 3.5.13  
vue-chartjs 4.1.2  
vue-i18n 9.14.4  
vue-router 4.5.1  

```

# 실행 방법
```
MongoDB 설치 후 터미널에서 다음을 실행.
--
$pip install -r requirements.txt
$python3 main.py
--open new terminal--
$python3 api_main.py
--open new terminal--
$cd front-end
$npm i
$npm run dev
```

# License
```
MIT License

Copyright (c) 2025 S3C1

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

# Contributor
|문영민(팀장)|이창형|이강민|양시경|
|------|---|---|---|
| [originap](https://github.com/ORIGINAP)              |      [zxczxczczz](https://github.com/zxczxczczz)         |   [DaveLEE777](https://github.com/DaveLEE777)      | [mountaindew93](https://github.com/mountaindew93)|
