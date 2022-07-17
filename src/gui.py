import PySimpleGUI as PySG
from selenium import webdriver
import validator as vad
import pyperclip

import parse_json
import indexer

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

        [PySG.Text("Web Domains",
                   size=(30, 1),
                   font=("Helvetica", 25),
                   pad=(10, 0),
                   text_color="white")],

        [PySG.InputText("Enter a Fully Qualified Domain Name",
                        size=(65, 10),
                        pad=(10, 0),
                        key="-WEBSITE_NAME-"),

         PySG.Button("Validate",
                     size=(10, 1),
                     key="-WEBSITE_VALIDATE-")],

        [PySG.Listbox(values=[],
                      size=(63, 15),
                      pad=(10, 0),
                      key="-WEBSITE_LISTBOX-"),

         PySG.Column([[PySG.Button("Crawl",
                                   size=(10, 1),
                                   key="-WEBSITE_CRAWL-")],
                      [PySG.Button("Delete",
                                   size=(10, 1),
                                   key="-WEBSITE_DELETE-")],
                      [PySG.Button("Copy",
                                   size=(10, 1),
                                   key="-WEBSITE_COPY-")],
                      [PySG.Button("Monitor",
                                   size=(10, 1),
                                   button_color="black on red3",
                                   disabled=True,
                                   key="-WEBSITE_MONITOR-")],
                      ])
         ],

        [PySG.InputText(size=(64, 1),
                        text_color="grey2",
                        pad=(10, (10, 0)),
                        disabled=True,
                        key="-WEBSITE_FILENAME-"),

         PySG.FileBrowse(size=(10, 1),
                         pad=((5, 0), (5, 0)),
                         file_types=(('ALL Files', '*.json'),))],

        [PySG.Button("Upload",
                     size=(10, 1),
                     pad=(10, 10),
                     key="-WEBSITE_UPLOAD-"),

         PySG.Text("No index file uploaded...",
                   pad=(5, 10),
                   key="-WEBSITE_INDEX_INFO")],
    ]

    monitor_layout = [

        [PySG.Text("Watcher",
                   size=(30, 1),
                   font=("Helvetica", 25),
                   pad=(10, 0), text_color="white")],

        [PySG.Table(values=[],
                    headings=["Domain", "Hash", "Archival Date"],
                    justification="left",
                    alternating_row_color="grey8",
                    auto_size_columns=False,
                    def_col_width=5,
                    col_widths=[22, 27, 15],
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,
                    key='-MONITOR_TABLE-')],

        [PySG.Button("Monitor",
                     size=(10, 1),
                     pad=(10, 10),
                     key="-MONITOR_MONITOR-"),
         PySG.Button("Info",
                     size=(10, 1),
                     pad=(10, 10),
                     key="-MONITOR_INFO-")],

        [PySG.Button("Back",
                     size=(10, 1),
                     pad=(10, 10),
                     key="-MONITOR_BACK-")]
    ]

    tab_group = [
        [PySG.TabGroup(
            [[
                PySG.Tab("        Website        ",
                         website_layout,
                         key="-WEBSITE_TAB-"),

                PySG.Tab("        Monitor        ",
                         monitor_layout,
                         key="-MONITOR_TAB-",
                         disabled=True),
            ]],
            expand_y    =True,
            enable_events=True,
            key='-TAB_GROUP-')]
    ]

    return tab_group


def generate_gui(layout):
    # Website Variables

    # Monitor Variables

    # Create the Window
    window = PySG.Window(VERSION,
                         layout,
                         margins=(10, 5))

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
                indexer.add(INDEX, values["-WEBSITE_NAME-"])
                window["-WEBSITE_LISTBOX-"].update(sorted(INDEX.keys()))
                if INDEX.keys():
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
                indexer.delete(INDEX,
                               window["-WEBSITE_LISTBOX-"].get_list_values()[
                                   window["-WEBSITE_LISTBOX-"].get_indexes()[0]])
                window["-WEBSITE_LISTBOX-"].update(sorted(INDEX.keys()))
                if INDEX.keys():
                    window["-WEBSITE_MONITOR-"].update(
                        button_color="white on green4", disabled=False)
                else:
                    window["-WEBSITE_MONITOR-"].update(
                        button_color="white on red3", disabled=True)
            except IndexError:
                pass

        if event == "-WEBSITE_COPY-":
            try:
                pyperclip.copy(window["-WEBSITE_LISTBOX-"].get_list_values()[
                                   window["-WEBSITE_LISTBOX-"].get_indexes()[0]])
            except IndexError:
                pass

        if event == "-WEBSITE_MONITOR-":
            for domain in window["-WEBSITE_LISTBOX-"].get_list_values():
                indexer.add(INDEX, domain)

            window['-MONITOR_TABLE-'].update(values=indexer.table(INDEX))

            window['-MONITOR_TAB-'].update(disabled=False)
            window['-TAB_GROUP-'].Widget.select(1)
            window['-WEBSITE_TAB-'].update(disabled=True)

        if event == "-WEBSITE_UPLOAD-":
            try:
                if True:  # json verifier and decrypter
                    INDEX.update(
                        parse_json.json_hash_indexer(
                            values["-WEBSITE_FILENAME-"]))
                    window["-WEBSITE_LISTBOX-"].update(sorted(INDEX.keys()))
                    window["-WEBSITE_INDEX_INFO"]. \
                        update("VALID INDEX FILE UPLOADED!",
                               text_color="green4")
                    if INDEX.keys():
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
        if event[0] == "-MONITOR_TABLE-" and event[1] == "+CLICKED+":
            if event[2][0] == -1 and event[2][1] != -1:
                window['-MONITOR_TABLE-'].update(values=indexer.sort_table(
                    window['-MONITOR_TABLE-'].get(), event[2][1]))

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
