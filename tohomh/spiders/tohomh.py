import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from tohomh.items import TohomhItem, ContentItem


class Tohomh(scrapy.Spider):
    name = 'tohomh'
    allowed_domains = ['tohomh123.com']
    base_url = 'https://www.tohomh123.com'
    start_url = 'https://www.tohomh123.com/f-1------hits--1.html'

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
        try:
            item['category'] = content.find('span', {'class': 'ticai'}).a.get_text()
        except Exception as e:
            item['category'] = ''
            print(e)
        item['desc'] = content.find('p', {'class': 'content'}).get_text()
        yield item

        chapters = content.find('ul', {'class': 'view-win-list detail-list-select'}).find_all('li')
        for chapter in chapters:
            chapter_name = chapter.a.get_text()
            chapter_url = self.base_url + chapter.a['href']
            yield Request(chapter_url, self.get_content, meta={'comicUrl': response.url, 'chapter': chapter_name})

    def get_content(self, response):
        content = BeautifulSoup(response.text, 'lxml')
        url = content.find_all('script', {'type': 'text/javascript'})[-1].get_text().split(';')[-3].split("'")[-2][:-8]
        format = content.find_all('script', {'type': 'text/javascript'})[-1].get_text().split(';')[-3].split("'")[-2][-4:]
        count = int(content.find_all('script', {'type': 'text/javascript'})[-1].get_text().split(';')[5].split(' = ')[-1])

        for i in range(count):
            item = ContentItem()
            item['comicUrl'] = response.meta['comicUrl']
            item['chapter'] = response.url.split('/')[-1].split('.')[0] + '_' + response.meta['chapter']
            item['url'] = url + str(i).zfill(4) + format
            item['name'] = item['comicUrl'].split('/')[-2] + '_' + item['chapter'] + '_' + str(i)
            yield item
