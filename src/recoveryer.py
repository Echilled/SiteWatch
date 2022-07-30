import os
from shutil import rmtree, copyfile
from distutils.dir_util import copy_tree


def wipe_folder(target_folder):
    print("wiping!")
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
    print("recovering")
    files = os.listdir(backup_folder)

    # iterating over all the files in
    # the source directory
    copy_tree(backup_folder, target_folder)


def recover_file(target_file, backup_file):
    print("recovering")
    copyfile(backup_file, target_file)


def main():
    target_folder = r"C:\Users\Kennard\Desktop\New folder\target"
    backup_folder = r"C:\Users\Kennard\Desktop\New folder\backup"
    target_file = r"C:\Users\Kennard\Desktop\New folder\target\yae.jpg"
    backup_file = r"C:\Users\Kennard\Desktop\New folder\backup\yae.jpg"
    #recover_folder(target_folder, backup_folder)
    #recover_file(target_file, backup_file)
    #print("done")


main()
