import os
import shutil

import pandas as pd
import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pprint


def flush_history():
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/Users/edwardbanner/Library/Application Support/Google/Chrome")
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('/Users/edwardbanner/Downloads/chromedriver', chrome_options=chrome_options)
    driver.get('chrome://history');
    driver.quit()


if __name__ == '__main__':
    #
    # Flush history so latest sites are added to history.
    #
    flush_history()

    #
    # Copy history file to home directory.
    #
    history_path = '/Users/edwardbanner/Library/Application\ Support/Google/Chrome/Default/History'
    os.system(f'cp {history_path} /Users/edwardbanner/History')

    #
    # Get connection to history db.
    #
    history_path = '/Users/edwardbanner/History'
    c = sqlite3.connect(history_path)
    cursor = c.cursor()


    #
    # Query history.
    #
    query = """

    SELECT
    datetime(last_visit_time/1000000-11644473600, "unixepoch") as last_visited,
    url,
    title,
    visit_count
    FROM urls
    ORDER BY last_visited
    DESC;

    """
    rows = cursor.execute(query).fetchall()
    df = pd.DataFrame(rows, columns=['date', 'url', 'title', 'visit_count'])
    for idx, row in df.head().iterrows():
        pprint.pprint(dict(row))
        print()
