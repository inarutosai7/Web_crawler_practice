import requests
from bs4 import BeautifulSoup


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
headers = {
    'User-Agent' : user_agent
}

url = 'http://ec2-13-114-140-26.ap-northeast-1.compute.amazonaws.com/practice/tfb103'

#create session
ss = requests.session()
res_hidden_val = ss.get(url, headers=headers)
hidden_val_soup = BeautifulSoup(res_hidden_val.text,'html.parser')
_hidden_info = hidden_val_soup.select('input[type="hidden"]')

# print(_hidden_info[0]['name'])


data = {
     'pwd' : 'Test another solution',
    _hidden_info[0]['name'] : _hidden_info[0]['value']
}

# print(data)
res = ss.post(url, headers=headers, data=data)
print(res.text )
