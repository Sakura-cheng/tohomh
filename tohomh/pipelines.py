# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tohomh import settings
from tohomh.items import TohomhItem, ContentItem
import pymysql


class TohomhPipeline(object):

    host = settings.MYSQL_HOST
    port = settings.MYSQL_PORT
    user = settings.MYSQL_USER
    password = settings.MYSQL_PASSWORD
    db = settings.MYSQL_DB
    db = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset="utf8")

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
