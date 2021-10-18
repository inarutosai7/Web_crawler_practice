import requests
import json
import os
from urllib import request
if not os.path.exists('./dcardPhoto'):
    os.mkdir('./dcardPhoto')

url = 'https://www.dcard.tw/service/api/v2/forums/photography/posts?limit=30&before=236646456'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
headers = {
    'User-Agent' : user_agent
}

# Dcard json page
res = requests.get(url, headers=headers)
#print(res.text)
#each object(Dict) in it is an article
#id: article url
#title: title
jsonData = json.loads(res.text) #return list/dict

# for r in jsonData:
#     print(r)

# print(jsonData[0].keys())
# for k in jsonData[0]:
#     print(k)

for articleDict in jsonData:
    article_url = 'https://www.dcard.tw/f/photography/p/' + str(articleDict['id'])
    article_title = articleDict['title']

    print(article_title)
    print(article_url)
    for imgs in articleDict['mediaMeta']:
        print('\t',imgs['url'])
        #image_path = './dcardPhoto/{}.{}'.format(article_title, imgs['url'].split('.')[-1])
        image_path = './dcardPhoto/{}.{}'.format(article_title, imgs['url'].split('/')[-1])
        #request.urlretrieve(imgs['url'],image_path)
        img_content = requests.get(imgs['url'], headers=headers).content
        with open(image_path,'wb') as f :
            f.write(img_content)
    print('============')




