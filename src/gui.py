import time

import PySimpleGUI as PySG
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options

import archiver
import validators as vad
import pyperclip
import matplotlib
import parse_json
import indexer
import crawler
import stats_graph
import webdriver
from recoveryer import recover_folder, root_browser, auto_recovery

matplotlib.use("TkAgg")
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
DRIVER = wd.Chrome(options=options)
VERSION = "SiteWatch"
INDEX = {}
ROW_COLOR = {}
RED = "red4"
GREEN = "green4"
GREY = "grey50"
WHITE = "white on "


def set_layout():
    # All the stuff inside your window.

    website_layout = [

        [PySG.Text("Web Domains",
                   size=(30, 1),
                   font=("Helvetica", 25),
                   pad=(10, 0),
                   text_color="white")],

        [PySG.Input("Enter a Fully Qualified Domain Name",
                    size=(0, 10),
                    pad=(10, 10),
                    expand_x=True,
                    key="-WEBSITE_NAME-"),

         PySG.Button("Validate",
                     size=(12, 1),
                     pad=((5, 10), (5, 0)),
                     key="-WEBSITE_VALIDATE-")],

        [PySG.Listbox(values=[],
                      size=(0, 25),
                      pad=(10, 0),
                      expand_x=True,
                      key="-WEBSITE_LISTBOX-"),

         PySG.Column([[PySG.Button("Crawl",
                                   size=(12, 1),
                                   key="-WEBSITE_CRAWL-")],
                      [PySG.Button("Delete",
                                   size=(12, 1),
                                   key="-WEBSITE_DELETE-")],
                      [PySG.Button("Copy",
                                   size=(12, 1),
                                   key="-WEBSITE_COPY-")],
                      [PySG.Button("Monitor",
                                   size=(12, 1),
                                   button_color=RED,
                                   disabled=True,
                                   key="-WEBSITE_MONITOR-")],
                      ])
         ],

        [PySG.InputText(size=(0, 1),
                        text_color="grey2",
                        pad=(10, (10, 0)),
                        disabled=True,
                        expand_x=True,
                        enable_events=True,
                        key="-WEBSITE_FILENAME-"),

         PySG.FileBrowse(size=(12, 1),
                         pad=((5, 10), (5, 0)),
                         file_types=(("ALL Files", "*.json"),))],

        [PySG.Button("Upload",
                     size=(14, 1),
                     pad=(10, 10),
                     key="-WEBSITE_UPLOAD-"),

         PySG.Text("NO TASK ASSIGNED...",
                   pad=(5, 10),
                   key="-WEBSITE_INFO")],
    ]

    monitor_layout = [

        [PySG.Text("Watcher",
                   size=(30, 1),
                   font=("Helvetica", 25),
                   pad=(10, 0),
                   text_color="white")],

        {PySG.Table(values=[],
                    headings=["Domain", "Hash", "Updated"],
                    justification="left",
                    text_color="white",
                    alternating_row_color="grey8",
                    auto_size_columns=False,
                    def_col_width=5,
                    col_widths=[28, 30, 15],
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,
                    key="-MONITOR_TABLE-")},

        [PySG.Text("Filter: ",
                   pad=((10, 4), (10, 0))),
         PySG.InputText(size=(0, 10),
                        pad=(10, (10, 0)),
                        expand_x=True,
                        enable_events=True,
                        key="-MONITOR_FILTER-")],

        [PySG.Button("Update",
                     size=(14, 1),
                     pad=(10, 10),
                     key="-MONITOR_UPDATE-"),

         PySG.Button("Update All",
                     size=(14, 1),
                     pad=(10, 10),
                     key="-MONITOR_UPDATE_ALL-"),

         PySG.Button("Details",
                     size=(14, 1),
                     pad=(10, 10),
                     key="-MONITOR_DETAILS-"),

         PySG.Input(enable_events=True,
                    visible=False,
                    key="-MONITOR_WHITELIST-"),

         PySG.FileBrowse("Whitelist",
                         size=(14, 1),
                         pad=(10, 10),
                         enable_events=True,
                         file_types=(("ALL Files", "*.json"),),
                         key="-MONITOR_WHITELIST_BTN-"),

         PySG.Button("Report",
                     size=(14, 1),
                     pad=(10, 10),
                     button_color=RED,
                     disabled=True,
                     key="-MONITOR_REPORT-"),

         PySG.Button("Save",
                     size=(14, 1),
                     pad=(10, 10),
                     button_color=RED,
                     disabled=True,
                     key="-MONITOR_SAVE-")],

        [PySG.ProgressBar(100,
                          size=(82, 20),
                          pad=((10, 0), (0, 0)),
                          orientation="h",
                          key="-MONITOR_PROG-")],

        [PySG.Button("Back",
                     size=(14, 1),
                     pad=(10, 10),
                     key="-MONITOR_BACK-"),

         PySG.Text("NO TASK ASSIGNED...",
                   pad=(5, 10),
                   key="-MONITOR_INFO-"),

         PySG.Stretch(),

         PySG.Button("AUTO",
                     size=(14, 1),
                     pad=(14, 10),
                     button_color=WHITE + GREEN,
                     disabled=False,
                     key="-MONITOR_TOGGLE-"),
         ]
    ]

    stats_layout = [
        [PySG.Text("Statistics",
                   size=(30, 1),
                   font=("Helvetica", 25),
                   pad=(10, 0),
                   text_color="white")],

        [PySG.Canvas(expand_x=True,
                     expand_y=True,
                     pad=(10, 10),
                     key="-STATS_CANVAS-")]
    ]

    recovery_layout = [
        [PySG.Text("Recovery",
                   size=(30, 1),
                   font=("Helvetica", 25),
                   pad=(10, 0),
                   text_color="white")],

        [PySG.Table(values=[],
                    headings=["File", "Hash", "Modified"],
                    justification="left",
                    text_color="white",
                    alternating_row_color="grey8",
                    auto_size_columns=False,
                    def_col_width=5,
                    col_widths=[28, 30, 15],
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,
                    key="-RECOVERY_TABLE-")],

        [PySG.Text("Target Path: ",
                   pad=((10, 12), (10, 0))),

         PySG.InputText(size=(0, 1),
                        text_color="grey2",
                        pad=(10, (10, 0)),
                        disabled=True,
                        expand_x=True,
                        enable_events=True,
                        key="-RECOVERY_ROOT-"),

         PySG.FolderBrowse(size=(12, 1),
                           pad=((5, 10), (5, 0)))],

        [PySG.Text("Backup Path: ",
                   pad=((10, 4), (10, 0))),

         PySG.InputText(size=(0, 1),
                        text_color="grey2",
                        pad=(10, (10, 0)),
                        disabled=True,
                        expand_x=True,
                        enable_events=True,
                        key="-RECOVERY_ARCHIVE-"),

         PySG.FolderBrowse(size=(12, 1),
                           pad=((5, 10), (5, 0)))],

        [PySG.Text("Auto Recover: ",
                   pad=((10, 4), (10, 10))),

         PySG.Button('Off',
                     size=(14, 1),
                     button_color='white on red',
                     key='-RECOVERY_TOGGLE-'),

         PySG.Stretch(),

         PySG.Button("Recover",
                     size=(12, 1),
                     pad=(10, 10),
                     key="-RECOVERY_RECOVER-"),
         ]
    ]

    tab_group = [
        [PySG.TabGroup(
            [[
                PySG.Tab("                    Website                    ",
                         website_layout,
                         key="-WEBSITE_TAB-"),

                PySG.Tab("                    Monitor                    ",
                         monitor_layout,
                         key="-MONITOR_TAB-",
                         disabled=True),

                PySG.Tab("                    Statistics                    ",
                         stats_layout,
                         key="-STATS_TAB-",
                         disabled=False),

                PySG.Tab("                    Recovery                    ",
                         recovery_layout,
                         key="-RECOVERY_TAB-",
                         disabled=False),
            ]],
            expand_y=True,
            enable_events=True,
            key="-TAB_GROUP-")]
    ]

    return tab_group


