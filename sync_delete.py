import os
import time
import shutil
import traceback

from pathlib import Path
from datetime import datetime


# Klasör yollarını base_path değişkeninin içine ekleyin.
# Dilediğiniz kadar dizin ekleyebilirsiniz.

# Define your folder paths here to the base_paths list.
# You can define as many folders as you wish.

# Windows dizinleri için çift ters taksim işareti kullanın (\\ gibi)
# Use double backslashes for windows paths (like \\)

# Yerel ağınızdaki klasörleri tanımlamak için, tuhaf ama,
# adresi '\\\\bilgisayar-adi\\paylasim_adi' şeklinde girmeniz gerek.

# Belki bir ara okunacak klasörlerin listesini harici bir dosyadan
# okunacak hale getirmek gerekebilir.

# To define a folder on your local network, weirdly, you have to
# write an address such as \\\\computer-name\\share.

# Maybe sometime later I should change the script to make it read
# the paths from an external file.

base_paths = [
    'C:\\Users\\sercio\\Documents\\dev\\test1\\',
    'C:\\Users\\sercio\\Documents\\dev\\test2\\'
    ]

# Tarama işleminden muaf tutulmasını istediğiniz dosya ya da dizin
# isimlerini burada belirleyebilirsiniz.
# Firmamız henüz joker karakter (wildcard) desteklememektedir.

# You can define the file or folder names which you like to be
# excluded from the scan.
# Sadly, our establishment do not support the wildcards as of this moment.

exclusions = [
    '.git'
    ]

# Silinmesini istediğiniz dosya / dizin isimlerinin sonuna eklenecek soneki
# (suffix) burada tanımlıyoruz.

# Here is where we are defining the suffix which will be added to the
# files / folders you like to be deleted
killcode = '__del'

# Silinecek dosyalar nereye gidecek? İşte buraya:
# Where do the deleted files go? Right here:
recycle_folder = '_deleted'

kc_length = len(killcode)


def trim_base_path(path, base_path):
    """Trim the base path from the full path"""
    return path[len(base_path)+1:]


def is_to_move(name):
    """Return True if name is prefixed with killcode. Otherwise return False"""

    filename, ext = os.path.splitext(name)

    return filename[-kc_length:] == killcode


def strip_suffix(name):
    """Strip suffix if exists"""

    filename, ext = os.path.splitext(name)

    if is_to_move(filename):
        return filename[:-kc_length] + ext
    else:
        return name


def build_path(base_path=None, relative_path=None, filename=None):

    path = ''

    if base_path:
        path = base_path

    if relative_path:
        path = os.path.join(path, relative_path)

    if filename:
        path = os.path.join(path, filename)

    return path


def update_move_list(move_list, base_path, relative_path=None):
    """
    Update the passed kill list with the items on the path provided

    File / folder names in the move list are always stripped off the killcode
    """

    # stores relative paths to the subdirectories
    # to be scanned
    dirs_to_walk = []

    full_path = build_path(base_path, relative_path)

    for dirname, dirs, files in os.walk(full_path):

        for dir in dirs:
            if dir in exclusions or dir == recycle_folder:
                continue

            cur_dir_rel_path = build_path(
                relative_path=relative_path, filename=dir)
            dirs_to_walk.append(cur_dir_rel_path)

            if is_to_move(dir):
                move_list.append((relative_path, strip_suffix(dir)))

        for file in files:
            if file in exclusions:
                continue

            cur_file_rel_path = build_path(
                relative_path=relative_path, filename=file)

            if is_to_move(file):
                move_list.append((relative_path, strip_suffix(file)))

        # Then iterate through directories
        for dir in dirs_to_walk:
            update_move_list(move_list, base_path, dir)

        # Break after the first yield because we are looping
        # through all of the subfolders in the above
        # procedure.
        break


def move_targets(base_paths, move_list):
    """
    Remove the matching files with the kill list which are located
    in the base paths
    """

    while len(move_list):
        entry = move_list.pop()
        for bp in base_paths:

            # prepare the recycle path
            recycle_path = build_path(bp, recycle_folder)
            Path(recycle_path).mkdir(parents=True, exist_ok=True)

            # prepare the datetime suffix
            now = datetime.now()
            now = now.strftime('%Y-%m-%d-%H-%M-%S')

            # prepare file / folder info
            (relative_path, filename_full) = entry
            filename, extension = os.path.splitext(filename_full)

            # check if file exists with the killcode or without it
            filepath_full = build_path(bp, relative_path, filename_full)
            if not os.path.exists(filepath_full):
                filename_w_kc = filename + killcode + extension
                filepath_full = build_path(bp, relative_path, filename_w_kc)

            filename_new = filename + '_' + now
            if extension:
                filename_new += extension

            filepath_new = build_path(
                recycle_path, relative_path, filename_new)

            try:
                os.makedirs(os.path.dirname(filepath_new), exist_ok=True)
                shutil.move(filepath_full, filepath_new)
            except:
                pass


def main():

    for bp in base_paths:
        move_list = []
        update_move_list(move_list, bp)
        move_targets(base_paths, move_list)

    # del_files(path_remote)


if __name__ == '__main__':
    main()
