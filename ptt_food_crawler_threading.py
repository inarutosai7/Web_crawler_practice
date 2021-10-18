import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def request_the_url(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    headers = {
        'User-Agent': user_agent
    }
    res = requests.get(url, headers=headers)
    article_soup = BeautifulSoup(res.text, 'html.parser')
    return article_soup


def main():
    start = time.time()

    #台北地區 -%E5%8F%B0%E5%8C%97  新北地區 - %E6%96%B0%E5%8C%97 宜蘭地區 - %E5%AE%9C%E8%98%AD
    location = '%E6%96%B0%E5%8C%97'
    page = 1
    url = 'https://www.ptt.cc/bbs/Food/search?page={}&q={}'.format(page, location)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    headers = {
        'User-Agent': user_agent
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 尋找最舊的那一頁
    the_oldest_page = int(soup.select('a[class="btn wide"]')[0]['href'].split('page=')[1].split('&')[0])
    print(the_oldest_page)
    # print(type(the_oldest_page))
    # run this file for 5 times
    data = []
    data_nums = 0
    for page in range(2,100):
        if page % 100 == 0:
            time.sleep(10)
            pass
        else:
            pass

        # soup = request_the_url(url)
        with ThreadPoolExecutor(max_workers=10) as executor:
            article_soups = []
            article_soup = executor.submit(request_the_url, url)
            article_soups.append(article_soup)
            for soup in as_completed(article_soups):
                soup = soup.result()
        # res = requests.get(url, headers=headers)
        # soup = BeautifulSoup(res.text, 'html.parser')
        print('現在是第 {} 頁'.format(page))
        # print(res.text)
        titles = soup.select('div[class=title]')
        for titleSoup in titles:
            try:
                # ptt 標題
                title = titleSoup.select('a')[0].text

                # ptt 網址
                article_url = 'https://www.ptt.cc' + titleSoup.select('a')[0]['href']
                with ThreadPoolExecutor(max_workers=10) as executor:
                    article_soups = []
                    article_soup = executor.submit(request_the_url, article_url)
                    article_soups.append(article_soup)
                    for soup in as_completed(article_soups):
                        article_soup = soup.result()
                # res_article = requests.get(article_url, headers=headers)
                # article_soup = BeautifulSoup(res_article.text, 'html.parser')

                # ptt 作者、標題、時間相關資訊
                article_info_list = article_soup.select('div[class="article-metaline"] span')
                for n, info in enumerate(article_info_list):
                    if (n + 1) % 6 == 2:
                        author = info.text
                    if (n + 1) % 6 == 4:
                        title = info.text
                    if (n + 1) % 6 == 0:
                        datetime = info.text

                # ptt 內文
                article_content_soup = article_soup.select('div[id="main-content"]')[0]
                for tag in ['div', 'span']:
                    for i in article_content_soup.select(tag):
                        i.extract()
                article_content = article_content_soup.text

                # ptt 分數
                push_soups = article_soup.select('div[class="push"]')
                push_up = 0
                push_down = 0
                for push_soup in push_soups:
                    # print(push_soup.text)
                    if '推' in push_soup.text:
                        push_up += 1
                    if '噓' in push_soup.text:
                        push_down += 1
                article_score = push_up - push_down
                # 要存入Mongo DB
                Mongodb_data = {
                    '文章標題': title,
                    '作者': author,
                    '發文時間': datetime,
                    '文章網址': article_url,
                    '文章內文': article_content,
                    '文章分數': article_score,
                }

                print(title)

            except IndexError:
                print(titleSoup.text.strip())
                print('===')

        # ptt 上一頁的網址
        the_previous_url = 'https://www.ptt.cc/bbs/Food/search?page={}&q={}'.format(page, location)
        # 將 url 換成上一頁的 url
        url = the_previous_url
    end = time.time()
    print("總共花費的時間 : {} 秒".format(end-start))

if __name__ == '__main__':
    main()