def generate_gui(layout):
    # Website Variables
    # NONE

    # Monitor Variables
    selected_row = None
    sort = True

    # Statistics Variables
    figure_agg = None

    # Recovery Variables
    filearray2D = []
    original_hashes = []

    auto_recover_status = False
    root_folder_set = False
    # global auto_recover_status
    # global root_folder_set
    target_folder = ""
    backup_folder = ""

    # Create the Window
    window = PySG.Window(VERSION,
                         layout,
                         margins=(10, 5),
                         finalize=True)

    figure_agg = stats_graph.draw_figure(window["-STATS_CANVAS-"].TKCanvas,
                                         stats_graph.create_scatterplot())

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)

        if event == PySG.WIN_CLOSED or event == "Exit":
            DRIVER.close()
            DRIVER.quit()

################################################################################
# WEBSITE EVENTS                                                               #
################################################################################

        if event == "-WEBSITE_VALIDATE-":
            if vad.url(values["-WEBSITE_NAME-"]):
                indexer.add(INDEX, values["-WEBSITE_NAME-"])
                window["-WEBSITE_LISTBOX-"].update(sorted(INDEX.keys()))
                window["-WEBSITE_INFO"].update("VALID DOMAIN ADDED",
                                               text_color=GREEN)
                if INDEX.keys():
                    window["-WEBSITE_MONITOR-"].update(
                        button_color=GREEN, disabled=False)
                else:
                    window["-WEBSITE_MONITOR-"].update(
                        button_color=RED, disabled=True)
            else:
                window["-WEBSITE_INFO"].update("INVALID DOMAIN NAME",
                                               text_color=RED)
        if event == "-WEBSITE_CRAWL-":
            try:
                url = window["-WEBSITE_LISTBOX-"].get_list_values()[
                    window["-WEBSITE_LISTBOX-"].get_indexes()[0]]
                a = crawler.Crawler(url)
                try:
                    for i in a.list:
                        window["-WEBSITE_NAME-"].update(text_color="green4")
                        indexer.add(INDEX, i)
                        window["-WEBSITE_LISTBOX-"].update(sorted(INDEX.keys()))
                        window["-WEBSITE_INFO"].update("DOMAIN CRAWLED",
                                                       text_color=GREEN)
                except Exception:
                    window["-WEBSITE_INFO"].update("DOMAIN CRAWL FAILED",
                                                   text_color=RED)
            except IndexError:
                window["-WEBSITE_INFO"].update("NO ROW SELECTED",
                                               text_color=RED)

        if event == "-WEBSITE_DELETE-":
            try:
                indexer.delete(INDEX,
                               window["-WEBSITE_LISTBOX-"].get_list_values()
                               [window["-WEBSITE_LISTBOX-"].get_indexes()[0]])

                window["-WEBSITE_LISTBOX-"].update(sorted(INDEX.keys()))
                window["-WEBSITE_INFO"].update("DOMAIN DELETED",
                                               text_color=GREEN)
                if INDEX.keys():
                    window["-WEBSITE_MONITOR-"].update(
                        button_color=GREEN, disabled=False)
                else:
                    window["-WEBSITE_MONITOR-"].update(
                        button_color=RED, disabled=True)
            except IndexError:
                window["-WEBSITE_INFO"].update("NO ROW SELECTED",
                                               text_color=RED)

        if event == "-WEBSITE_COPY-":
            try:
                pyperclip.copy(window["-WEBSITE_LISTBOX-"].get_list_values()
                               [window["-WEBSITE_LISTBOX-"].get_indexes()[0]])
                window["-WEBSITE_INFO"].update("DOMAIN COPIED TO CLIPBOARD",
                                               text_color=GREEN)
            except IndexError:
                window["-WEBSITE_INFO"].update("NO ROW SELECTED",
                                               text_color=RED)

        if event == "-WEBSITE_MONITOR-":
            window["-WEBSITE_INFO"].update("", text_color="white")
            for domain in window["-WEBSITE_LISTBOX-"].get_list_values():
                indexer.add(INDEX, domain)

            window["-MONITOR_TABLE-"].update(values=indexer.table(INDEX))
            window["-MONITOR_TABLE-"].Update(
                row_colors=indexer.set_row_color(
                    window["-MONITOR_TABLE-"].get(), ROW_COLOR))

            window["-MONITOR_TAB-"].update(disabled=False)
            window["-TAB_GROUP-"].Widget.select(1)
            window["-WEBSITE_TAB-"].update(disabled=True)
            window["-WEBSITE_INFO"].update("PROCEED TO MONITOR",
                                           text_color=GREEN)

        if event == "-WEBSITE_UPLOAD-":
            try:
                if parse_json.json_verifier(values["-WEBSITE_FILENAME-"],
                                            decryption_password=123, ):

                    INDEX.update(parse_json.json_hash_indexer(
                        values["-WEBSITE_FILENAME-"]))

                    window["-WEBSITE_LISTBOX-"].update(sorted(INDEX.keys()))
                    window["-WEBSITE_INFO"]. \
                        update("VALID INDEX FILE UPLOADED",
                               text_color=GREEN)
                    if INDEX.keys():
                        window["-WEBSITE_MONITOR-"].update(
                            button_color=GREEN,
                            disabled=False)
                    else:
                        window["-WEBSITE_MONITOR-"].update(
                            button_color=RED,
                            disabled=True)
                else:
                    window["-WEBSITE_INFO"]. \
                        update("INVALID INDEX FILE", text_color=RED)
            except FileNotFoundError:
                window["-WEBSITE_INFO"]. \
                    update("INDEX FILE NOT FOUND", text_color=RED)

