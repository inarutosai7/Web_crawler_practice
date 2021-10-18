import requests
from bs4 import BeautifulSoup


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
headers = {
    'User-Agent' : user_agent
}

landing_page_url = 'https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html'
ask_over18_url = 'https://www.ptt.cc/ask/over18'
ptt_gossiping = 'https://www.ptt.cc/bbs/Gossiping/index.html'

#create session
ss = requests.session()
print(ss.cookies)

#get form data
res_landing_page_url = ss.get(landing_page_url, headers=headers)
soup_landing_page = BeautifulSoup(res_landing_page_url.text,'html.parser')
print(ss.cookies)

data = dict()
key_1 = soup_landing_page.select('input')[0]['name']
value_1 = soup_landing_page.select('input')[0]['value']
data[key_1] = value_1

key_2 = soup_landing_page.select('button')[0]['name']
value_2 = soup_landing_page.select('button')[0]['value']
data[key_2] = value_2
print(data)

res_ask_over18_url = ss.post(ask_over18_url, headers=headers, data=data)
print(ss.cookies)

res = ss.get(ptt_gossiping, headers=headers)
print(res.text)




