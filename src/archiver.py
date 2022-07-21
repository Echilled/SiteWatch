import difflib
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import hashlib
import datetime
import json
import re
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
DRIVER = webdriver.Chrome("chromedriver.exe", options=options)
times_url_change_dict = {}
DOM_CHANGES = {}
APP_PASSWORD = 'happymother123'


def web_hash_checker(url, md5, INDEX, json_file):
    digest = md5.hexdigest()
    try:
        if INDEX[url][0].strip('\n') != digest:
            INDEX[url][0] = digest
            print("Website does not match previous hash archive")  # Need user to accept before updating archive
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


def format_title(title):
    title = title.replace("|", "")
    return title


def index_change_history(json_filename):
    with open(json_filename, "r") as file:
        try:
            data = json.load(file)
            for url, property in data['URLs'].items():
                times_url_change_dict[url] = property['properties']['number of times URL content change']
                # print(properties)
        except Exception as e:
            print(e)
    return times_url_change_dict


def update_change_history(json_filename):
    index_change_history(json_filename)
    # print(times_url_change_dict)
    for key in times_url_change_dict.keys():
        if key in DOM_CHANGES:
            times_url_change_dict[key] = times_url_change_dict.get(key, 0) + 1
    # print(times_url_change_dict)


def archive_updater(json_filename):
    # with open("WebHash.txt", "w+") as wf:
    print("Updating archive")
    # wf.writelines("\n".join(','.join((key,val)) for (key,val) in INDEX.items()))
    JSON_values = []  # Archive web page hash
    temp_dict = {'URLs': {}}
    update_change_history(json_filename)
    for key, val in INDEX.items():
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        changes_number = times_url_change_dict[key]
        JSON_tuple = (key, val[0], now, changes_number)
        JSON_values.append(JSON_tuple)
    for val in JSON_values:
        JSON_dict = json_construct(*val)
        temp_dict['URLs'].update(JSON_dict)
    update_json(json_filename, temp_dict)
    for key in list(DOM_CHANGES.keys()):  # Archive web page code
        # print(DOM_CHANGES.keys())
        DRIVER.get(key)
        page_title = format_title(DRIVER.title)
        old = "archive\\" + page_title + ".html"
        new = "archive\\" + page_title + "_new.html"
        os.remove(old)
        os.rename(new, "archive\\" + page_title + ".html")


def json_construct(id, hash, date, times_it_changed):
    website_dic = {id: {'properties': {}}}
    values = [{'hash': hash}, {'archival_date': date}, {'number of times URL content change': times_it_changed}]
    for val in values:
        website_dic[id]['properties'].update(val)
    return website_dic


def update_json(filename, data_dict):
    with open(filename, "r") as rfile:
        archived_history = json.load(rfile)
        for key, value in archived_history['URLs'].items():
            if key in data_dict['URLs'].keys():
                archived_history['URLs'][key] = data_dict['URLs'][key]
        json_object = json.dumps(archived_history, indent=4)
        rfile.close()
    with open(filename, "w") as outfile:
        outfile.write(json_object)


def page_archiver(page_source, page_title):
    page_title = format_title(page_title)
    if not os.path.isfile("archive\\" + page_title + ".html"):
        #print('First time webpage code archive')
        with open("archive\\" + page_title + ".html", "w+") as file:
            file.write(page_source)
    elif os.path.isfile("archive\\" + page_title + ".html"):
        #print('changed webpage code archived, will use it for comparison
        # later')
        with open("archive\\" + page_title + "_new.html", "w+") as file:
            file.write(page_source)


def show_webpage_code_diff(DOM_CHANGES):
    if DOM_CHANGES:  # If there are any changes to any URLs (dictionary not empty)
        print('There are ' + str(len(DOM_CHANGES)) + ' url/s with changes')
        print('The URL/s with changes are:')
        for key in DOM_CHANGES.keys():
            print(key)
        print('Here are the changes, there might be new content added or removed.:')
        for key, value in DOM_CHANGES.items():
            print('\n', key)
            print("Original content:")
            print(value[0])
            print("Changed:")
            print(value[1])
            print("Removed content:")
            if (get_removed_content(value[1], value[0])) is False:
                print("There is no removed content")
            else:
                print(get_removed_content(value[1], value[0]))
    else:
        print("there are no changes to any URLs")


