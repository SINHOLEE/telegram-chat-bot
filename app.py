# 11 app.py를 생성하고 플라스크 공식 홈페이지에서 기초정보를 가져온다.
from flask import Flask, request
from decouple import config # 21 토큰값을 받기 위해
import pprint #30 임포트 합시다
import requests #34 sendMeassge를 실행하기 위해 필요한 모듈 /  request는 flask에 있는 모듈, requests는 따로 있는 모듈

app = Flask(__name__)

# 상수변수
API_TOKEN = config('API_TOKEN') #22 환경변수에서 받아와라
NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')

@app.route('/')
def hello():
    return 'Hello'


# 13 앞으로 챗봇에서 받은 메시지를 모두 나에게 받아줘 라는 API가 있다. setwebhook 이라는 텔레그램API를 사용하자
# 14 하지만 우리가 가지고 있는 로컬 도메인으로는 못온다 그러므로 임시 도메인을 생성한다. https://ngrok.com/ ngrok에 깃허브로 가입하고, 다운받는다
# 15 다운받은 ngrok.exe 파일을 app.py와 sendMessage.py가 있는 폴더에 가져온다.
# 16 terminal -> app.py가 실행되고 있는 상태에서 +버튼 옆에 창을 나눈 후 ngrok에 3connect 에 있는 ./ngrok authtoken 38ci2H6UBF4DApZd3ojyB_4qgpGLnNTvQx3oJUnucYo이 정보를 입력
# 17 bash에 $ ./ngrok.exe http 5000라고 입력한 후 https의 주소를 컨트롤 클릭하면 로컬호스트의 주소를 임시로 https://45c26e45.ngrok.io/ 여기다가 보여줄게 라는 명령이 실행된다.
# 18 그렇기 때문에 임시로 받은 주소는 app.py를 껏다가 키면 바뀌므로 앵간해선 냅둬야 한다.
# 19 즉 이제 외부에서도 우리의 로컬호스트로 접속할 수 있다.


@app.route('/greeting/<name>')
def greeting(name):
    return f'hello {name}'


@app.route(f'/{API_TOKEN}', methods=['POST']) # 20 토큰값을 꺼내기 위해 디커플 모듈을 실행한다. / #23 토큰을 불러온다. 
#25 methods=['POST'] 이건 아이디나 중요한 정보가 바로 나오지 못하게 가려주세요? post 로보내주세요? 질문 다시하자    
def telegram() :
    #27 이제 메시지 정보를 받아보자
    from_telegram = request.get_json()
    # print(from_telegram)
    #29 보기 힘들기 때문에 pprint로 받자. 1 import
    # pprint.pprint(from_telegram)
    #30 사용자가 메시지를 보냇을경우에만 받읍시다 

    if from_telegram.get('message') is not None :     #32 from_telegram은 딕셔너리 형식으로 그 안에 키값 message로 접근하는 방법은 크게 [] 혹은 .get두방법이 있다. 
         #31 우리가 원하는 로직을 쌓아가자.             # 전자는 값이 없으면 오류, 후자는 오류 없이 값을 갖고온다.
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text') # 사용자가 보낸 메시지
        print('chat_id : ', chat_id)
        print('text : ', text)
        
        # 34 첫 네글자가 '/한영 '일 때 
        if text[0:4] == '/한영 ' :
            # 35 요청에 대한 정보를 저장하라... 잘 몰라
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET, # 36 trailing comma 혹시라도 추가할 수 도 있으니까.
            }

            data = {
                'source' : 'ko',
                'target' : 'en',
                'text' : text[4:] # 36 번역이후의 문자열을 대상으로 번역
            }

            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data) # 37 왜 post인지는 아직 모르겠다.
            pprint.pprint(papago_res.json()) # 38 papago_res.json()은 딕셔너리 형식으로 받아오라는 뜻
            text = papago_res.json().get('message').get('result').get('translatedText')
        
        #39 영한으로 번역하고 싶다면 
        if text[0:4] == '/영한 ' :
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET, 
            }

            data = {
                'source' : 'en',
                'target' : 'ko',
                'text' : text[4:] 
            }

            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            pprint.pprint(papago_res.json())
            text = papago_res.json().get('message').get('result').get('translatedText')


        #######sendMessage################
        base_url = 'https://api.telegram.org'
        chat_id = config('CHAT_ID')
        api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}'  #3 이쪽으로 요청을 보내면 챗봇에 명령이 갑니다.


        response = requests.get(api_url) # 33 리퀘스츠는 괄호의 url을 입력해주세요!
        
    #28 그리고 메시지를 보내면 메시지의 내용이 from_telegram에 저장된다.    
    return '', 200 #24 응답은 공백이고, 200이라는 값을 보내줄게

# 26 set??


if __name__ == "__main__": # 12 앱을 실행했을 때 다른 파일에서 모듈로 사용되지 않을때만 작동하라 / 디버그 모듈을 설치해야 했다.
    app.run(debug=True)