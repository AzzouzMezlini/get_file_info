# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
from pathlib import Path
from os.path import getsize, getatime, getctime, getmtime
import filetype
import time
import hashlib


def get_file_name(source_path, lfile):
    p = Path(source_path)
    for x in p.iterdir():
        if x.is_file() and is_image(x):
            lfile.append(x)
        elif x.is_dir():
            get_file_name(x, lfile)


def write_file_path(dest_path, l_path_files):
    p = Path(dest_path)
    f = open(p, 'w', encoding="utf-8")
    file_detail = list(map(get_file_info, l_path_files))
    f.write(json.dumps(file_detail, indent=2))


def get_file_info(path_file):
    resolved_file_path = path_file.resolve().as_posix()
    return {
        "nom": resolved_file_path, "info": {
            "taille": getsize(path_file), "date_creation": getctime(path_file), "date_accees": getatime(path_file)
        }, "hash": hash_file(resolved_file_path).hexdigest()
    }


def hash_file(file_path):
    BLOCK_SIZE = 65536  # The size of each read from the file
    file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
    with open(file_path, 'rb') as f:  # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
        while len(fb) > 0:  # While there is still data being read from the file
            file_hash.update(fb)  # Update the hash
            fb = f.read(BLOCK_SIZE)  # Read the next block from the file
    return file_hash


def is_image(file_path):
    guess_type = filetype.guess(file_path)
    if guess_type:
        return guess_type.mime.split('/')[0] == 'image'
    else:
        return False


def main():
    source = r'C:\Users\Dev\PycharmProjects\get_file_info\data'
    list_file = []
    get_file_name(source, list_file)
    write_file_path('output/liste_fichier.json', list_file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
