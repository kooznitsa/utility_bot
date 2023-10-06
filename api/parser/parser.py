from datetime import date, timedelta
import re
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup
from googletrans import Translator

from .helpers import DISTRICTS, HEADERS, MONTHS


class Page:
    def __init__(self, url):
        self.url = url + '?pismo=cyr'

    def get_urls(self):
        req = urlopen(Request(url=self.url, headers=HEADERS))
        soup = BeautifulSoup(req, 'html.parser')
        return soup.find_all('h2', {'class': 'entry-title'})


class Article:
    TRANSLATOR = Translator()

    def __init__(self, tag):
        self.url = tag.find('a')['href'] + '?pismo=cyr'

    @property
    def article(self):
        req = urlopen(Request(url=self.url, headers=HEADERS))
        return BeautifulSoup(req, 'html.parser')

    @property
    def container(self):
        return self.article.find('div', {'class': 'entry-content'})

    @property
    def title(self):
        return self.article.find('h1', {'class': 'entry-title'}).text

    @property
    def content(self):
        return [
            i.text for i in self.container.select('h5,ul,p:not(blockquote p)')
            if i.text not in ('Преузмите андроид апликацију.')
        ]

    @property
    def pub_date(self):
        day, month, year, _ = self.article.find('div', {'class': 'herald-date'}).text.split('.')
        return date(int(year), int(month), int(day))

    @staticmethod
    def get_deadline(pub_date, title):
        try:
            pattern = r'[0-9]{1,2}\.[ \n\t]' + f'({"|".join(MONTHS)})'
            day, month = re.search(pattern, title).group(0).split()
            return date(pub_date.year, MONTHS.index(month) + 1, int(day[:-1]))
        except AttributeError:
            try:
                pattern = r'(данас|сутра|прекосутра)'
                word = re.search(pattern, title).group(0)
                match word:
                    case 'данас': return pub_date
                    case 'сутра': return pub_date + timedelta(days=1)
                    case 'прекосутра': return pub_date + timedelta(days=2)
            except AttributeError:
                return pub_date + timedelta(days=7)

    def get_items(self):
        return {
            'url': self.url,
            'title': self.TRANSLATOR.translate(self.title, dest='ru').text,
            'content': self.TRANSLATOR.translate('\n'.join(self.content), dest='ru').text,
            'pub_date': self.pub_date,
            'deadline': self.get_deadline(self.pub_date, self.title)
        }

    def get_tags(self):
        tags = self.container.find('div', {'class': 'meta-tags'}).find_all('a')
        return [{'tag': tag.text} for tag in tags]

    def get_districts(self):
        tags = [i.get('tag') for i in self.get_tags()]
        districts = [{'district': 'Нови Сад'}]

        for word in [j for i in self.content for j in i.split()] + self.title.split() + tags:
            for start, full in DISTRICTS:
                if word.startswith(start):
                    districts.append({'district': full})
        return districts


if __name__ == '__main__':
    page = Page('https://gradskeinfo.rs/kategorija/servisne-info/')

    for i in page.get_urls():
        article = Article(i)
        print(article.get_items())
        print(article.get_tags())
        print(article.get_districts())