def Diff(list1, list2):
    new_changed_list = []
    changes_list = []
    present_in_original_list = list(set(list1) - set(list2))
    not_present_in_original_list = list(set(list2) - set(list1))
    # changes_list = list(set(li1) - set(li2)) + list(set(li2) - set(li1))
    for change in present_in_original_list:
        # arrange by closest match, however may also include stuff that is present in new/old but not in old/new
        new_changed_list.append(" ".join(difflib.get_close_matches(change, not_present_in_original_list, 1)))
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
        if os.path.isfile(old) and os.path.isfile(new):  # If files exist in the archive
            DOM_CHANGES[url] = show_difference(old, new)
        else:
            print('relevant files does not exist for comparison, could be first time archiving webpage code')
    except Exception as e:
        print(e)


def get_removed_content(changed_list, original_list):
    empty_element = ''
    indexes = [i for i in range(len(changed_list)) if changed_list[i] == empty_element]
    if str(indexes) == '[]':
        return False
    elif str(indexes) != '[]':
        selected_elements = [original_list[index] for index in indexes]
        return selected_elements


def get_added_content(changed_list, original_list):
    empty_element = ''
    indexes = [i for i in range(len(original_list)) if original_list[i] == empty_element]
    if str(indexes) == '[]':
        return False
    elif str(indexes) != '[]':
        selected_elements = [changed_list[index] for index in indexes]
        return selected_elements


def page_changes_listing(DOM_CHANGES):
    show_webpage_code_diff(DOM_CHANGES)
    userinput = input("Do you accept these changes? y/n")  # only when user accepts, then the archive up beu updated
    if userinput.lower() == "y":
        archive_updater("archive\WebHash.Json")
    if userinput.lower() == "n":
        print("changes discarded")


# print('If you want to accept all changes, press 0')
# decision = input('Enter you choice')
# print(decision)


def ad_blocker():
    all_iframes = DRIVER.find_elements(By.TAG_NAME, "iframe")
    if len(all_iframes) > 0:
        print("Ad Found, changes detected may contain ads\n")
        DRIVER.execute_script("""
            var elems = document.getElementsByTagName("iframe"); 
            for(var i = 0, max = elems.length; i < max; i++)
                 {
                     elems[i].hidden=true;
                 }
                              """)


def report_generation(DOM_CHANGES):
    if not os.path.isdir("Reports\\"):
        os.mkdir("Reports\\")
    date_time_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    date_time_write = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    with open("Reports\\Report_" + date_time_now + ".txt", "w") as rf:
        rf.write("URLs checked at: " + date_time_write + "\n")
        for url in INDEX.keys():
            rf.write(url + '\n')
            if url in DOM_CHANGES.keys():
                rf.write("Approved changes not in whitelist:\n")
                rf.write("Original content: " + str(DOM_CHANGES[url][0]) + "\n")
                rf.write("Changed/removed content: " + str(DOM_CHANGES[url][1]) + "\n")
                if get_removed_content(DOM_CHANGES[url][1], DOM_CHANGES[url][0]) is not False:
                    rf.write("Content Removed: " + str(get_removed_content(DOM_CHANGES[url][1], DOM_CHANGES[url][0])))
                    rf.write("\n")
            else:
                rf.write("No content changes to URL" + "\n")
            rf.write("Number of times URL content changed up to this point:" + str(times_url_change_dict[url]) + "\n\n")

    rf.close()


def clean_urls(url_list):
    regex = re.compile(
        r'^.*\.(?!js$|ico$|atom$|png$)[^.]+$')  # remove non-webpages
    filtered = [i for i in url_list if regex.match(i)]
    return filtered
