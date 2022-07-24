import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

import os
import archiver
import hashlib
import datetime

import parse_json

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')


def update(domain):
    DRIVER = webdriver.Chrome(options=options)
    DRIVER.get(domain[0])
    dom = DRIVER.page_source
    title = DRIVER.title.replace("|", "")

    web_hash = hashlib.md5(dom.encode("utf-8")).hexdigest().upper()
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    archiver.page_archiver(dom, title)
    DRIVER.close()
    DRIVER.quit()
    return {domain[0]: [web_hash, date_time]}


def compare_hash(domain):
    DRIVER = webdriver.Chrome(options=options)
    DRIVER.get(domain[0])
    title = DRIVER.title.replace("|", "")
    new_md5 = domain[1]
    try:
        with open("archive/" + title + ".html", "r") as rf:
            dom = "".join(rf.readlines())
            old_md5 = hashlib.md5(dom.encode("utf-8")).hexdigest().upper()

            DRIVER.close()
            DRIVER.quit()
            if new_md5 == old_md5:
                return [True, title, new_md5, old_md5]
            else:
                return [False, title, new_md5, old_md5]
    except FileNotFoundError:
        DRIVER.close()
        DRIVER.quit()
        return [False, "File", "Not", "Found"]


def details(domain, loc):
    DRIVER = webdriver.Chrome(options=options)
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
        DRIVER.close()
        return "".join(out)
    except Exception:
        DRIVER.close()
        DRIVER.quit()
        return "Error Getting Details!"



