# https://freelearning.tistory.com/308

# 데이터 tradingview에서 받아서 데모 돌려보기

import yaml
import hmac
import hashlib
import httplib2
import base64
import simplejson as json
import time

PRIVATE_INFO_PATH = 'info/private.yaml'
PUBLIC_INFO_PATH = 'info/public.yaml'

PRIVATE = {}
PUBLIC = {}

# parse
with open(PRIVATE_INFO_PATH) as f:
	PRIVATE = yaml.load(f, Loader=yaml.FullLoader)
with open(PUBLIC_INFO_PATH) as f:
	PUBLIC = yaml.load(f, Loader=yaml.FullLoader)


# 환율 분봉이랑 김프 분봉 가지고 실제 얻을 수 있는 수익 시뮬 하기.
# 김프 사이에 환율이 바뀔 수도 있어서 그럼.
# 파동 디텍션은 단순한 알고리즘 이평이라던지 stochastic같은 것 중 가장 잘 되는거 써 보기.
# 백테스팅 플랫폼 이용해야 하나?
# 다양한 코인 별 김프 다 계산해서 최고 최저로 판단
# https://iri-kang.tistory.com/3


def get_encoded_payload(payload):
  payload[u'nonce'] = int(time.time()*1000)

  dumped_json = json.dumps(payload).encode()
  encoded_json = base64.b64encode(dumped_json)
  return encoded_json


def get_signature(encoded_payload, secret_key):
  signature = hmac.new(secret_key.upper().encode(), encoded_payload, hashlib.sha512);
  return signature.hexdigest()


def post_response(url, payload):
  encoded_payload = get_encoded_payload(payload)
  headers = {
    'Content-type': 'application/json',
    'X-COINONE-PAYLOAD': encoded_payload,
    'X-COINONE-SIGNATURE': get_signature(encoded_payload, PRIVATE['COINONE-API-SECRET'])
  }
  http = httplib2.Http()
  response, content = http.request(url, 'POST', headers=headers, body=encoded_payload)
  return content

def get_response(url, payload):
  encoded_payload = get_encoded_payload(payload)
# #   headers = {
# #     'Content-type': 'application/json',
# #     'X-COINONE-PAYLOAD': encoded_payload,
# #     'X-COINONE-SIGNATURE': get_signature(encoded_payload, PRIVATE['COINONE-API-SECRET'])
# #   }
#   headers = {}
  http = httplib2.Http()
  response, content = http.request(url, 'GET', body=encoded_payload)
  return content

# coinone private post

# url = 'https://api.coinone.co.kr/v2/account/balance/'
# payload = {
# 	"access_token": PRIVATE['COINONE-API-KEY'],
# }
# response = post_response(url, payload)
# content = json.loads(response)

# print(content)

# coinone ticker

url = 'https://api.coinone.co.kr/ticker/?currency=all'
payload = {
	#"access_token": PRIVATE['COINONE-API-KEY'],
	"currency": "eth"
}
response = get_response(url, payload)
content = json.loads(response)

coinone_coins = list(content.keys())
coinone_coins.remove('result')
coinone_coins.remove('errorCode')
coinone_coins.remove('timestamp')

print(coinone_coins)

# 우선 api 다 콜 해서 공통 코인 별 김프를 다 계산할 수 있게 하기
# 공통 코인 : ticker 별로 매치되는거 찾기
# 저점이어도 손해는 봐야 할 듯
# 주식 틱봉은 못 받아오나?

# coinone orderbook

url = 'https://api.coinone.co.kr/orderbook/?currency=eth'
payload = {
	
}
response = get_response(url, payload)
content = json.loads(response)

print(content)