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

from colorama import init, Fore, Back, Style
init(autoreset=True)

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
    files_downloaded = 0
    files_prev_downloaded = 0
    episodes = list(shows.keys())

    for ep in episodes:
        full_url = 'http://www.oldradioworld.com' + ep
        print(Back.GREEN + '{} files downloaded this round and {} files previously downloaded.'.format(files_downloaded, files_prev_downloaded))
        print(Style.RESET_ALL)
        print(full_url)
        showname = extract_title(ep)
        print(Back.BLUE + showname)
        date = extract_embeded_datestr(showname)
        print(Fore.BLUE + Back.WHITE + str(date))
        epi_tuple = (ep, date.month, date.day, date.year, full_url)
        print(epi_tuple)
        destination_path = prepare_download_dir(epi_tuple)
        print(destination_path)
        if shows[ep] or file_exists(destination_path):  # has episode been downloaded?
            files_prev_downloaded += 1
            shows[ep] = True  # failsafe
            print(Fore.RED + Back.WHITE + 'Downloaded')
        else:
            # get the file
            if destination_path:
                try:
                    media = wget.download(full_url, destination_path)
                except Exception as e:
                    pass
                shows[ep] = True
                print(Back.GREEN + 'Storing file')
                files_downloaded += 1
                Store_file(shows, shows_db_filename)
                pause = random.randint(5,10)
                print(Style.DIM + 'Pausing for {} seconds.'.format(pause))
                sleep(pause)

    return True

UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWERCASE = UPPERCASE.lower()

def find_camelcase(db):
    """ Given a database of keys which are strings,
    scan keys for strings that contain CamelCase.
    Build new string with spaces instead e.g."Camel Case"
    place string into a list and return the expanded string
    along with the original string in a list of tuples [(expanded, original)]
    """
    names = []
    for name in db:
        showname = extract_title(name)
        Fixedname = ''
        for indx, char in enumerate(showname):
            if indx > 0:
                if char in UPPERCASE:
                    if showname[indx - 1] in LOWERCASE:
                        Fixedname += ' '
            Fixedname += char
        if showname != Fixedname:
            names.append((Fixedname, name))
    return names


if __name__ == '__main__':
    """
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
    """

    #load database
    show_database = 'oldradioworld_mp3s_shows.json'
    date_database = 'oldradioworld_mp3s_dates.json'

    print('Recovering show database file: {}'.format(show_database))
    sh_db = Recover_file(show_database)
    print('Recovering dates database file: {}'.format(date_database))
    dt_db = Recover_file(date_database)
    stat = stats(sh_db)
    print('Database stats: {} files, {} downloaded'.format(stat[0], stat[1]))

    #scan filenames
    cc = find_camelcase(sh_db)
    print('{} filenames found to contain CamelCase'.format(len(cc)))

        #add spaces to CamElcAse (e.g. Cam Elc Ase)
        #change '.' to '_' (except for extension)
        #change '-' to '_'
        #expand known abreviations (use a public dictionary to identify words to identify abreviations)

        #check file date from original filename, if different from fixed filename, move file.

