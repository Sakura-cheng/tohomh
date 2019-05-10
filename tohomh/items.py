# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TohomhItem(scrapy.Item):
    # 漫画名
    name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 漫画地址
    comicUrl = scrapy.Field()
    # 状态
    comicStatus = scrapy.Field()
    # 漫画题材
    category = scrapy.Field()
    # 简介
    desc = scrapy.Field()


class ContentItem(scrapy.Item):
    # 漫画地址
    comicUrl = scrapy.Field()
    # 章节
    chapter = scrapy.Field()
    # 图片名
    name = scrapy.Field()
    # 图片地址
    url = scrapy.Field()
