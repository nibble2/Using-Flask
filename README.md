&#128668; Flask 프레임 워크를 활용하여 API 작성하기
===

### 0. Flask 프레임 워크란 ?
~~~
파이썬으로 작성된 마이크로 웹 프레임 워크

라이브러리 vs 프레임워크?
라이브러리는 필요한 모듈을 내가 가져와 작성하는 것이고 프레임워크는 필요한 코드를 내가 작성하는 것
그래서 제어역전(Inversion Of Control)이라고 불린다.
~~~

### 1. Flask 기본 폴더 구조
- folder name
> static
    + style.css
> templates
    + index.html
> app.py

### 2. app.py 작성하기
~~~
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
   return 'This is Home!'

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
~~~

### 2. html 파일과 css 파일 분리
~~~
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
~~~

### 4. Study List
- [x] Flask 사용해보기
- [x] Flask를 이용한 API 작성
- [x] Flask + Pymongo 함께 사용하기
- [x] Postman 사용해보

#### 5. 발생한 에러 문구
raise ValueError('update only works with $ operators') ValueError: update only works with $ operators

> db 업데이트 할때 pymongo update 문을 오타나서 $이 아닌 #으로 입력

raise TypeError(f'Object of type {o.__class__.__name__} ' TypeError: Object of type UpdateResult is not JSON serializable