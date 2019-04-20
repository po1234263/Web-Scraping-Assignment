import os
import ssl

from datetime import datetime
from . import log

def verify_https_issue():
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context


def write_webpage_as_html(source, dest, data=''):
    try:
        with open(source, 'r', encoding = 'utf-8') as fobj:
            lines = fobj.readlines()
        with open(dest, 'w', encoding = 'utf-8') as fobj:
            for line in lines:
                fobj.write(line)
            fobj.write(data[0])
            fobj.write(data[1])
    except Exception as e:
        print(e)
        log.report(e)
        return False
    else:
        return True


def read_webpage_from_html(filename):
    try:
        with open(filename, encoding='UTF-8') as fobj:
            data = fobj.read()
    except Exception as e:
        print(e)
        log.report(e)
        return False
    else:
        return data

# Getting time difference in minutes when file last modified
def get_last_scraped_time(filename):
    if not os.path.exists(filename):
        return -1 # file doesn't exist

    file_time = os.path.getmtime(filename)
    now = datetime.timestamp(datetime.now())
    diff = now - file_time
    #print(file_time, now, diff)
    minutes = int(round(diff / 60))
    return minutes
    
# Checking the time file created and returns whether the program should redownload or not
def check_cache(filename, cache_time):
    # getting last scarping time info
    scraping_time = get_last_scraped_time(filename)

    # check caching duration 
    if scraping_time < 0 or scraping_time > cache_time:
        return True 
    
    return False 