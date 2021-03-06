import datetime
import pandas as pandas
import argparse

from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

today_date = datetime.date.today()
date_of_creation = 1920
age_of_the_winery = today_date.year - date_of_creation

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file_name', default='wine.xlsx', help='Имя файла ')
args = parser.parse_args()

wines_from_file = pandas.read_excel(
    args.file_name,
    na_values=['N/A', 'NA'], keep_default_na=False
).to_dict(orient='records')

all_wines = defaultdict(list)
for wine in wines_from_file:
    category = wine.get('Категория')
    all_wines[category].append(wine)

rendered_page = template.render(
    age_of_the_winery=age_of_the_winery,
    wines=all_wines,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
