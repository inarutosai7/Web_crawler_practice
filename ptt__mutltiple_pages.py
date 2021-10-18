import requests
from bs4 import BeautifulSoup

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
            title = titleSoup.select('a')
            print(title[0].text)
            print('https://www.ptt.cc' + title[0]['href'])
            print('===')
        except IndexError:
            print(titleSoup.text.strip())
            print('===')

    the_previous_button = soup.select('a[class="btn wide"]')[1]['href']
    the_previous_url = 'https://www.ptt.cc' + the_previous_button
    #print(the_prebious_url)
    url = the_previous_url