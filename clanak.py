import csv

import bs4
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}

csv_file = open('data.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(
    [
        'id',
        'link',
        'pre_title',
        'title',
        'subtitle',
        'author',
        'datetime',
        'categories',
        'tags',
        'avg_rating',
        'num_votes',
        'views',
        'encoding',
        'text',
        'comments'
    ]
)

with open('linkovi.txt') as f:
    for id_, link in enumerate(f.readlines()):
        r = requests.get(link[:-1], headers=headers)
        if r.status_code == requests.codes.ok:
            encoding = r.encoding
            soup = bs4.BeautifulSoup(r.text, 'html.parser')

            region_content = soup.find('div', class_='region region-content')

            pre_title = region_content.find_all('div', class_='content')[0].find('div', class_='field-item even').text
            title = soup.title.text[:-16]
            subtitle = region_content.find(
                'div',
                class_='field field-name-field-podnaslov field-type-text-long field-label-hidden'
            )

            if not subtitle:
                subtitle = ''
            else:
                subtitle = subtitle.find_all('div')[-1].text

            author = region_content.find(
                lambda t: t.name == 'a' and t.attrs.get('href', '').startswith('/autori/'))
            if author:
                author = author.text
            else:
                author = 'Unknown'
            datetime = region_content.find(
                lambda t: t.name == 'span' and t.attrs.get('property', '') == 'dc:date dc:created'
            ).attrs['content']

            categories = soup.find(
                'div',
                class_='field field-name-field-tags field-type-taxonomy-term-reference field-label-inline clearfix'
            ).contents[1].find_all('a')
            categories = [a.text for a in categories]

            tags = region_content.find(
                'div',
                class_='field field-name-field-tag field-type-taxonomy-term-reference field-label-inline clearfix'
            )
            if tags:
                tags = tags.contents[1].find_all('a')
                tags = [a.text for a in tags]
            else:
                tags = []

            vote_form = region_content.find('form', class_='fivestar-widget')
            average_rating = vote_form.find('span', class_='average-rating')
            if average_rating:
                average_rating = average_rating.find('span').text
                total_votes = vote_form.find('span', class_='total-votes').find('span').text
            else:
                average_rating = 0
                total_votes = 0

            views = region_content.find('ul', class_='links inline').find_all('span')[-1].text[:-8]

            ps = region_content.find_all(lambda t: t.name == 'p' and t.text != '')
            text = '\n\n'.join([p.text.strip() for p in ps])

            comment_divs = region_content.find('div', id='comments')
            comments = []

            if comment_divs:
                comment_divs = comment_divs.find_all('div', typeof='sioc:Post sioct:Comment')
                for cd in comment_divs:
                    username_span = cd.find('div', class_='submitted').find('span', class_='username')
                    username_date = username_span.next_sibling
                    username = username_span.text
                    comment_text = cd.find('div', class_='content').find('div', class_='field-item even').text
                    comment = '{}:{}:{}###'.format(username_date, username, comment_text)
                    comments.append(comment)
            else:
                comments = ''

        else:
            r.raise_for_status()

        csv_writer.writerow(
            [
                id_,
                link,
                pre_title,
                title,
                subtitle,
                author,
                datetime,
                ','.join(categories),
                ','.join(tags),
                average_rating,
                total_votes,
                views,
                encoding,
                text,
                comments
            ]
        )
