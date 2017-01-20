#!/usr/bin/python

# Created by Abhishek Sharma

## Script is created for learning purpose, crawling any website without website owner permission is a copyright violation.

import re
import six
import scrapy
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import SitemapSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import Spider
from scrapy.http import Request, XmlResponse
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
from scrapy.utils.gz import gunzip, is_gzipped

class EasySpider(SitemapSpider):

    name = 'sitemapxml'
    allowed_domains = ['amazon.com']
    sitemap_urls = ['https://www.amazon.com/robots.txt']
    rule = "/product/"
    count = 0
    other = 0

    def start_requests(self):
        for url in self.sitemap_urls:
            yield Request(url, self.parse_sitemap)

 
    def parse_sitemap(self,response):
        
        if response.url.endswith('/robots.txt'):
            for url in sitemap_urls_from_robots(response.text, base_url=response.url):
                yield Request(url, callback=self.parse_sitemap)

        else:
            body = self._get_sitemap_body(response)
            if body is None:
                logger.warning("Ignoring invalid sitemap: %(response)s",
                               {'response': response}, extra={'spider': self})
                return

            s = Sitemap(body)
            if s.type == 'sitemapindex':
                for loc in iterloc(s, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self.parse_sitemap)

            elif s.type == 'urlset':
                for loc in iterloc(s):
		    print loc
                    if loc.count(self.rule):
			self.count = self.count + 1
		    else:
			self.other = self.other + 1
	        print "Total Rule Matched: ",self.count
		print "Total Other Count: ", self.other


def regex(x):
    if isinstance(x, six.string_types):
        return re.compile(x)
    return x


def iterloc(it, alt=False):
    for d in it:
        yield d['loc']

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and 'alternate' in d:
            for l in d['alternate']:
                yield l

