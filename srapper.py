import csv
import json
import os
import urllib2
import zipfile
from collections import namedtuple
from celery import Celery

app = Celery("BSEApp")
app.config_from_object("celeryconfig")

from helper import get_date_str, get_redis_connection, get_sorted_list

zip_filename = 'Bhavcopy.zip'
csv_filename = 'Bhavcopy.csv'

current_path = os.path.dirname(os.path.abspath(__file__))

BSEObj = namedtuple('BSEObj', 'code name open high low close')


def download_zip_and_extract():
    """Remove old downloaded zip and csv file"""
    try:
        os.remove(zip_filename)
        os.remove(csv_filename)
    except:
        pass

    """ Download new zip file """
    response = urllib2.urlopen('https://www.bseindia.com/download/BhavCopy/Equity/EQ' + get_date_str() + '_CSV.ZIP')
    output = open(zip_filename, "w")
    output.write(response.read())
    output.close()

    zip_ref = zipfile.ZipFile(os.path.dirname(os.path.abspath(__file__)) + "/" + zip_filename, 'r')
    zipinfos = zip_ref.infolist()
    zipinfos[0].filename = csv_filename
    zip_ref.extract(zipinfos[0])


def add_to_redis(result_dict):
    json_string = json.dumps(result_dict)
    r = get_redis_connection()
    r.flushall()
    r.set('users', json_string)
    r.set('ten_users', json.dumps(result_dict[:10]))


@app.task
def main1():
    download_zip_and_extract()

    with open(csv_filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader, None)  # Skip Header Row
        result = [
            BSEObj(
                row[0].rstrip().strip(),
                row[1].rstrip().strip(),
                row[4].rstrip().strip(),
                row[5].rstrip().strip(),
                row[6].rstrip().strip(),
                row[7].rstrip().strip()
            )
            for row in spamreader
        ]
        result = get_sorted_list(result, 'tuple')
        result = [obj.__dict__ for obj in result]  # List of dictionaries

    add_to_redis(result_dict=result)


# Executing starts here
if __name__ == '__main__':
    main1()
