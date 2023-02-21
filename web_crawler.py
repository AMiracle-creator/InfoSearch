import requests
from fake_useragent import UserAgent

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

urls = []
page = 7
while page < 15:
    pages_response = requests.get(f'https://www.liveinternet.ru/rating/today.tsv?;page={page}', headers=headers)
    urls.append(list(map(lambda item: 'http://' + item.split("\t")[1].replace("/", ""), pages_response.text.split("\n")[1:30])))
    page += 1


link_number = 1
for item in urls:
    for link in item:
        ua = UserAgent()

        headers = {
            'User-Agent': ua.random
        }

        try:
            html = requests.get(link, headers=headers).text
        except Exception:
            continue

        with open(f'выкачка_{link_number}', 'w', encoding='utf-8') as file:
            file.write(html)

        with open('index.txt', 'a', encoding='utf-8') as file:
            file.writelines(f'{link_number}   {link}\n')

        link_number += 1


