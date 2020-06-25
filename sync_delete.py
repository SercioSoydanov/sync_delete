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
    'C:\\Users\\[username]\\Documents\\folder1',
    'C:\\Users\\[username]\\Documents\\folder2'
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
    return name[-kc_length:] == killcode


def strip_suffix(name):
    """Strip suffix if exists"""

    if is_to_move(name):
        return name[:-kc_length]
    else:
        return name


def update_move_list(move_list, base_path, relative_path=None):
    """Update the passed kill list with the items on the path provided"""

    # stores relative paths to the subdirectories
    # to be scanned
    dirs_to_walk = []

    if relative_path:
        full_path = os.path.join(base_path, relative_path)

    else:
        full_path = base_path

    for dirname, dirs, files in os.walk(full_path):

        for dir in dirs:
            if dir in exclusions:
                continue

            if relative_path:
                cur_dir_rel_path = os.path.join(relative_path, dir)
            else:
                cur_dir_rel_path = dir
            dirs_to_walk.append(cur_dir_rel_path)

            if is_to_move(dir):
                # append the suffixed path
                move_list.append(cur_dir_rel_path)

                # then append the path stripped from the suffix
                # because that's how it exists on the other folders
                move_list.append(cur_dir_rel_path[:-kc_length])

        for file in files:
            if file in exclusions:
                continue

            if relative_path:
                cur_file_rel_path = os.path.join(relative_path, file)
            else:
                cur_file_rel_path = file

            filename, extension = os.path.splitext(file)
            if is_to_move(filename):
                # append the suffixed path
                move_list.append(cur_file_rel_path)

                # then append the path stripped from the suffix
                # because that's how it exists on the other folders
                filename_wo_pfx = filename[:-kc_length] + extension
                if relative_path:
                    cur_file_path_wo_pfx = os.path.join(
                        relative_path, filename_wo_pfx)
                else:
                    cur_file_path_wo_pfx = filename_wo_pfx
                move_list.append(cur_file_path_wo_pfx)

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
            recycle_path = os.path.join(bp, recycle_folder)
            Path(recycle_path).mkdir(parents=True, exist_ok=True)
            now = datetime.now()
            now = now.strftime('%Y-%m-%d-%H-%M-%S')

            filepath = os.path.join(bp, entry)
            filename, extension = os.path.splitext(entry)
            filename = strip_suffix(filename)
            filename_new = filename + '_' + now
            if extension:
                filename_new += extension
            filepath_new = os.path.join(recycle_path, filename_new)

            try:
                os.makedirs(os.path.dirname(filepath_new), exist_ok=True)
                shutil.move(filepath, filepath_new)
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
