# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import re
from scrapy.exceptions import DropItem
from sqlalchemy import exc as sqlalchemy_exc


class ScrapPipeline(object):
    def process_item(self, item, spider):
        return item


class SqlAlchemyPipeline(object):

    def __init__(self):
        self.zid_seen = set()

    def process_item(self, item, spider):
        if item['zid'] in self.zud_seen:
            raise DropItem('Duplicate listing found %s' % item['zid'])
        elif re.search('AuthRequired', item['link']):
            raise DropItem('Unauthorized listing found %s' % item['zid'])
        #  TODO: add item to database here

