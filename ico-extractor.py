#!/usr/bin/env python3
import os
import sys
import glob
import re
from subprocess import call

IGNORE = r'(\$[^\/]*\$|\{[^\/]*\}|dllcache\/|.tmp\/|SoftwareDistribution\/)'

def get_files(win_dir):
    os.chdir(win_dir)
    types = ('*.exe', '*.dll', '*.cpl')
    files_grabbed = []
    for t in types:
        files_grabbed.extend(glob.glob('**/%s' % t, recursive=True))
    return files_grabbed

def extract_icons(resource, output):
    
    if re.search(IGNORE, resource):
        print("Skipping %s" % resource, file=sys.stderr)
        return
    
    subpath = os.path.join(output, os.path.dirname(resource))
    os.makedirs(subpath, exist_ok=True)
    call(["wrestool", "-t14", "-x", resource, "-o", subpath])

def remove_empty_dir(path):
    try:
        os.rmdir(path)
    except OSError:
        pass

def remove_empty_dirs(path):
    for root, dirnames, filenames in os.walk(path, topdown=False):
        for dirname in dirnames:
            remove_empty_dir(os.path.realpath(os.path.join(root, dirname)))

def main():
    args = sys.argv[1:]

    if len(args) != 2:
        print('usage: win_dir output_dir')
        sys.exit(1)

    win_dir = args[0]
    output_dir = args[1]

    resources = get_files(win_dir)
    for res in resources:
        extract_icons(res, output_dir)

    remove_empty_dirs(output_dir)

if __name__ == '__main__':
    main()
