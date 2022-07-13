import PySimpleGUI as PySG
from selenium import webdriver
import validator as vad
import pyperclip

import parse_json

VERSION = "SiteWatch v0.1"
# DRIVER = webdriver.Chrome("chromedriver.exe")
INDEX = {}
times_url_change_dict = {}
DOM_CHANGES = {}
APP_PASSWORD = "happymother123"


# DRIVER.minimize_window()


def set_layout():
    # All the stuff inside your window.

    website_layout = [

        [PySG.Text("Web Domains", size=(30, 1), font=("Helvetica", 25),
                   pad=(10, 0), text_color="white")],

        [PySG.InputText("Enter a Fully Qualified Domain Name",
                        key="-WEBSITE_NAME-",
                        size=(57, 10), pad=(10, 0)),
         PySG.Button("Validate", key="-WEBSITE_VALIDATE-",
                     size=(10, 1))],

        [PySG.Listbox(key="-WEBSITE_LISTBOX-", values=[], size=(55, 15),
                      pad=(10, 0)),
         PySG.Column([[PySG.Button("Crawl", key="-WEBSITE_CRAWL-",
                                   size=(10, 1))],
                      [PySG.Button("Delete", key="-WEBSITE_DELETE-",
                                   size=(10, 1))],
                      [PySG.Button("Copy", key="-WEBSITE_COPY-",
                                   size=(10, 1))],
                      [PySG.Button("Monitor", key="-WEBSITE_MONITOR-",
                                   size=(10, 1), button_color="black on red3",
                                   disabled=True)],
                      ])
         ],

        [PySG.InputText(key="-WEBSITE_FILENAME-", disabled=True, size=(57, 1),
                        text_color="grey2", pad=(10, (10, 0))),
         PySG.FileBrowse(size=(10, 1), pad=((5, 0), (5, 0)),
                         file_types=('ALL Files', '*.json'),)],

        [PySG.Button("Upload", key="-WEBSITE_UPLOAD-",
                     size=(10, 1), pad=(10, 10)),
         PySG.Text("No index file uploaded...", key="-WEBSITE_INDEX_INFO",
                   pad=(5, 10))],
    ]

    monitor_layout = [

        [PySG.Text("Watcher", size=(30, 1), font=("Helvetica", 25),
                   pad=(10, 0), text_color="white")],

        [PySG.InputText("Enter thing", key="-MONITOR_NAME-",
                        size=(57, 10), pad=(10, 0))],

        [PySG.Button("Back", key="-MONITOR_BACK-", size=(10, 1), pad=(10, 10))]

    ]

    tab_group = [
        [PySG.TabGroup(
            [[
                PySG.Tab("Website", website_layout, key="-WEBSITE_TAB-"),
                PySG.Tab("Monitor", monitor_layout, key="-MONITOR_TAB-",
                         disabled=True),
            ]],
            key='-TAB_GROUP-', enable_events=True)]
    ]

    return tab_group


def generate_gui(layout):
    # Website Variables
    website_list = []

    # Monitor Variables

    # Create the Window
    window = PySG.Window(VERSION, layout, margins=(10, 5))

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)

        if event == PySG.WIN_CLOSED or event == "Exit":
            break

################################################################################
# WEBSITE EVENTS                                                               #
################################################################################

        if event == "-WEBSITE_VALIDATE-":
            if vad.is_valid_url(values["-WEBSITE_NAME-"]):
                window["-WEBSITE_NAME-"].update(text_color="green4")
                website_list.append(values["-WEBSITE_NAME-"])
                website_list = sorted(set(website_list))
                window["-WEBSITE_LISTBOX-"].update(website_list)
                if website_list:
                    window["-WEBSITE_MONITOR-"].update(
                        button_color="white on green4", disabled=False)
                else:
                    window["-WEBSITE_MONITOR-"].update(
                        button_color="white on red3", disabled=True)
            else:
                window["-WEBSITE_NAME-"].update("Invalid "
                                                "Domain Name",
                                                text_color="red2")
        if event == "-WEBSITE_CRAWL-":
            pass

        if event == "-WEBSITE_DELETE-":
            try:
                website_list.pop(window["-WEBSITE_LISTBOX-"].get_indexes()[0])
                window["-WEBSITE_LISTBOX-"].update(website_list)
                if website_list:
                    window["-WEBSITE_MONITOR-"].update(
                        button_color="white on green4", disabled=False)
                else:
                    window["-WEBSITE_MONITOR-"].update(
                        button_color="white on red3", disabled=True)
            except IndexError:
                pass

        if event == "-WEBSITE_COPY-":
            try:
                pyperclip.copy(
                    website_list[window["-WEBSITE_LISTBOX-"].get_indexes()[0]])
            except IndexError:
                pass

        if event == "-WEBSITE_MONITOR-":
            window['-MONITOR_TAB-'].update(disabled=False)
            window['-TAB_GROUP-'].Widget.select(1)
            window['-WEBSITE_TAB-'].update(disabled=True)

        if event == "-WEBSITE_UPLOAD-":
            try:
                if True:  # json verifier and decrypter
                    INDEX.update(
                        parse_json.json_hash_indexer(
                            values["-WEBSITE_FILENAME-"]))
                    website_list.extend(list(INDEX.keys()))
                    website_list = sorted(set(website_list))
                    window["-WEBSITE_LISTBOX-"].update(website_list)
                    window["-WEBSITE_INDEX_INFO"]. \
                        update("VALID INDEX FILE UPLOADED!",
                               text_color="green4")
                    if website_list:
                        window["-WEBSITE_MONITOR-"].update(
                            button_color="white on green4", disabled=False)
                    else:
                        window["-WEBSITE_MONITOR-"].update(
                            button_color="red3", disabled=True)
                else:
                    window["-WEBSITE_INDEX_INFO"]. \
                        update("INVALID INDEX FILE!", text_color="Red2")
            except FileNotFoundError:
                window["-WEBSITE_INDEX_INFO"]. \
                    update("INDEX FILE NOT FOUND!", text_color="Red2")

################################################################################
# MONITOR EVENTS                                                               #
################################################################################
        if event == "-MONITOR_BACK-":
            window['-WEBSITE_TAB-'].update(disabled=False)
            window['-TAB_GROUP-'].Widget.select(0)
            window['-MONITOR_TAB-'].update(disabled=True)

################################################################################

    window.close()


################################################################################
# TESTS                                                                        #
################################################################################
def test_func():
    return True


def test():
    if test_func():
        return True
    # print("All Testing Completed Successfully!")


################################################################################
# MAIN                                                                         #
################################################################################
def main():
    if test():
        # STYLE
        PySG.theme("DarkGrey11")
        PySG.set_options(font=("Arial", 12))

        # MAIN
        generate_gui(set_layout())


if __name__ == "__main__":
    main()
