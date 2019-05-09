import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from tohomh.items import TohomhItem


class Tohomh(scrapy.Spider):
    name = 'tohomh'
    allowed_domians = ['tohomh123.com']
    base_url = 'https://www.tohomh123.com'
    start_url = 'https://www.tohomh123.com/f-1------hits--362.html'

    def start_requests(self):
        yield Request(self.start_url, self.parse)

    def parse(self, response):
        content = BeautifulSoup(response.text, 'lxml')

        comics_li = content.find('ul', {"class": "mh-list"}).find_all('li')
        for li in comics_li:
            comic_url = self.base_url + li.div.a['href']
            yield Request(comic_url, self.get_item)

        next_url = content.find('div', {"class": "page-pagination"}).ul.find_all('li')[-1].a['href']
        next_url = self.base_url + next_url
        yield Request(next_url, self.parse)

    def get_item(self, response):
        content = BeautifulSoup(response.text, 'lxml')
        item = TohomhItem()
        item['name'] = str(content.find('h1').get_text())
        item['author'] = str(content.find('p', {'class': 'subtitle'}).get_text().split('：')[-1])
        item['comicUrl'] = response.url
        item['comicStatus'] = content.find('span', {'class': 'block'}).span.get_text()
        item['category'] = content.find('span', {'class': 'ticai'}).a.get_text()
        item['desc'] = content.find('p', {'class': 'content'}).get_text()
        return item
