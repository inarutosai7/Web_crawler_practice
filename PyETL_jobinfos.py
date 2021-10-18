import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
headers = {
    'User-Agent' : user_agent
}


page = 4
infos_data = []
for page in range(1, page+1):
    print(page)
    data_job_url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E8%B3%87%E6%96%99%E5%B7%A5%E7%A8%8B%E5%B8%AB&expansionType=job&order=1&asc=0&page={}&mode=s&jobsource=2018indexpoc'.format(str(page))
    ss = requests.session()

    #get the first page
    res_job = ss.get(data_job_url, headers=headers)
    soup_job_url = BeautifulSoup(res_job.text,'html.parser')
    # print(soup_job_url)


    titles = soup_job_url.select('h2[class="b-tit"]')
    # print(titles)

    for titleSoup in titles:
        try:
            #Need API to get json
            article_url = 'https:'+titleSoup.select('a')[0]['href']
            article_id = article_url.split('job/')[1].split('?')[0]
            article_data_url = 'https://www.104.com.tw/job/ajax/content/{}'.format(article_id)
            headers['Referer'] = 'https://www.104.com.tw/job/77u0t?jobsource=jolist_c_relevance'
            res_article = ss.get(article_data_url, headers=headers)


            # job infromation
            jsonData = json.loads(res_article.text)
            # print(article_url)
            opening = jsonData['data']['header']['jobName']
            company = jsonData['data']['header']['custName']
            region_location = jsonData['data']['jobDetail']['addressRegion']
            job_content = jsonData['data']['jobDetail']['jobDescription'].replace('\r\n',' ').replace('\n',' ').replace('\n\n',' ')
            job_other_content = jsonData['data']['condition']['other']
            salary = jsonData['data']['jobDetail']['salary']
            language = jsonData['data']['condition']['language'][0]['language']
            ability = jsonData['data']['condition']['language'][0]['ability']
            specialtys = jsonData['data']['condition']['specialty']
            specialty = []
            for i in specialtys:
                specialty.append(str.lower(i['description']))

            # read the programming key word textfile
            with open('./programming.txt', 'r', encoding='utf=8') as f:
                programming = f.read()
            # print(programming)
            # ability word_count
            key_word = [str.lower(ability_key_word) for ability_key_word in programming.split('\n')]
            key_word_count = {}
            for i in key_word:
                if i in specialty:
                    if i in key_word_count:
                        key_word_count[i] += 1
                    else:
                        key_word_count[i] = 1
                else:
                    key_word_count[i] = 0

            # print(key_word_count)
            job_info = ''
            job_info = '職缺 @claire {}'.format(opening)+'\$claire'
            job_info += '公司 @claire {}'.format(company)+'\$claire'
            job_info += '地區 @claire {}'.format(region_location)+'\$claire'
            job_info += '網址 @claire {}'.format(article_url)+'\$claire'
            job_info += '工作內容 @claire {}'.format(job_content) + '\$claire'
            job_info += '語文條件 @claire {}'.format(language)+ '\$claire'
            job_info += '語文程度 @claire {}'.format(ability) + '\$claire'
            job_info += '薪資 @claire {}'.format(salary)
            # job_info += '其他條件 : {}'.format(job_other_content)

            # 整理成適合存進csv的格式
            data = [i.split(' @claire ')[1] for i in job_info.split('\$claire')]+ list(key_word_count.values())
            # print(data)
            infos_data.append(data)

        except IndexError:
            pass
    # print(key_word)
    # print(key_word_count.values())
columns = [i.split(' @claire ')[0] for i in job_info.split('\$claire')] + key_word
# print(infos_data)
# print(columns)
#存入csv
df = pd.DataFrame(data=infos_data, columns=columns)
# print(df)
df.to_csv('./job_info.csv', index=0, header=columns, encoding='utf-8-sig')

