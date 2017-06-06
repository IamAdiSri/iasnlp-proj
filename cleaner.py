#! /usr/bin/python3

import csv
import re
import subprocess as sp
from alphabet_detector import AlphabetDetector as ad
from emoji import UNICODE_EMOJI as ue

SETUP_FILE = 'cleaner.conf'
INPUT_FILE = 'output.csv'

# Flags
REMOVE_REDUNDANT_ROWS = '1'
REMOVE_REPEATED_CHARS = '2'
TAG_WEB_LINKS = '3'
TAG_HASHTAGS = '4'
TAG_EMOTICONS = '5'

def tag_web_links():
    global INPUT_FILE

    inp_file = open(INPUT_FILE, 'r')
    inp = csv.reader(inp_file)

    try:
        temp_file = open('.temp', 'w+')
        temp = csv.writer(temp_file)
    except PermissionError:
        print(">> Permission denied while trying to create temporary file; cannot proceed; returning")
        return

    p = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))', flags=re.UNICODE) # courtesy Gruber@DaringFireball.net

    while True:
        try:
            s = next(inp)[0]
            s = s.strip()
            
            links = p.findall(s)
            if len(w) > 0:
                for link in links:
                    if link != '':
                        re.sub(link, "{%s}|WEB_LINK" % link, s)
                temp.writerow([s])
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



def tag_hashtags():
    global INPUT_FILE
    
    inp_file = open(INPUT_FILE, 'r')
    inp = csv.reader(inp_file)

    try:
        temp_file = open('.temp', 'w+')
        temp = csv.writer(temp_file)
    except PermissionError:
        print(">> Permission denied while trying to create temporary file; cannot proceed; returning")
        return

    p = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)
    while True:
        try:
            s = next(inp)[0]
            s = s.strip()
            
            hashtags = p.findall(s)
            if len(w) > 0:
                for hashtag in hashtags:
                    re.sub("＃"+hashtag, "{%s}|HASHTAG" % hashtag, s)
                    re.sub("#"+hashtag, "{%s}|HASHTAG" % hashtag, s)
                temp.writerow([s])
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

def tag_emoticons():
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

            t = ""
            
            for c in s:
                if c in ue.keys():
                    t += "{%s}|EMOJI" % (c)
                else:
                    t += c
            
            temp.writerow([t])
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

    p = re.compile("[a-z]", re.I)
    while True:
        try:
            s = next(inp)[0]
            s = s.strip()
            
            if ad.only_alphabet_chars(s, "LATIN"):
                if p.search(s):
                    temp.writerow([s])
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

def clean(flags = (REMOVE_REDUNDANT_ROWS, TAG_HASHTAGS, TAG_WEB_LINKS, REMOVE_REPEATED_CHARS)):
    global INPUT_FILE

    try:
        sp.call(["cp", INPUT_FILE, "original_"+INPUT_FILE]) # Creates a backup of the input
    except sp.CalledProcessError:
        print(">> Cannot proceed; returning")
        return

    if REMOVE_REDUNDANT_ROWS in flags:
        remove_redundant_rows() # remove all rows containing no latin alphabets
    if TAG_HASHTAGS in flags:
        tag_hashtags() # tag all hashtags from the comments
    if TAG_WEB_LINKS in flags:
        tag_web_links() # tag email IDs and website links
    # if REMOVE_REPEATED_CHARS in flags:
    #     remove_repeated_chars() # remove character repetitions   
    if TAG_EMOTICONS in flags:
        tag_emoticons() # tag emojis   

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