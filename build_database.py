""" Take the input file and organize media files by category.
"""

from time import sleep
from datetime import datetime as time
import json
import re
from dateutil.parser import parse
from datetime import datetime
import copy


def Recover_file(filename):
    """ Load the specified file relative to the current working directory.
    Filename is assumed to be a JSON formatted file.
    Return the data as a dictionary.
    """
    with open(filename) as fp:
        json_dict = json.load(fp)
    return json_dict


def extract_title(string):
    """ Assumes that the given string is formatted like a URL.
    The end of the URL is assumed to have a "." extension.
    What remains after the extension is then normalized with
    space characters as word seperators.
    """
    splt_str = string.split('/')
    last_item = splt_str[-1]
    chop_ext = last_item.split('.')
    show_name = chop_ext[0]
    parts = show_name.split('_')
    reconstructed = ' '.join(parts)
    return reconstructed


def build_dictionary_from(filename):
    """ Filename offered is assumed to be JSON formatted.
    The file is further assumed to contain one (1) entry
     for each URL file found while crawling the website.
    The URL is relative to the website and incomplete.
    The VALUE stored along with the URL is the website page where the URL was found.
    Non-MP3 URLs are discarded.
    MP3 URLs are combined into lists based on what website page they were found on.
    The new dictionary contains one (1) entry for each refering page and the VALUE
     is the list of MP3 URLs found at that page.
    """
    database = {}
    result = Recover_file(filename)
    for k, v in result.items():
        if k.endswith('.mp3'):
            if v in database and k != None:
                l = database[v]
                l.append(k)  # NOTE: appending directly to the dictionary would cause errors.
                database[v] = l
            else:
                if k != None:
                    database[v] = [k]
    return database


def extract_embeded_datestr(string):
    """ Takes an input string and scans it for yalid date strings.
    The first valid string found is returned as a datetime object.
    If no date is found then a prdictable default date is returned.
    """
    DEFAULT = parse('1936-07-25', yearfirst=True)
    DADS_BDAY = parse('1936-07-25 12:34:56', yearfirst=True)
    elements = string.split()
    for e in elements:
        try:
            date = parse(e, yearfirst=True, fuzzy=False, default=DEFAULT)
        except ValueError, e:
                date = DEFAULT        
        if date != DEFAULT:
            break
    if date == DEFAULT:
        date = DADS_BDAY
    return date

   
def Run():
    file = '/home/conrad/Programming_Code/Python/oldradioworld/2016-09-15 21:43:50.333220.json'
    shows = 0
    episodes = 0
    earliest_date = parse('2016-1-1')
    latest_date = parse('1900-1-1')
    dictionary_of_shows = build_dictionary_from(file)
    sd = dictionary_of_shows 
    for k in sd:
        shows += 1
        show_name = extract_title(k)
        print('{:4d} MP3s in {} "{}"'.format(len(sd[k]), show_name, k))
        for episode in sd[k]:
            episodes += 1
            air_date = extract_embeded_datestr(episode)
            if air_date > latest_date:
                latest_date = copy.copy(air_date)
            if air_date < earliest_date:
                earliest_date = copy.copy(air_date)
            print('{}: {}'.format(show_name, air_date))
    print('{} total shows'.format(shows))
    print('{} total episodes'.format(episodes))
    print('Earliest air date: {}'.format(earliest_date))
    print('Last air date: {}'.format(latest_date))

if __name__ == '__main__':
    Run()
