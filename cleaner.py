#! /usr/bin/python3

import csv
import re
import subprocess as sp

SETUP_FILE = 'cleaner.conf'
INPUT_FILE = 'output.csv'

# Flags
REMOVE_REDUNDANT_ROWS = '1'
REMOVE_HASHTAGS = '2'
REMOVE_WEB_LINKS = '3'
REMOVE_REPEATED_CHARS = '4'

def remove_redundant_rows():
    global INPUT_FILE
    
    inp_file = open(INPUT_FILE, 'r')
    inp = csv.reader(inp_file)

    try:
        temp_file = open('.temp', 'w+')
        temp = csv.writer(temp_file)
    except PermissionError:
        print(">> Permission denied while trying to create temporary file; cannot proceed; returning")
        return

    while True:
        try:
            s = next(inp)[0]
            s = s.strip()
            
            p = re.compile("[a-z]", re.I)
            if p.search(s):
                temp.writerow([s.encode('ascii', errors='ignore').decode('ascii')])
                # print(s)
        except csv.Error:
            pass
        except IndexError:
            pass
        except StopIteration:
            break

    temp_file.close()
    inp_file.close()
    
    sp.call(["rm", INPUT_FILE])
    sp.call(["mv", ".temp", INPUT_FILE])

    try:
        sp.call(["cp", INPUT_FILE, "original_"+INPUT_FILE]) # Creates a backup of the input
    except sp.CalledProcessError:
        print(">> Cannot proceed; returning")
        return
    

def clean(flags = (REMOVE_REDUNDANT_ROWS, REMOVE_HASHTAGS, REMOVE_WEB_LINKS, REMOVE_REPEATED_CHARS)):
    global INPUT_FILE

    try:
        sp.call(["cp", INPUT_FILE, "original_"+INPUT_FILE]) # Creates a backup of the input
    except sp.CalledProcessError:
        print(">> Cannot proceed; returning")
        return

    if REMOVE_REDUNDANT_ROWS in flags:
        remove_redundant_rows() # remove all rows containing no alphabets
    # if REMOVE_HASHTAGS in flags:
    #     remove_hashtags() # remove all hashtags from the comments
    # if REMOVE_WEB_LINKS in flags:
    #     remove_web_links() # remove email IDs and website links
    # if REMOVE_REPEATED_CHARS in flags:
    #     remove_repeated_chars() # remove character repetitions   

def setup():
    global SETUP_FILE
    global INPUT_FILE

    try:
        s = open(SETUP_FILE, "r")
        params = s.readlines()
        s.close()

        for param in params:
            t = param.split("=")
            t[0] = t[0].strip()
            t[1] = t[1].strip()

            if 'INPUT_FILE' in t[0]:
                TOKEN = t[1]
            else:
                print(">> Parameter unrecognised: " + t[0])
    except FileNotFoundError:
        print(">> Configuration file " + SETUP_FILE + " not found; loading default paramaters")
        print(">> You can change the configuration file to be loaded by manually changing the SETUP_FILE variable")
 
if __name__=='__main__':
    setup()
    clean()