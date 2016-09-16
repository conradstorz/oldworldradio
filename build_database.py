"""
	Take the input file and organize media files by category.
	"""

from time import sleep
from datetime import datetime as time
import json


def Recover_file(filename):
	with open(filename) as fp:
	    json_dict = json.load(fp)
	return json_dict


def Main():
	database = {}
	file = '/home/conrad/Programming_Code/Python/oldradioworld/2016-09-15 21:43:50.333220.json'
	result = Recover_file(file)
	for k, v in result.items():
		#print()
		#print(database)
		#print(k, v)
		if k.endswith('.mp3'):
			if v in database and k != None:
				l = database[v]
				l.append(k)
				#print(l)
				#print('append', l)
				database[v] = l
			else:
				if k != None:
					database[v] = []
					#print(k)
					database[v].append(k)
					#print(database[v])
	print(len(database))
	print(len(database.keys()))
	for k in database:
		splt_str = k.split('/')
		last_item = splt_str[-1]
		chop_ext = last_item.split('.')
		show_name = chop_ext[0]
		print('{:4d} MP3s in {}'.format(len(database[k]), show_name))
		#print(database[k])


if __name__ == '__main__':
	Main()
