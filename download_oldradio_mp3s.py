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
    return (show, downloaded)


def Store_file(db, filename):
    """ Write the database (db) to filename as a JSON format file.
    """
    with open(filename, 'w') as fp:
        json.dump(db, fp)


def file_exists(ep, db):
    downloaded = db[ep[1]][ep[2]][ep[3]][ep[0]]
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
             full url of episode)
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


def download_random_episode(db):
    """ Load JSON database of recordings.
    Pick a random file and if it has not been downloaded, download it.
    Wait a random amount of time before downloading another file.
    Use sys module to monitor for CTRL-C and exit cleanly.
    """

    # 3 pick a random file and download it
    def random_show(db):
        month = random.choice(list(db.keys()))
        day = random.choice(list(db[month].keys()))
        year = random.choice(list(db[month][day].keys()))
        ep = random.choice(list(db[month][day][year].keys()))
        full_url = 'http://www.oldradioworld.com' + ep
        return (ep, month, day, year, full_url)

    episode = random_show(db)

    # choose a valid file sequentially if need be
    if file_exists(episode, db):
        for m in db:
            for d in db[m]:
                for y in db[m][d]:
                    for e in db[m][d][y]:
                        if not file_exists((db[m][d][y].key(), m, d, y, ''), db):
                            full_url = 'http://www.oldradioworld.com' + db[m][d][y].key()
                            episode = (db[m][d][y].key(), m, d, y, full_url)
                            break

    # are we done with all files?
    if file_exists(episode, db):
        return False

    ep = episode
    full_url = ep[-1]

    print(full_url)

    destination_path = prepare_download_dir(episode)
    if destination_path:
        media = wget.download(full_url, destination_path)
        db[ep[1]][ep[2]][ep[3]][ep[0]] = True

    return True


if __name__ == '__main__':
    database = 'oldradioworld_mp3s.json'

    print('Recovering database file: {}'.format(database))
    db = Recover_file(database)

    print('Downloading...')
    while download_random_episode(db):
        print('Done.')

        print('Storing file')
        Store_file(db, database)
        print('Next file...')
        pause = random.randint(30,120)
        print('Pausing for {} seconds.'.format(pause))
        sleep(pause)

    print(time.now())

