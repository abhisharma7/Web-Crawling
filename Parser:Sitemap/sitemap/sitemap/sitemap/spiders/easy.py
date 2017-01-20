# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import SitemapSpider
from scrapy.selector import HtmlXPathSelector
import sys
import re
import time
import datetime
import bs4

class EasySpider(SitemapSpider):
	
	name = 'easy'
	TAG_REMOVE = re.compile(r'<[^>]+>')

    	allowed_domains = ["example.com"]
    	sitemap_urls = ["https://www.example.com"]
	rule_list = ["//h1/text()","url","H1 Tag"]

        def parse(self,response):

                url_found = response.url
                page_source = response.body
                soup = bs4.BeautifulSoup(page_source)
		rule_list = ["//h1/text()","xpath","H1 Tag"]
                for values in self.rule_list:
                     
                	rule = values[1]
                  	rule_type = values[2]
                    	attribute_name = values[3]

             	if rule_type == "xpath":
                	self.xpath_parse(response,rule,attribute_name,url_found)
          	else:
                    	pass

        def xpath_parse(self,response,rule,attribute_names,url_found):

                attribute_name =  attribute_names.encode('utf-8').strip()
                hxs = HtmlXPathSelector(response)
                try:
                        attribute_list = hxs.xpath(rule).extract()[0]
                        try:
                                attribute_value = ''.join(str(e) for e in attribute_list)
                        except Exception as error:
                                attribute_value = attribute_list
                except Exception as error:
                        attribute_value = "not found"
                attribute_value = attribute_value.strip()
                attribute_values = self.TAG_REMOVE.sub('',attribute_value)
                attribute_value = attribute_values.encode('utf-8').strip()
                attribute_values = attribute_value.strip("\n")
                attribute_value = attribute_values.rstrip()
                attribute_value = attribute_value.strip()

                if attribute_value == "not found":
                        pass
                else:
                        print attribute_name
                        print attribute_value
