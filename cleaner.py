#! /usr/bin/python3

import csv
import re
import subprocess as sp
from alphabet_detector import AlphabetDetector
from emoji import UNICODE_EMOJI as ue
from math import log

SETUP_FILE = 'cleaner.conf'
INPUT_FILE = 'output.csv'
WORDS_FILE = 'words.txt'

# Flags
REMOVE_REDUNDANT_ROWS = '1'
REMOVE_REPEATED_CHARS = '2'
TAG_WEB_LINKS = '3'
TAG_HASHTAGS = '4'
TAG_EMOTICONS = '5'

def separate_ht(s): # courtesy GenericHuman
    global WORDCOST
    global MAXWORD

    try:
        words = open("words.txt").read().split()
        # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability)
        WORDCOST = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
        MAXWORD = max(len(x) for x in words)
    except FileNotFoundError:
        print(">> %s could not be found; cannot load list of words. Returning..." % (WORDS_FILE))
        return s

    s = s.lower()

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters
    # Returns a pair (match_cost, match_length)
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-MAXWORD):i]))
        return min((c + WORDCOST.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    s = " ".join(reversed(out))
    return s

def remove_repeated_chars():
    global INPUT_FILE
    
    inp_file = open(INPUT_FILE, 'r')
    inp = csv.reader(inp_file)

    try:
        temp_file = open('.temp', 'w+')
        temp = csv.writer(temp_file)
    except PermissionError:
        print(">> Permission denied while trying to create temporary file; cannot proceed; returning")
        return

    p = re.compile(r"([a-zA-Z])\1{2,}", re.UNICODE)
    while True:
        try:
            s = next(inp)[0]
            s = s.strip()
            
            s = re.sub(p, r'\1\1', s)
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
            
            s = re.sub(p, r"{\1}|WEB_LINK", s)
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
            
            h = []
            hashtags = p.findall(s)
            for hashtag in hashtags:
                # print(hashtags)
                h = separate_ht(hashtag)
                # print(hashtag, h)
                s = re.sub("#"+hashtag, "{%s}|HASHTAG" % h, s)
                s = re.sub("＃"+hashtag, "{%s}|HASHTAG" % h, s)
            # s = re.sub(p, r" {\1}|HASHTAG", s)

            s = s.strip()
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

    ad = AlphabetDetector()

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

def clean(flags = (REMOVE_REDUNDANT_ROWS, TAG_HASHTAGS, TAG_WEB_LINKS, REMOVE_REPEATED_CHARS, TAG_EMOTICONS)):
    global INPUT_FILE

    try:
        sp.call(["cp", INPUT_FILE, "original_"+INPUT_FILE]) # Creates a backup of the input
    except sp.CalledProcessError:
        print(">> Cannot proceed; returning")
        return

    if REMOVE_REDUNDANT_ROWS in flags:
        remove_redundant_rows() # remove all rows containing no latin alphabets
        print("Removed redundant rows")
    if REMOVE_REPEATED_CHARS in flags:
        remove_repeated_chars() # remove three or more character repetitions   
        print("Removed repeated characters")
    if TAG_HASHTAGS in flags:
        tag_hashtags() # tag all hashtags from the comments
        print("Tagged hashtags")
    if TAG_EMOTICONS in flags:
        tag_emoticons() # tag emojis   
        print("Tagged emoticons")
    if TAG_WEB_LINKS in flags:
        tag_web_links() # tag email IDs and website links
        print("Tagged web links")

def setup():
    global SETUP_FILE
    global INPUT_FILE
    global WORDS_FILE

    try:
        s = open(SETUP_FILE, "r")
        params = s.readlines()
        s.close()

        for param in params:
            t = param.split("=")
            t[0] = t[0].strip()
            t[1] = t[1].strip()

            if 'INPUT_FILE' in t[0]:
                INPUT_FILE = t[1]
            elif 'WORDS_FILE' in t[0]:
                WORDS_FILE = t[1]
            else:
                print(">> Parameter unrecognised: " + t[0])

    except FileNotFoundError:
        print(">> Configuration file " + SETUP_FILE + " not found; loading default paramaters")
        print(">> You can change the configuration file to be loaded by manually changing the SETUP_FILE variable")
 
if __name__=='__main__':
    setup()
    clean()