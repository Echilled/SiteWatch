import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
import archiver
import hashlib
import datetime

import parse_json

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
DRIVER = webdriver.Chrome("chromedriver.exe", options=options)


def update(domain):
    DRIVER.get(domain[0])
    dom = DRIVER.page_source
    title = DRIVER.title.replace("|", "")

    web_hash = hashlib.md5(dom.encode("utf-8")).hexdigest().upper()
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    archiver.page_archiver(dom, title)
    return {domain[0]: [web_hash, date_time]}


def compare_hash(domain):
    DRIVER.get(domain[0])
    title = DRIVER.title.replace("|", "")
    new_md5 = domain[1]

    with open("archive/" + title + ".html", "r") as rf:
        dom = "".join(rf.readlines())
        old_md5 = hashlib.md5(dom.encode("utf-8")).hexdigest().upper()

        if new_md5 == old_md5:
            return [True, title, new_md5, old_md5]
        else:
            return [False, title, new_md5, old_md5]


def details(domain, loc):
    try:
        out = []
        DRIVER.get(domain[0])
        title = DRIVER.title.replace("|", "")

        size_kb = os.path.getsize("archive/" + title + ".html") / 1024.0
        old_index = parse_json.json_hash_indexer(loc)

        out.append("URL: " + domain[0] + "\r\n")
        out.append("Title: " + title + "\r\n")
        out.append("New MD5: " + domain[1] + "\r\n")
        out.append("Old   MD5: " + old_index[domain[0]][0] + "\r\n")
        out.append("Updated: " + domain[2] + "\r\n")
        out.append("Archived: " + old_index[domain[0]][1] + "\r\n")
        out.append("File Size: " + str(size_kb) + "KB" + "\r\n")
        out.append("\r\n")
        return "".join(out)
    except Exception:
        return "Error Getting Details!"