################################################################################
# MONITOR EVENTS                                                               #
################################################################################
        if values["-MONITOR_FILTER-"] != "":
            filter_list = [row for row in indexer.table(INDEX)
                           if values["-MONITOR_FILTER-"] in " ".join(row)]
            window["-MONITOR_TABLE-"].update(filter_list)
            window["-MONITOR_TABLE-"].Update(
                row_colors=indexer.set_row_color(window["-MONITOR_TABLE-"]
                                                 .get(),
                                                 ROW_COLOR))
            window.refresh()

        if event[0] == "-MONITOR_TABLE-" and event[1] == "+CLICKED+" and sort:
            if event[2][0] == -1 and event[2][1] != -1:
                window["-MONITOR_TABLE-"].update(indexer.sort_table(
                    window["-MONITOR_TABLE-"].get(), event[2][1]))
                window["-MONITOR_TABLE-"].Update(
                    row_colors=indexer.set_row_color(
                        window["-MONITOR_TABLE-"].get(),
                        ROW_COLOR))
                window.refresh()

        if event[0] == "-MONITOR_TABLE-" and event[1] == "+CLICKED+":
            if event[2][0] != -1 and event[2][1] != -1:
                selected_row = event[2][0]
                window.refresh()

        if event == "-MONITOR_UPDATE-":
            window["-MONITOR_INFO-"].update("UPDATING DOMAIN",
                                            text_color=GREY)
            window["-MONITOR_PROG-"].update(0, 1)

            if selected_row is not None:
                url = window["-MONITOR_TABLE-"].get()[selected_row]

                if webdriver.check_whitelist(url):
                    wl = webdriver.whitelist(DRIVER, url)
                    if wl[0]:
                        ROW_COLOR[url[0]] = GREY
                    else:
                        ROW_COLOR[url[0]] = RED

                    INDEX.update({wl[1]: [wl[2], wl[3]]})
                    window["-MONITOR_TABLE-"].update(
                        [row for row in indexer.table(INDEX)
                         if values["-MONITOR_FILTER-"] in " ".join(row)])
                else:
                    updated = webdriver.update(DRIVER, url)
                    INDEX.update(updated)
                    window["-MONITOR_TABLE-"].update(
                        [row for row in indexer.table(INDEX)
                         if values["-MONITOR_FILTER-"] in " ".join(row)])
                    url = window["-MONITOR_TABLE-"].get()[selected_row]
                    if webdriver.compare_hash(DRIVER, url)[0]:
                        ROW_COLOR[url[0]] = GREEN
                    else:
                        ROW_COLOR[url[0]] = RED

                window["-MONITOR_TABLE-"].Update(
                    row_colors=indexer.set_row_color(
                        window["-MONITOR_TABLE-"].get(), ROW_COLOR))
                window["-MONITOR_REPORT-"].update(
                    button_color=GREEN,
                    disabled=False)
                window["-MONITOR_SAVE-"].update(
                    button_color=GREEN,
                    disabled=False)
                window["-MONITOR_INFO-"].update("DOMAIN UPDATED",
                                                text_color=GREEN)
                window["-MONITOR_PROG-"].update(1, 1)
            else:
                window["-MONITOR_INFO-"].update("NO ROW SELECTED",
                                                text_color=RED)

        if event == "-MONITOR_UPDATE_ALL-":
            window["-MONITOR_INFO-"].update("UPDATING ALL DOMAINS",
                                            text_color=GREY)
            webdriver.element_state(window, True)
            sort = False
            max_val = len(window["-MONITOR_TABLE-"].get())
            window["-MONITOR_PROG-"].update(0, max_val)
            for selected_row, url in enumerate(window["-MONITOR_TABLE-"].get()):
                url = window["-MONITOR_TABLE-"].get()[selected_row]

                if webdriver.check_whitelist(url):
                    wl = webdriver.whitelist(DRIVER, url)
                    if wl[0]:
                        ROW_COLOR[url[0]] = GREY
                    else:
                        ROW_COLOR[url[0]] = RED

                    INDEX.update({wl[1]: [wl[2], wl[3]]})
                    window["-MONITOR_TABLE-"].update(
                        [row for row in indexer.table(INDEX)
                         if values["-MONITOR_FILTER-"] in " ".join(row)])
                else:
                    updated = webdriver.update(DRIVER, url)
                    INDEX.update(updated)
                    window["-MONITOR_TABLE-"].update(
                        [row for row in indexer.table(INDEX)
                         if values["-MONITOR_FILTER-"] in " ".join(row)])
                    url = window["-MONITOR_TABLE-"].get()[selected_row]
                    if webdriver.compare_hash(DRIVER, url)[0]:
                        ROW_COLOR[url[0]] = GREEN
                    else:
                        ROW_COLOR[url[0]] = RED

                window["-MONITOR_TABLE-"].Update(
                    row_colors=indexer.set_row_color(window["-MONITOR_TABLE-"]
                                                     .get(),
                                                     ROW_COLOR))
                window["-MONITOR_INFO-"].update(str(selected_row + 1) + " OF " +
                                                str(max_val) + " DOMAIN UPDATED",
                                                text_color=GREY)
                window["-MONITOR_PROG-"].update(selected_row + 1, max_val)
                window.refresh()

            time.sleep(2)
            sort = True
            window["-MONITOR_INFO-"].update("ALL DOMAIN UPDATED",
                                            text_color=GREEN)
            window["-MONITOR_REPORT-"].update(button_color=GREEN)
            window["-MONITOR_SAVE-"].update(button_color=GREEN)
            webdriver.element_state(window, False)


        if event == "-MONITOR_DETAILS-":
            window["-MONITOR_INFO-"].update("GENERATING DETAILS",
                                            text_color=GREY)
            window["-MONITOR_PROG-"].update(0, 1)
            if selected_row is not None:
                domain = window["-MONITOR_TABLE-"].get()[
                    selected_row]
                info = webdriver.details(DRIVER,
                                         domain,
                                         values["-WEBSITE_FILENAME-"])
                pyperclip.copy(info)
                PySG.popup("URL DETAILS",
                           info + "Details copied onto your clipboard", )
                window["-MONITOR_INFO-"].update("GENERATED DETAILS",
                                                text_color=GREEN)
            else:
                window["-MONITOR_INFO-"].update("NO ROW SELECTED",
                                                text_color=RED)
            window["-MONITOR_PROG-"].update(1, 1)

        if event == "-MONITOR_WHITELIST-":
            if values["-MONITOR_WHITELIST-"] != "":
                if webdriver.set_whitelist(values["-MONITOR_WHITELIST-"]):
                    window["-MONITOR_INFO-"].update("WHITELIST UPLOADED",
                                                    text_color=GREEN)
                else:
                    window["-MONITOR_INFO-"].update("INVALID WHITELIST",
                                                    text_color=RED)

        if event == "-MONITOR_REPORT-":
            window["-MONITOR_INFO-"].update("GENERATING REPORT",
                                            text_color=GREY)
            window["-MONITOR_PROG-"].update(0, 1)
            try:
                for url in INDEX.keys():
                    archiver.Diff_url(DRIVER, url)
                archiver.report_generation(INDEX)
                window["-MONITOR_INFO-"].update("REPORT GENERATED",
                                                text_color=GREEN)
            except Exception:
                window["-MONITOR_INFO-"].update("REPORTING FAILED",
                                                text_color=RED)

            window["-MONITOR_PROG-"].update(1, 1)

        if event == "-MONITOR_SAVE-":
            print(INDEX)
            window["-MONITOR_INFO-"].update("SAVING JSON ARCHIVE",
                                            text_color=GREY)
            window["-MONITOR_PROG-"].update(0, 1)
            archiver.archive_updater(DRIVER,
                                     INDEX,
                                     values["-WEBSITE_FILENAME-"])
            window["-MONITOR_INFO-"].update("JSON ARCHIVE UPDATED",
                                            text_color=GREEN)
            if figure_agg:
                stats_graph.delete_fig_agg(figure_agg)
                figure_agg = stats_graph.draw_figure(
                    window["-STATS_CANVAS-"].TKCanvas,
                    stats_graph.create_scatterplot())

            window["-MONITOR_PROG-"].update(1, 1)

        if event == "-MONITOR_BACK-":
            window["-WEBSITE_TAB-"].update(disabled=False)
            window["-TAB_GROUP-"].Widget.select(0)
            window["-MONITOR_TAB-"].update(disabled=True)

        if event == "-MONITOR_TOGGLE-":
            if window["-MONITOR_TOGGLE-"].get_text() == "AUTO":
                sort = False
                window["-MONITOR_TOGGLE-"].update("OFF",
                                                  button_color=WHITE + RED)
                webdriver.auto_updater_handler(True,
                                               window,
                                               values,
                                               DRIVER,
                                               INDEX,
                                               ROW_COLOR)

            elif window["-MONITOR_TOGGLE-"].get_text() == "OFF":
                sort = True
                window["-MONITOR_TOGGLE-"].update("AUTO",
                                                  button_color=WHITE + GREEN)
                webdriver.auto_updater_handler(False,
                                               window,
                                               values,
                                               DRIVER,
                                               INDEX,
                                               ROW_COLOR)

