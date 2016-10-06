""" Take the input file and organize media files by category.
"""

from time import sleep
from datetime import datetime as time
import json
import re
from dateutil.parser import parse
from datetime import datetime
import copy
import random
import wget
import os

from build_database2 import extract_title
from build_database2 import extract_embeded_datestr


def Recover_file(filename):
    """ Load the specified file relative to the current working directory.
    Filename is assumed to be a JSON formatted file.
    Return the data as a dictionary.
    """
    with open(filename) as fp:
        json_dict = json.load(fp)
    return json_dict


def stats(db):
    show = 0
    downloaded = 0
    for k, v in db.items():
        show += 1
        if v:
            downloaded += 1
    return [show, downloaded]


def Store_file(db, filename):
    """ Write the database (db) to filename as a JSON format file.
    """
    with open(filename, 'w') as fp:
        json.dump(db, fp)


def file_exists(filename):
    """ look for file in directory tree
    """
    downloaded = os.path.isfile(filename)
    if downloaded:
        return True
    return False


def combine_paths(args):
    """ args is a list of directory names
    """
    path = ''
    for directory in args:
        path += directory
        path += '/'
    return path


def validate_path(path_list):
    """ path is a list of directories.
    validate and if neccessary create path
    """
    full_path = combine_paths(path_list)
    if os.path.isdir(full_path):
        return True
    else:
        # attempt to create path
        partial_path = []
        for element in path_list:
            partial_path.append(element)
            test = combine_paths(partial_path)
            if not os.path.isdir(test):
                os.mkdir(test)

    if os.path.isdir(full_path):
        return True
    return False


def prepare_download_dir(episode):
    """ episode is expected to be a tuple of 
            (episode name,
             month digit,
             day digit,
             year digit,
             full_url)
    This function needs to check for existance of destination
    directory and create it if necessary.
    """
    ep = episode
    root_dir = os.getcwd()
    media_root = 'media'
    month_dir = str(ep[1])
    day_dir = str(ep[2])
    year_dir = str(ep[3])

    desired_path = [root_dir, media_root, month_dir, day_dir, year_dir]

    destination = combine_paths(desired_path)

    validate_path(desired_path)

    if os.path.isdir(destination):
        return destination
    return False


def download_episodes(shows, shows_db_filename, dates):
    """ Load JSON database of recordings.
        download all episodes
    """

    episodes = list(shows.keys())

    for ep in episodes:
        full_url = 'http://www.oldradioworld.com' + ep
        print(full_url)
        showname = extract_title(ep)
        print(showname)
        date = extract_embeded_datestr(showname)
        print(date)
        epi_tuple = (ep, date.month, date.day, date.year, full_url)
        print(epi_tuple)
        destination_path = prepare_download_dir(epi_tuple)
        print(destination_path)
        if shows[ep]:  # has episode been downloaded?
            Print('Downloaded')
        else:
            if file_exists(destination_path):
                shows[ep] = True
            else:
                # get the file
                if destination_path:
                    media = wget.download(full_url, destination_path)
                    shows[ep] = True
                    print('Storing file')
                    Store_file(shows, shows_db_filename)
                    print('Next file...')
                    pause = random.randint(5,30)
                    print('Pausing for {} seconds.'.format(pause))
                    sleep(pause)

    return True


if __name__ == '__main__':
    show_database = 'oldradioworld_mp3s_shows.json'
    date_database = 'oldradioworld_mp3s_dates.json'

    print('Recovering show database file: {}'.format(show_database))
    sh_db = Recover_file(show_database)
    print('Recovering dates database file: {}'.format(date_database))
    dt_db = Recover_file(date_database)
    #print('Database stats: {} files, {} downloaded'.format(stats(sh_db)))
    print('Downloading...')
    download_episodes(sh_db, show_database, dt_db)

    print(time.now())

