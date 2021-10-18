import requests
from bs4 import BeautifulSoup
import os

#開資料夾
if not os.path.exists('./pttGossip'):
    os.mkdir('./pttGossip')

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
headers = {
    'User-Agent' : user_agent
}

landing_page_url = 'https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html'
ask_over18_url = 'https://www.ptt.cc/ask/over18'
ptt_gossiping_url = 'https://www.ptt.cc/bbs/Gossiping/index.html'

#create session
ss = requests.session()
# print(ss.cookies)

#get form data
res_landing_page_url = ss.get(landing_page_url, headers=headers)
soup_landing_page = BeautifulSoup(res_landing_page_url.text,'html.parser')
# print(ss.cookies)

data = dict()
key_1 = soup_landing_page.select('input')[0]['name']
value_1 = soup_landing_page.select('input')[0]['value']
data[key_1] = value_1

key_2 = soup_landing_page.select('button')[0]['name']
value_2 = soup_landing_page.select('button')[0]['value']
data[key_2] = value_2
# print(data)

res_ask_over18_url = ss.post(ask_over18_url, headers=headers, data=data)

pages = input('你想要查詢多少Ptt的頁數?')
for i in range(0,int(pages)+1):
    # 利用ss.get進入網頁
    res = ss.get(ptt_gossiping_url, headers=headers)
    gossip_soup = BeautifulSoup(res.text, 'html.parser')
    titles = gossip_soup.select('div[class=title]')
    for title_soup in titles:
        try:
            title = title_soup.select('a')[0].text
            print(title)
            article_url = 'https://www.ptt.cc' + title_soup.select('a')[0]['href']
            print(article_url)
            res_article = ss.get(article_url, headers=headers)
            article_soup = BeautifulSoup(res_article.text, 'html.parser')
            article_content = article_soup.select('div[id="main-content"]')[0].text.split('※ 發信站')[0]
            push_soups = article_soup.select('div[class="push"]')
            push_up = 0
            push_down = 0
            for push_soup in push_soups:
                # print(push_soup.text)
                if '推' in push_soup.text:
                    push_up += 1
                if '噓' in push_soup.text:
                    push_down += 1
            article_content += '\n---split--- \n'
            article_content += '推的總數: {} \n'.format(push_up)
            article_content += '噓的總數: {} \n'.format(push_down)
            article_content += '分數: {} \n'.format(push_up - push_down)
            # print(article_content)

            # 在最下面顯示ptt作者相關資訊
            article_info_list = article_soup.select('div[class="article-metaline"] span')
            # print(article_infos[0])
            # for article_info in article_infos:
            #     # print(article_info)
            #     article_content += article_info.text + '\n'
            for n, info in enumerate(article_info_list):
                if (n+1)%6 == 2:
                    author = info.text
                if (n+1)%6 == 4:
                    title = info.text
                if (n+1)%6 == 0:
                    datetime = info.text
            article_content += '作者: {}\n'.format(author)
            article_content += '標題: {}\n'.format(title)
            article_content += '時間: {}\n'.format(datetime)
            # print(article_content)
            try:
                with open('./pttGossip/{}.txt'.format(title), 'w', encoding='utf=8') as f:
                    f.write(article_content)
            except FileNotFoundError:
                title = title.replace('/', '_')
                with open('./pttGossip/{}.txt'.format(title), 'w', encoding='utf=8') as f:
                    f.write(article_content)
            except OSError:
                title = title.replace(':', '-').replace('?', ' ').replace('<<', '_').replace('>>', '_')
                with open('./pttGossip/{}.txt'.format(title), 'w', encoding='utf=8') as f:
                    f.write(article_content)
        except IndexError:
            print('===')
            print(title_soup.text.strip())
            print('===')

    the_previous_button = gossip_soup.select('a[class="btn wide"]')[1]['href']
    the_previous_url = 'https://www.ptt.cc' + the_previous_button
    #print(the_prebious_url)
    ptt_gossiping_url = the_previous_url







