import os, shutil, argparse
from os.path import join, getsize

# parse command line arguments
parser = argparse.ArgumentParser(description='Remove empty directories')
parser.add_argument("folder", nargs=1, type=str,
        help="root folder whose children to be removed if empty")
parser.add_argument("-s", "--size", nargs="?", const=1, default=1, type=int,
        help="max directory size in KB that considered empty")
args = parser.parse_args()

# assign inputs to constants
DIR = args.folder[0]
MAX_DIR_SIZE_IN_KB = args.size

def get_dir_size(start_path = '.'):
    """ return directory size start from given path """
    total_size = 0
    # for each directory
    for dirpath, dirnames, filenames in os.walk(start_path):
        # for each file
        for filename in filenames:
            filepath = join(dirpath, filename)
            total_size += getsize(filepath)
    return total_size


founded_dirs = []
number_of_found_dirs, total_size = 0, 0
# start from leaf directories to the root (bottom up)
for dirpath, dirnames, filenames in os.walk(DIR, topdown=False):
    for dirname in dirnames:
        current_dirpath = join(dirpath, dirname)
        current_dirsize = get_dir_size(current_dirpath)
        if current_dirsize < MAX_DIR_SIZE_IN_KB * 1024:
            print(current_dirpath)
            founded_dirs.append(current_dirpath)
            number_of_found_dirs += 1
            total_size += current_dirsize

if founded_dirs:
    delete = input("Do you want to delete founded directories[y/n]?")

    if delete == "y":
        for dirpath in founded_dirs:
            shutil.rmtree(dirpath, ignore_errors = False)
            print(dirpath, 'removed')

        print(number_of_found_dirs, 'directories removed')
        print(total_size/1024, 'kB removed')
