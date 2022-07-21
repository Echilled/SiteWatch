import os


def format_title(title):
    title = title.replace("|", "")
    return title


def page_archiver(page_source, page_title):
    page_title = format_title(page_title)
    if not os.path.isfile("archive\\" + page_title + ".html"):
        print('First time webpage code archive')
        with open("archive\\" + page_title + ".html", "w+") as file:
            file.write(page_source)
    elif os.path.isfile("archive\\" + page_title + ".html"):
        print('changed webpage code archived, will use it for comparison later')
        with open("archive\\" + page_title + "_new.html", "w+") as file:
            file.write(page_source)
