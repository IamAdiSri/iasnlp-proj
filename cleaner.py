#! /usr/bin/python3

import csv
import re

SETUP_FILE = 'cleaner.conf'
INPUT_FILE = 'output.csv'

# Flags
CLEAN_REDUNDANT_ROWS = '1'
CLEAN_HASHTAGS = '2'
CLEAN_WEB_LINKS = '3'

def remove_redundant_rows(inp):
    temp_file = open('.temp', 'w+')
    temp = csv.writer(temp_file)

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

def clean(flags = (CLEAN_REDUNDANT_ROWS, CLEAN_HASHTAGS, CLEAN_WEB_LINKS)):
    global INPUT_FILE
    global inp_file

    try:
        inp_file = open(INPUT_FILE, 'r')
        inp = csv.reader(line.replace('\0','') for line in inp_file) # removes all null bytes

        inp = remove_redundant_rows(inp) # removes all rows containing no alphabets

        inp_file.close()

    except FileNotFoundError:
        print(">> " + INPUT_FILE + " not found. You can change the input file to be loaded by manually changing the INPUT_FILE variable")

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