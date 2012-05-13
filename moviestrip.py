'''
Created on 5/05/2012

@author: Andrew
'''
import os
import re
import 


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

r = re.compile('.*\s\[HD\]')

for d in listdir_fullpath('F:\Files\Videos\Movies'):
    if r.match(d):
        print d
        newname = ' '.join(d.split(' ')[:-1]).strip()
        try:
            os.rename(d, newname)
        except:
            pass
