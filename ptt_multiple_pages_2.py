import requests
from bs4 import BeautifulSoup
import os

#開資料夾
if not os.path.exists('./pttMovie'):
    os.mkdir('./pttMovie')




url = 'https://www.ptt.cc/bbs/movie/index.html'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
headers = {
    'User-Agent' : user_agent
}


# run this file for 5 times
for i in range(0,5):
    res = requests.get(url, headers=headers)
    print(i)
    # print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    # titles = soup.select('a')#return list
    titles = soup.select('div[class=title]')
    for titleSoup in titles:
        try:
            # print(title)
            title = titleSoup.select('a')[0].text
            article_url = 'https://www.ptt.cc' + titleSoup.select('a')[0]['href']
            res_article = requests.get(article_url, headers=headers)
            # 用BeautiflSoup才能使用select
            soup_article = BeautifulSoup(res_article.text, 'html.parser')
            #article_content = soup_article.select('div[id="main-content"]')[0].text.split('※ 發信站')[0]
            article_content_soup = soup_article.select('div[id="main-content"]')[0]
            #for i in article_content_soup.select('div'):
            #   i.extract()
            #for i in article_content_soup.select('span'):
            #    i.extract()
            for tag in ['div','span']:
                for i in article_content_soup.select(tag):
                    i.extract()
            article_content = article_content_soup.text
            print(title)
            print(article_url)
            try:
                with open('./pttMovie/{}.txt'.format(title),'w',encoding='utf=8') as f:
                    f.write(article_content)
            except FileNotFoundError:
                title = title.replace('/', '_')
                with open('./pttMovie/{}.txt'.format(title), 'w', encoding='utf=8') as f:
                    f.write(article_content)
            except OSError:
                title = title.replace(':','-').replace('?',' ').replace('<<','_').replace('>>','_')
                with open('./pttMovie/{}.txt'.format(title), 'w', encoding='utf=8') as f:
                    f.write(article_content)


        except IndexError:
            print('===')
            print(titleSoup.text.strip())
            print('===')


    the_previous_button = soup.select('a[class="btn wide"]')[1]['href']
    the_previous_url = 'https://www.ptt.cc' + the_previous_button
    #print(the_prebious_url)
    url = the_previous_url