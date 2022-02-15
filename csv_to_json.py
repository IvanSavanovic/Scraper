import csv
import json

articles = []
with open('data.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i != 0:
            article = {
                'id': row[0],
                'link': row[1],
                'pre_title': row[2],
                'title': row[3],
                'subtitle': row[4],
                'author': row[5],
                'datetime': row[6],
                'categories': row[7],
                'tags': row[8],
                'avg_rating': row[9],
                'num_votes': row[10],
                'views': row[11],
                'encoding': row[12],
                'text': row[13],
                'comments': row[14]
            }
            articles.append(article)

with open('data.json', 'w') as f:
    json.dump(articles, f)
