# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tohomh import settings
from tohomh.items import TohomhItem, ContentItem
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import pymysql
import os


class TohomhPipeline(object):

    host = settings.MYSQL_HOST
    port = settings.MYSQL_PORT
    user = settings.MYSQL_USER
    password = settings.MYSQL_PASSWORD
    database = settings.MYSQL_DATABASE

    def process_item(self, item, spider):
        if isinstance(item, TohomhItem):
            cursor = self.db.cursor()
            is_sql = "select comic_url from comics where comic_url = %s"
            sql = "insert into comics (name, author, comic_url, comic_status, category) values (%s, %s, %s, %s, %s)"
            try:
                cursor.execute(is_sql, (item['comicUrl']))
                is_exist = cursor.fetchone()
                if is_exist:
                    print('已经存储过了...')
                else:
                    cursor.execute(sql, (item['name'], item['author'], item['comicUrl'], item['comicStatus'], item['category']))
                    self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
        elif isinstance(item, ContentItem):
            cursor = self.db.cursor()
            is_sql = "select url from contents where url = %s"
            sql = "insert into contents (comic_url, chapter, name, url) values (%s, %s, %s, %s)"
            try:
                cursor.execute(is_sql, (item['url']))
                is_exist = cursor.fetchone()
                if is_exist:
                    print('已经存储过了...')
                else:
                    cursor.execute(sql, (item['comicUrl'], item['chapter'], item['name'], item['url']))
                    self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
        return item

    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, charset="utf8")

    def close_spider(self, spider):
        self.db.close()


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        name = item['comicName']
        chapter = item['chapter']
        url = request.url
        file_name = os.path.join(name, chapter, url.split('/')[-1])
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        if isinstance(item, ContentItem):
            yield Request(item['url'], meta={'item': item})
