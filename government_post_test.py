import requests
from bs4 import BeautifulSoup
url = 'https://web.pcc.gov.tw/tps/pss/tender.do?searchMode=common&searchType=advance'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
headers = {
    'User-Agent' : user_agent
}
dataStr = """method:search
searchMethod:true
searchTarget:ATM
orgName:fadsfasd
orgId: 
hid_1:1
tenderName:asdfadsfsa
tenderId: 
tenderStatus:5,6,20,28
tenderWay: 
awardAnnounceStartDate:110/08/07
awardAnnounceEndDate:110/08/07
proctrgCate: 
tenderRange: 
minBudget: 
maxBudget: 
item:adsfasd
hid_2:1
gottenVendorName:sadfsdf
gottenVendorId: 
hid_3:1
submitVendorName: 
submitVendorId: 
location: 
execLocationArea: 
priorityCate: 
isReConstruct: 
btnQuery:查詢"""
data = dict()

# for r in dataStr.split("\n"):
#     key = r.split(":")[0]
#     value = r.split(":")[1]
#     data[key] = value

print(data)
data = {i.split(':')[0] : i.split(':')[1] for i in dataStr.split('\n') }


res = requests.post(url, headers=headers, data=data)
print(res.text)
soup = BeautifulSoup(res.text,'html.parser')

