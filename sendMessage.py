import requests  #1 요청을 하기 위한 모듈
import pprint    #5 요청받은 response 값을 보기 쉽게 변환해주는 모듈 
#9 decouple 모듈을 사용하기 위해서 bash에서 $ pip install python-decouple, $ python -m pip install --upgrade pip를 입력한다.
from decouple import config # .env에 있는 값을 불러오는 모듈


base_url = 'https://api.telegram.org'
#2 bot 은 나중에 다시 넣을겁니다.
toke = config('API_TOKEN')  # .env에 있는 정보를 받아와라
chat_id = config('CHAT_ID')
text = '디커플 실행한다'

api_url = f'{base_url}/bot{toke}/sendMessage?chat_id={chat_id}&text={text}'  #3 이쪽으로 요청을 보내면 챗봇에 명령이 갑니다.

response = requests.get(api_url)  #4 200 잘 실행 되었을 때, 404 잘 안되었을 때 ... json타입으로 받는다.

pprint.pprint(response.json())  #6 json타입의 정보를 보기 쉽게 변환해주는 함수

#7 토큰값과 챗아이디를 노출시키면 보안상 문제가 있기 때문에, 두 정보를 숨겨놓고 싶다. .env라는 이름의 새파일을 생성하자.
#8 .env는 환경변수라고 해서 깃허브로 올리거나 공개를 했을 때 아무도 모르도록 하는 설정이다.

#10 이제 챗봇에 받은 메시지를 분석하여 대응하는 행동을 하기 위해 app.py를 새로 만든다.
