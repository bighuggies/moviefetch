#!/usr/bin/env python

import os
import sys
import re
import shutil
import json
import logging
import requests

endwith = re.compile('.*[0-9]\)$')  # matches a string ending in [0-9])
path = sys.argv[1]


def sanitise_title(title):
    if '.' in title:
        title = ' '.join(title.split('.')[:-1])

    if '[' in title:
        title = ' '.join(title.split('[')[:-1])

    return title.strip()


def main():
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)

        title = sanitise_title(filename)

        if os.path.isfile(full_path):
            newdir = os.path.join(path, title)

            print("Moving {movie} into a directory.".format(movie=title))
            log.write('Moving {title} from {source} to {dest}\n'.format(
                title=title, source=full_path, dest=newdir))
            os.mkdir(os.path.join(path, title))
            shutil.move(full_path, newdir)

            full_path = newdir

        if not endwith.match(title):
            print("Getting data for {title}".format(title=title))
            r = requests.get('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=xrwz8fmkszafbkgyzn2xbegz&q={title}&page_limit=3&page=1'.format(title=title))
            t = json.loads(r.text)

            if t['total'] > 0:
                for movie in t['movies']:
                    titleandyear = '{title} ({year})'.format(
                        title=movie['title'], year=str(movie['year']))
                    titleandyear = str.replace(titleandyear, ': ', ' - ')
                    print(titleandyear)

                    print('Is this a good folder name? (y/n): ')
                    yn = input()

                    if yn == 'y':
                        print('Renaming {old} to {new}'.format(
                            old=full_path, new=titleandyear))

                        try:
                            log.write('Renaming {old} to {new}'.format(
                                old=full_path, new=titleandyear))
                            os.rename(
                                full_path, os.path.join(path, titleandyear))
                        except:
                            print('Skipping {movie} (failed to rename).'.format(movie=title))
                            log.write('Renaming {old} to {new} failed'.format(
                                old=full_path, new=titleandyear))
                            break

                        break
            else:
                print('Skipping {movie} (no data found).'.format(movie=title))
        else:
            print('Skipping {movie} (already has year).'.format(movie=title))

if __name__ == '__main__':
    logging.basicConfig(filename='moviefetch.log', level=logging.DEBUG)
    main()