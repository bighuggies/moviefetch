#!/usr/bin/env python

import os
import sys
import re
import shutil
import json
import logging
import requests

endwith = re.compile('.*[0-9]\)$')  # matches a string ending in [0-9])


def rename_movie(path, title, year):
    titleandyear = '{title} ({year})'.format(
        title=title, year=year)
    titleandyear = str.replace(titleandyear, ': ', ' - ')

    if input('Is "{new}" a good folder name? (y/n): '.format(new=titleandyear)).lower() == 'y':

        print('Renaming "{old}" to "{new}"'.format(old=path, new=titleandyear))

        try:
            logging.info('Renaming "{old}" to "{new}"'.format(old=path, new=titleandyear))
            shutil.move(path, titleandyear)
        except Exception as e:
            print('Skipping "{movie}" (failed to rename: {error}).'.format(movie=title, error=e))
            logging.error('Renaming "{old}" to "{new}" failed'.format(old=path, new=titleandyear))

        return True

    return False


def tidy_movies(path):
    os.chdir(path)

    for filename in os.listdir(path):
        # Full path is useful for manipulating directories
        full_path = os.path.join(path, filename)
        title = filename.strip()

        # If the string ends with [0-9]) we assume it already has a date
        if endwith.match(title):
            print('Skipping "{movie}" (already has year).'.format(movie=title))
            continue

        # If the entry is a file, move it into a directory
        if os.path.isfile(full_path):
            # Get rid of file extension
            title = os.path.splitext(title)[0]
            new_path = os.path.join(path, title)

            print('Moving {movie} into a directory.'.format(movie=title))
            logging.info('Moving "{title}" from "{source}" to "{dest}"\n'.format(
                title=title, source=full_path, dest=new_path))

            os.mkdir(new_path)
            shutil.move(full_path, new_path)

            # Change the full path to the new location
            full_path = new_path

        # Get three likely title/dates by searching the title on rotten
        # tomatoes
        print('Getting data for "{movie}"'.format(movie=title))
        data = json.loads(
            requests.get('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=xrwz8fmkszafbkgyzn2xbegz&q={title}&page_limit=10&page=1'.format(title=title)).text)

        if 'movies' in data and data['total'] > 0:
            for movie in data['movies']:
                # If we find a good title, don't look at the rest
                if rename_movie(full_path, movie['title'], str(movie['year'])):
                    break
        else:
            logging.debug(
                'Skipping "{movie}" (no data found).'.format(movie=title))


if __name__ == '__main__':
    logging.basicConfig(filename='moviefetch.log', level=logging.DEBUG)
    tidy_movies(sys.argv[1])
