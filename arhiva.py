import bs4
import requests

base_url = 'https://www.zadarskilist.hr'
section_url = 'https://www.zadarskilist.hr/sekcije'
sections = {
    'dogadjaji': 259,
    'kronika': 25,
    'zadar': 138,
    'zupanija': 66,
    'kultura': 16,
    'sport': 59,
    'zabava': 11,
    'prilozi': 3,
    'magazin': 4,
    'fotogalerije': 3
}
start = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}

links = []
for section, end in sections.items():
    for i in range(start, end + 1):
        articles_url = '{}/{}?page={}'.format(section_url, section, i)
        r = requests.get(articles_url, headers=headers)

        if r.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(r.text, 'html.parser')
            view_content = soup.find_all('div', class_='view-content')[1]

            field_contents = soup.find_all('span', class_='field-content')

            if i == 0:
                links.append('{}{}'.format(base_url, view_content.find('a').attrs['href']))
                field_contents = field_contents[9:]

            for field_content in field_contents:
                a = field_content.find('a')
                if a:
                    links.append('{}{}'.format(base_url, a.attrs['href']))
        else:
            r.raise_for_status()

with open('linkovi.txt', 'w') as f:
    f.writelines([link + '\n' for link in links])
