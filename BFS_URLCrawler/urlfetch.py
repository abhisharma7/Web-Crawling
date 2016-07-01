#!/usr/bin/python

import urllib
import urlparse
import os
import sys
import subprocess as sp
from bs4 import BeautifulSoup
import nltk
import MySQLdb

class UrlCrawler:

	def urlcrawler_execution(self,url):

		urls = [url]
		visited = [url]

		while len(urls) > 0:
	
			try:
				htmltext = urllib.urlopen(urls[0]).read()
			except Exception as error:
				print error
				print urls[0]
	
			soup = BeautifulSoup(htmltext)
			urls.pop(0)
			print len(urls)

			for tag in soup.findAll('a', href=True):
				tag['href'] = urlparse.urljoin(url,tag['href'])
				if url in tag['href'] and tag['href'] not in visited:
					urls.append(tag['href'])
					visited.append(tag['href'])			
			print visited

		total_url=len(visited)
		
		if total_url == 0:
			return "Something Wrong"
		else:
# Fetching Images as Json.

			for url in visited:
        		        url_images = {'URL': [], 'Images': []}
	        	        url_description = {'URL': [], 'Description' : []}
				url_images = ['URL'].append(url)
				url_desciption = ['URL'].append(url)
				try:
					htmltext = urllib.urlopen(url)
				except Exception as error:
					pass
				soup = BeautifulSoup(htmltext)
				for imagetag in soup.find_all('img'):
					try:
						imagetag['src'] = urlparse.urljoin(url,imagetag['src'].strip())
						url_images['Images'].append(imagetag['src'])
					except Exception as error:
						pass
				print url_images
			
# Fetching Text as Json.
				for script in soup(["script", "style"]):
    					script.extract()    # rip it out
				text = soup.get_text()
				lines = (line.strip() for line in text.splitlines())
				chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
				text = '\n'.join(chunk for chunk in chunks if chunk)
				url_description['Description'].append(text)
				print url_description

			return "Done"

# Pass URL as parameter.
url = sys.argv[1]

# Class Object
urlcrawler = UrlCrawler()

request = urlcrawler.urlcrawler_execution(request_id, url)

if request == "Something Wrong":
	print "Failed"
else:
        print "Done"



