'''
Created on 5/05/2012

@author: Andrew
'''

import requests
import json
import os
import string
import re

endwith = re.compile('.*[0-9]\)$')


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


for directory in listdir_fullpath('D:\Videos\Movies'):
    title = os.path.basename(directory)
    path = os.path.dirname(directory)
    print(title)

    if not endwith.match(title):
        r = requests.get('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=xrwz8fmkszafbkgyzn2xbegz&q={title}&page_limit=3&page=1'.format(title=title))
        t = json.loads(r.text)

        if t['total'] > 0:
            for movie in t['movies']:
                titleandyear = movie['title'] + ' (' + str(movie['year']) + ')'
                titleandyear = string.replace(titleandyear, ': ', ' - ')
                print(titleandyear)

                print('Is this a good folder name? (y/n): ')
                yn = raw_input()

                if yn == 'y':
                    print('Renaming ' + '"' + directory + '"' + ' to ' + '"' + titleandyear + '"')

                    try:
                        os.rename(directory, os.path.join(path, titleandyear))
                    except:
                        print('Failed to rename, skipping.')
                        break

                    break
                else:
                    print('Bad name, skipping.')
        else:
            print('No data found, skipping.')
    else:
        print('Movie already has year, skipping.')
