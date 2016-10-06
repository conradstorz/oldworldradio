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
    What remains before the extension is then normalized with
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
    MP3 URLs are added to the dictionary along with a flag indicating that the file has not been downloaded yet.
    """
    database = {}
    result = Recover_file(filename)
    for k, v in result.items():
        if k.endswith('.mp3'):
            database[k] = False  # Flag for status of download
    return database


def extract_embeded_datestr(string):
    """ Takes an input string and scans it for yalid date strings.
    The first valid string found is returned as a datetime object.
    If no date is found then a predictable default date is returned.
    """
    DEFAULT = parse('1936-07-25', yearfirst=True)
    DADS_BDAY = parse('1936-07-25 12:34:56', yearfirst=True)
    elements = string.split()
    for e in elements:
        try:
            date = parse(e, yearfirst=True, fuzzy=False, default=DEFAULT)
        except ValueError as e:
                date = DEFAULT        
        if date != DEFAULT:
            break

    if date.year > 1999:  # fix 2 digit date being reported as 20xx
        date = date.replace(year=date.year - 100)

    if date == DEFAULT:
        date = DADS_BDAY

    return date


def Build_an_mp3_database(file):

    dictionary_of_shows = build_dictionary_from(file)

    showname_dict = {}
    for k in list(dictionary_of_shows.keys()):
        show_name = extract_title(k)
        showname_dict[show_name] = extract_embeded_datestr(show_name).strftime("%A, %d. %B %Y %I:%M%p")

    print('{} items in database.'.format(len(dictionary_of_shows)))
    finished_time = time.now()
    print(finished_time)
    sleep(1)
    filename = '{}shows.json'.format(finished_time)
    with open(filename, 'w') as fp:
        json.dump(dictionary_of_shows, fp)
    print('Results saved as {}'.format(filename))
    sleep(1)
    filename = '{}dates.json'.format(finished_time)
    with open(filename, 'w') as fp:
        json.dump(showname_dict, fp)
    print('Results saved as {}'.format(filename))

    return



if __name__ == '__main__':
    file = '/home/conrad/Programming_Code/Python/oldradioworld/2016-09-15 21:43:50.333220.json'
    print('Processing: {}'.format(file))
    Build_an_mp3_database(file)

