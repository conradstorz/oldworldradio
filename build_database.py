"""
    Take the input file and organize media files by category.
    """

from time import sleep
from datetime import datetime as time
import json
import re
from dateutil.parser import parse
from datetime import datetime


def Recover_file(filename):
    with open(filename) as fp:
        json_dict = json.load(fp)
    return json_dict


def extract_artist_name(s):
    splt_str = s.split('/')
    last_item = splt_str[-1]
    chop_ext = last_item.split('.')
    show_name = chop_ext[0]
    parts = show_name.split('_')
    reconstructed = ' '.join(parts)
    return reconstructed


def build_database_from(filename):
    database = {}
    result = Recover_file(filename)
    for k, v in result.items():
        if k.endswith('.mp3'):
            if v in database and k != None:
                l = database[v]
                l.append(k)
                database[v] = l
            else:
                if k != None:
                    database[v] = [k]
    return database


def parse_date(name):
    #Finds any 6 or 8 digit date with D/M/Y unseparated
    #or separated by '-' or '/'
    date = re.search("([\d][-/]?){6}|([\d][-/]?){8}", name)
    if date:
        print(date.group(0))
        date = parse(date.group(0), yearfirst=True)
        #Dateutil bug sometimes returns 21st century. Force 20th 
        if date.year > 1999:
            date = date.replace(year = date.year - 100)
    else:
        date = None
    return date

def parse_dates_in_list(filenames):
    """
    Goes through a list of file names and creates a dict
    containing a datetime and the corresponding filename for
    every file with a date in the title.
    """
    datedict = {}
    #print(filenames)
    for name in filenames:
        for part in name.split():
            try:
                date = parse(name, yearfirst=True)
            except ValueError, e:
                date = None
            datedict[name] = date       

    return datedict



def Main():
    file = '/home/conrad/Programming_Code/Python/oldradioworld/2016-09-15 21:43:50.333220.json'
    database_of_shows = build_database_from(file)
    sd = database_of_shows  
    for k in sd:
        show_name = extract_artist_name(k)
        #print('{:4d} MP3s in {} "{}"'.format(len(sd[k]), show_name, k))
        for item in sd[k]:
            #print(item.split())
            #air_date = extract_embeded_datestr(item)
            print(parse_dates_in_list([item]))


if __name__ == '__main__':
    Main()
