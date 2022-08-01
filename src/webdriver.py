import json
import os
import archiver
import hashlib
import datetime
import parse_json
import time
import threading
import indexer
from bs4 import BeautifulSoup

WHITELIST = {}
RED = "red4"
GREEN = "green4"
GREY = "grey50"
WHITE = "white on "
thread_state = ""


def thread_function( window, values, DRIVER, INDEX, ROW_COLOR):
    global thread_state
    while thread_state == "ON":
        window["-MONITOR_INFO-"].update("STARTING THREAD",
                                        text_color=GREY)
        max_val = len(window["-MONITOR_TABLE-"].get())
        window["-MONITOR_PROG-"].update(0, max_val)
        for selected_row, url in enumerate(window["-MONITOR_TABLE-"].get()):
            if thread_state == "OFF":
                window["-MONITOR_INFO-"].update("STOPPING THREAD",
                                                text_color=RED)
                return
            url = window["-MONITOR_TABLE-"].get()[selected_row]

            if check_whitelist(url):

                wl = whitelist(DRIVER, url)
                if wl[0]:
                    ROW_COLOR[url[0]] = GREY
                else:
                    ROW_COLOR[url[0]] = RED

                INDEX.update({wl[1]: [wl[2], wl[3]]})
                window["-MONITOR_TABLE-"].update(
                    [row for row in indexer.table(INDEX)
                     if values["-MONITOR_FILTER-"] in " ".join(row)])

                window.refresh()

                window["-MONITOR_REPORT-"].update(
                    button_color=GREEN,
                    disabled=False)
                window["-MONITOR_SAVE-"].update(
                    button_color=GREEN,
                    disabled=False)

                window["-MONITOR_TABLE-"].Update(
                    row_colors=indexer.set_row_color(window["-MONITOR_TABLE-"]
                                                     .get(),
                                                     ROW_COLOR))

                window["-MONITOR_INFO-"].update("ALL DOMAIN UPDATED",
                                                text_color=GREEN)
                window["-MONITOR_PROG-"].update(selected_row + 1, max_val)
                window.refresh()

            else:
                updated = update(DRIVER, url)
                INDEX.update(updated)
                window["-MONITOR_TABLE-"].update(
                    [row for row in indexer.table(INDEX)
                     if values["-MONITOR_FILTER-"] in " ".join(row)])
                url = window["-MONITOR_TABLE-"].get()[selected_row]
                if compare_hash(DRIVER, url)[0]:
                    ROW_COLOR[url[0]] = GREEN
                else:
                    ROW_COLOR[url[0]] = RED

                window.refresh()

                window["-MONITOR_REPORT-"].update(
                    button_color=GREEN,
                    disabled=False)
                window["-MONITOR_SAVE-"].update(
                    button_color=GREEN,
                    disabled=False)

            window["-MONITOR_TABLE-"].Update(
                row_colors=indexer.set_row_color(window["-MONITOR_TABLE-"]
                                                 .get(),
                                                 ROW_COLOR))
            window["-MONITOR_PROG-"].update(selected_row + 1, max_val)
            window.refresh()

        window["-MONITOR_INFO-"].update("RE-STARTING THREAD",
                                        text_color=GREEN)
        window["-MONITOR_PROG-"].update(max_val, max_val)
        window.refresh()
        time.sleep(5)


def update_thread(state, window, values, DRIVER, INDEX, ROW_COLOR):
    global thread_state
    if state:
        thread_state = "ON"
        t = threading.Thread(target=thread_function, args=(window,
                                                           values,
                                                           DRIVER,
                                                           INDEX,
                                                           ROW_COLOR)).start()
    if not state:
        thread_state = "OFF"



def update(DRIVER, domain):
    try:
        DRIVER.get(domain[0])
        archiver.ad_blocker(DRIVER)
        dom = DRIVER.page_source
        title = DRIVER.title.replace("|", "")

        web_hash = hashlib.md5(dom.encode("utf-8")).hexdigest().upper()
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        archiver.page_archiver(dom, title)
        archiver.Diff_url(DRIVER, domain[0])
        return {domain[0]: [web_hash, date_time]}
    except Exception:
        print("Problems getting domain")
        return {domain[0]: ["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "0000-00-00 "
                                                                "00:00:00"]}


def check_whitelist(domain):
    if domain[0] in WHITELIST.keys():
        return True
    else:
        return False


def set_whitelist(filepath):
    WHITELIST.clear()
    try:
        with open(filepath) as jf:
            data = json.load(jf)
            for url, tags in data['Whitelist'].items():
                WHITELIST[url] = tags
            return True
    except KeyError:
        print("Invalid WhiteList")
        return False


def whitelist(DRIVER, domain):
    DRIVER.get(domain[0])
    archiver.ad_blocker(DRIVER)
    new_dom = DRIVER.page_source
    new_soup = BeautifulSoup(new_dom, 'html.parser')
    title = DRIVER.title.replace("|", "")
    archiver.page_archiver(new_dom, title)

    with open("archive/" + title + ".html", "r", encoding='utf-8') as rf:
        old_dom = "".join(rf.readlines())
        old_soup = BeautifulSoup(old_dom, 'html.parser')
        for tag in WHITELIST[domain[0]].values():
            for occurrence in new_soup(tag):
                occurrence.decompose()
            for occurrence1 in old_soup(tag):
                occurrence1.decompose()

    new_dom = str(BeautifulSoup(str(new_soup), 'html.parser'))
    old_dom = str(BeautifulSoup(str(old_soup), 'html.parser'))

    with open("archive\\" + title + "_new.html", "w+", encoding='utf-8') as wf:
        wf.write(new_dom)
    with open("archive\\" + title + ".html", "w+", encoding='utf-8') as wf:
        wf.write(old_dom)

    new_md5 = hashlib.md5(new_dom.encode("utf-8")).hexdigest().upper()
    old_md5 = hashlib.md5(old_dom.encode("utf-8")).hexdigest().upper()
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if new_md5 == old_md5:
        return [True, domain[0], new_md5, date_time]
    else:
        return [False, domain[0], new_md5, date_time]


def compare_hash(DRIVER, domain):
    DRIVER.get(domain[0])
    title = DRIVER.title.replace("|", "")
    new_md5 = domain[1]
    try:
        with open("archive/" + title + ".html", "r") as rf:
            dom = "".join(rf.readlines())
            old_md5 = hashlib.md5(dom.encode("utf-8")).hexdigest().upper()
            if new_md5 == old_md5:
                return [True, title, new_md5, old_md5]
            else:
                return [False, title, new_md5, old_md5]
    except FileNotFoundError:
        return [False, "File", "Not", "Found"]


def details(DRIVER, domain, loc):
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


