#!/usr/bin/env python

import os
import sys
import re
import shutil
import json
import logging
import requests

endwith = re.compile('.*[0-9]\)$')  # matches a string ending in [0-9])


def sanitise_title(title):
    if '.' in title:
        title = ' '.join(title.split('.')[:-1])

    if '[' in title:
        title = ' '.join(title.split('[')[:-1])

    return title.strip()


def tidy_movies(path):
    for filename in os.listdir(path):
        # Full path is useful for manipulating directories
        full_path = os.path.join(path, filename)

        # Get rid of file extensions and dates formatted like [2001]
        title = sanitise_title(filename)

        # If the string ends with [0-9]) we assume it already has a date
        if endwith.match(title):
            print('Skipping "{movie}" (already has year).'.format(movie=title))
            break

        # If the entry is a file, move it into a directory
        if os.path.isfile(full_path):
            new_path = os.path.join(path, title)

            print('Moving {movie} into a directory.'.format(movie=title))
            logging.info('Moving "{title}" from "{source}" to "{dest}"\n'.format(
                title=title, source=full_path, dest=new_path))

            os.mkdir(new_path)
            shutil.move(full_path, new_path)

            # Change the full path to the new location
            full_path = new_path

        # Get three likely title/dates by searching the title on rotten tomatoes
        print('Getting data for "{movie}"'.format(movie=title))
        data = json.loads(requests.get('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=xrwz8fmkszafbkgyzn2xbegz&q={title}&page_limit=3&page=1'.format(title=title)).text)

        if 'movies' not in data or data['total'] <= 0:
            logging.debug(
                'Skipping "{movie}" (no data found).'.format(movie=title))
        else:
            for movie in data['movies']:
                titleandyear = '{title} ({year})'.format(
                    title=movie['title'], year=str(movie['year']))
                titleandyear = str.replace(titleandyear, ': ', ' - ')

                print('Is "{new}" a good folder name? (y/n): '.format(
                    new=titleandyear))

                if input() == 'y':
                    print('Renaming "{old}" to "{new}"'.format(
                        old=full_path, new=titleandyear))

                    try:
                        logging.info('Renaming "{old}" to "{new}"'.format(
                            old=full_path, new=titleandyear))
                        os.rename(
                            full_path, os.path.join(path, titleandyear))
                    except:
                        print('Skipping "{movie}" (failed to rename).'.format(
                            movie=title))
                        logging.error('Renaming "{old}" to "{new}" failed'.format(
                            old=full_path, new=titleandyear))
                        break

                    break

if __name__ == '__tidy_movies__':
    logging.basicConfig(filename='moviefetch.log', level=logging.DEBUG)
    tidy_movies(sys.argv[1])
