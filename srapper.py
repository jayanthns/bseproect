import csv
import json
import os
import urllib2
import zipfile
from collections import namedtuple
from datetime import datetime

from celery import Celery

app = Celery("BSEApp")
app.config_from_object("celeryconfig")

from helper import get_date_str, get_redis_connection, get_sorted_list

zip_filename = 'Bhavcopy.zip'
csv_filename = 'Bhavcopy.csv'

current_path = os.path.dirname(os.path.abspath(__file__))

BSEObj = namedtuple('BSEObj', 'code name open high low close')


def download_zip_and_extract(day=0):
    """Remove old downloaded zip and csv file"""

    """ Download new zip file """
    try:
        response = urllib2.urlopen('https://www.bseindia.com/download/BhavCopy/Equity/EQ' + get_date_str(day) + '_CSV.ZIP')
        # response = urllib2.urlopen('https://www.bseindia.com/download/BhavCopy/Equity/EQ' + '180518' + '_CSV.ZIP')
        try:
            os.remove(zip_filename)
            os.remove(csv_filename)
        except:
            pass
        output = open(zip_filename, "w")
        output.write(response.read())
        output.close()

        zip_ref = zipfile.ZipFile(os.path.dirname(os.path.abspath(__file__)) + "/" + zip_filename, 'r')
        zipinfos = zip_ref.infolist()
        zipinfos[0].filename = csv_filename
        zip_ref.extract(zipinfos[0])

    except:
        download_zip_and_extract(1)


def add_to_redis(result_dict):
    print("ADDING TO REDIS")
    sorted_result = get_sorted_list(result_dict, 'dict')
    json_string = json.dumps(sorted_result)
    r = get_redis_connection()
    r.flushall()
    r.set('users', json_string)
    r.set('ten_users', json.dumps(sorted_result[:10]))
    print("SUCCESS ADDED")


@app.task
def main1():
    print(datetime.utcnow())
    download_zip_and_extract(0)

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