################################################################################
# STATISTICS EVENTS                                                            #
################################################################################
    # NONE

################################################################################
# RECOVERY EVENTS                                                              #
################################################################################
        if event == "-RECOVERY_TABLE-":
            pass
        if event == "-RECOVERY_TOGGLE-":
            auto_recover_status = not auto_recover_status
            if auto_recover_status is True and target_folder != "" and backup_folder != "":
                window["-RECOVERY_TOGGLE-"].update("ON",
                                                   button_color="white on green")
            else:
                window["-RECOVERY_TOGGLE-"].update("OFF",
                                                   button_color="white on red")
            auto_recovery(auto_recover_status, window, target_folder, backup_folder, root_folder_set)
            pass
        if event == "-RECOVERY_ROOT-":
            print(window["-RECOVERY_ROOT-"].get())
            target_folder = values["-RECOVERY_ROOT-"]
            filearray2D = root_browser(target_folder)
            root_folder_set = True
            if values["-RECOVERY_ROOT-"] != "":
                window["-RECOVERY_TABLE-"].update(filearray2D)
        if event == "-RECOVERY_ARCHIVE-":
            print(window["-RECOVERY_ARCHIVE-"].get())
            backup_folder = values["-RECOVERY_ARCHIVE-"]
        if event == "-RECOVERY_RECOVER-":
            if target_folder != "" and backup_folder != "":
                recover_folder(target_folder, backup_folder)
                filearray2D = root_browser(target_folder)
                # original_hashes = root_browser(target_folder)[1]
                window["-RECOVERY_TABLE-"].update(filearray2D)
            else:
                pass
            pass

################################################################################
################################################################################
# TESTS                                                                        #
################################################################################


def test_func():
    return True


def test():
    if test_func():
        return True
    # print("All Testing Completed Successfully")


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
