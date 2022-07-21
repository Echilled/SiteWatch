from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
import archiver
import difflib
import hashlib
import datetime


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
DRIVER = webdriver.Chrome("chromedriver.exe", options=options)
DOM_CHANGES = {}
times_url_change_dict = {}


def format_title(title):
    title = title.replace("|", "")
    return title


def get_added_content(changed_list, original_list):
    empty_element = ''
    indexes = [i for i in range(len(original_list)) if
               original_list[i] == empty_element]
    if str(indexes) == '[]':
        return False
    elif str(indexes) != '[]':
        selected_elements = [changed_list[index] for index in indexes]
        return selected_elements


def Diff(list1, list2):
    new_changed_list = []
    changes_list = []
    present_in_original_list = list(set(list1) - set(list2))
    not_present_in_original_list = list(set(list2) - set(list1))
    # changes_list = list(set(li1) - set(li2)) + list(set(li2) - set(li1))
    for change in present_in_original_list:
        # arrange by closest match, however may also include stuff that is present in new/old but not in old/new
        new_changed_list.append(" ".join(
            difflib.get_close_matches(change, not_present_in_original_list, 1)))
    # print(previous_list)
    # print(new_changed_list)
    changes_list.append(present_in_original_list)
    changes_list.append(new_changed_list)
    return changes_list


def show_difference(old_file, new_file):
    f_old = open(old_file)
    old_text = f_old.readlines()
    f_new = open(new_file)
    new_text = f_new.readlines()
    return Diff(old_text, new_text)


def page_checker(url):
    DRIVER.get(url)
    webpage_title = format_title(DRIVER.title)
    old = "archive\\" + webpage_title + ".html"
    new = "archive\\" + webpage_title + "_new.html"
    try:
        if os.path.isfile(old) and os.path.isfile(
                new):  # If files exist in the archive
            DOM_CHANGES[url] = show_difference(old, new)
        else:
            print('relevant files does not exist for comparison,'
                  ' could be first time archiving webpage code')
    except Exception as e:
        print(e)


def web_hash_checker(url, md5, INDEX, json_file):
    digest = md5.hexdigest()
    try:
        if INDEX[url][0].strip('\n') != digest:
            INDEX[url][0] = digest
            print(
                "Website does not match previous hash archive")
            # Need user to accept before updating archive
            page_checker(url)  # function to run if hash is not the same
            # archive_updater()
        else:
            print("Website match previous archive")
            try:
                if "archive\\" + DRIVER.title + "_new.html":
                    os.remove("archive\\" + DRIVER.title + "_new.html")
                    print(url + " archive will not change")
            except FileNotFoundError:
                print(url + " archive will not change")
    except Exception as e:
        # First time archiving
        INDEX[url][0] = digest
        print("New webpage archived")
        times_url_change_dict[url] = 0
        # archive_updater(json_file)


def show_webpage_code_diff(DOM_CHANGES):
    if DOM_CHANGES:  # If there are any changes to any URLs (dictionary not empty)
        print('There are ' + str(len(DOM_CHANGES)) + ' url/s with changes')
        print('The URL/s with changes are:')
        for key in DOM_CHANGES.keys():
            print(key)
        print(
            'Here are the changes, there might be new content added or removed.:')
        for key, value in DOM_CHANGES.items():
            print('\n', key)
            print("Original content:")
            print(value[0])
            print("Changed:")
            print(value[1])
            print("Removed content:")
            #if (get_removed_content(value[1], value[0])) is False:
            #    print("There is no removed content")
            #else:
            #    print(get_removed_content(value[1], value[0]))
    else:
        print("there are no changes to any URLs")


def update(domain):
    DRIVER.get(domain[0])
    dom = DRIVER.page_source
    web_hash = hashlib.md5(dom.encode("utf-8")).hexdigest().upper()
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {domain[0]: [web_hash, date_time]}
