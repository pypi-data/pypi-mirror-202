import sys

from filewiz import move_file

def main():
    source = sys.argv[1]
    move_file(source)

