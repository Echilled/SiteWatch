import hashlib
import os
from shutil import rmtree, copyfile
from distutils.dir_util import copy_tree
from datetime import datetime as dt
from threading import Thread
from time import sleep
import indexer

recover_state = False
set_root = True
ROW_COLOR = {}
RED = "red4"
GREEN = "green4"
WHITE = "grey50"


def auto_recovery(auto_recover_status, window, target_folder, backup_folder, rootfolderset):
    global recover_state
    global set_root
    if target_folder != "" and backup_folder != "":
        backup_array = root_browser(backup_folder)
    print(auto_recover_status)
    if auto_recover_status:
        recover_state = True
    if not auto_recover_status:
        recover_state = False
    recoverythread = Thread(target=auto_recovery_thread,
                            args=(window, target_folder, backup_array)).start()


def auto_recovery_thread(window, target_folder, backup_array):
    global recover_state
    global set_root
    oldfilearray = []
    while True:
        print(recover_state)
        sleep(5)
        newfilearray = root_browser(target_folder)
        if set_root:
            oldfilearray = window["-RECOVERY_TABLE-"].get()
            set_root = False
        window["-RECOVERY_TABLE-"].update(newfilearray)
        for newfile, fileitem in enumerate(window["-RECOVERY_TABLE-"].get()):
            fileitem = window["-RECOVERY_TABLE-"].get()[newfile]
            for oldfile in oldfilearray:
                if oldfile[0] == fileitem[0] and oldfile[1] != fileitem[1]:
                    ROW_COLOR[fileitem[0]] = RED
                    if recover_state:
                            print("attempting to recover file")
                            for backup_file in backup_array:
                                backup_name = backup_file[0].split("\\")
                                target_name = fileitem[0].split("\\")
                                print(backup_name)
                                if backup_name[-1] == target_name[-1]:
                                    recover_file(fileitem[0], backup_file[0])


                elif oldfile[0] == fileitem[0] and oldfile[1] == fileitem[1]:
                    ROW_COLOR[fileitem[0]] = WHITE
        window["-RECOVERY_TABLE-"].Update(
            row_colors=indexer.set_row_color(window["-RECOVERY_TABLE-"]
                                             .get(),
                                             ROW_COLOR))
        #if recover_state:
        #    if target_folder != "" and backup_folder != "":
        #        recover_folder(target_folder, backup_folder)
        #        pass
        #    pass
    pass


def root_browser(target_folder):
    filearray2D = []
    for root, dirs, files in os.walk(target_folder, topdown=True):
        for name in files:
            # print(os.path.join(root, name))
            FileName = (os.path.join(root, name)).replace("/", "\\")
            hasher = hashlib.md5()
            with open(str(FileName), 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
            filehash = hasher.hexdigest()
            last_modified_time = dt.fromtimestamp(os.path.getmtime(FileName)).strftime("%Y-%m-%d %H:%M:%S")
            # print(name)
            # print(filehash)
            # flatlist=[file]
            filearray2D.append([FileName, filehash, last_modified_time])
    return filearray2D


def wipe_folder(target_folder):
    for filename in os.listdir(target_folder):
        file_path = os.path.join(target_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def recover_folder(target_folder, backup_folder):
    wipe_folder(target_folder)
    files = os.listdir(backup_folder)

    # iterating over all the files in
    # the source directory
    copy_tree(backup_folder, target_folder)


def recover_file(target_file, backup_file):
    print("recovering")
    copyfile(backup_file, target_file)
