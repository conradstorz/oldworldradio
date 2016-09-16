""" This module attempts to traverses a website url.
	The first step is to locate links (href) on the given url.
	These links are placed into a list.

	The second step is traversing this list for links to other pages.
	These pages are visited and traveresed as in the first step.

	When all links have been identified and traveresed
	 the work of this module is done.
	"""

from time import sleep
from datetime import datetime as time
import requests
from lxml import html
import json
from random import randint

traverse = {}
total_media_files = 0
website = 'http://www.oldradioworld.com'


def extract_links(webpage):
	"""
		If a webpage specification is valid, return a list of links (href) on the page.
		If not then return the webpage string itself
		"""
	sleep(1)
	try:
		current_page = requests.get(webpage)
	except:
		print('"{}" could not be processed.'.format(webpage))
		return webpage
	content = html.fromstring(current_page.content)
	links = content.xpath('//a/@href')
	return links

def crawl(webpage):
	"""
		Attempt to crawl the webpage and enter it into the dictionary.
		After finding all the links on the page, attempt to crawl each of them.
		"""
	global total_media_files
	traverse[webpage] = 'Self reference'
	sleep(1)
	links = extract_links(webpage)
	if links == webpage:
		fixed_url = website + webpage
		print('Trying {}'.format(fixed_url))
		links = extract_links(fixed_url)
		webpage = fixed_url

	print('{} contains {} links.'.format(webpage, len(links)))
	traverse[webpage] = links

	for link in links:
		if link.endswith('.php'):
			if link == webpage or link in traverse:
				#print('Found a circular reference')
				traverse[link] = 'Self reference'
			else:
				sleep(randint(1, 5))
				traverse[link] = crawl(link)
		else:
			traverse[link] = webpage
			total_media_files += 1
	return links


def Main():
	"""
		Process the given website for links.
		Save the results into a JSON formatted file.
		"""
	sleep(1)
	print(time.now())
	print('Begin crawling {}'.format(website))
	result = crawl(website)
	print('Finished.')
	finished_time = time.now()
	print(finished_time)
	sleep(1)
	filename = '{}.json'.format(finished_time)
	with open(filename, 'w') as fp:
	    json.dump(traverse, fp)
	print('Results saved as {}'.format(filename))
	print(total_media_files)
	return 0

if __name__ == '__main__':
	Main()
