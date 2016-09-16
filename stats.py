"""
	Take the input file and count the number of each entry type.
	"""

from time import sleep
from datetime import datetime as time
import requests
from lxml import html
import json
from pprint import pprint as pprint


def Recover_file(filename):
	with open(filename) as fp:
	    json_dict = json.load(fp)
	return json_dict


def Main():
	file = '/home/conrad/Programming_Code/Python/oldradioworld/2016-09-15 21:43:50.333220.json'
	result = Recover_file(file)
	pprint(result, indent=4)


if __name__ == '__main__':
	Main()
