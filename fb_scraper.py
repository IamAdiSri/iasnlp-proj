#! /usr/bin/python3

import requests as req
import csv

# Default parameters
SETUP_FILE = 'scraper.conf'
PAGES_FILE = 'pages.txt'

POSTS = 2000
COMMENTS = 300

GRAPH_API_VERSION = 'v2.9'
POSTS_LIMIT = '50'
COMMENTS_LIMIT = '100'

TOKEN = ""

# Remove special characters and then append comments to output.csv
def fetch_comments(post):
    ## Prepare URL for get requests
    url = "https://graph.facebook.com"
    url += "/" + GRAPH_API_VERSION + "/" + post
    url += "?fields=comments.limit(" + COMMENTS_LIMIT + ")"
    url += "&access_token=" + TOKEN

    out_file = open('output.csv', 'a+')
    out = csv.writer(out_file)

    n = 0
    while n < COMMENTS:
        r = req.get(url)
        r = r.json()

        n += int(COMMENTS_LIMIT)

        try:
            for comment in r['comments']['data']:
                try:
                    msg = comment['message']
                    out.writerow([msg.encode('ascii', errors='ignore').decode('ascii')])
                except KeyError:
                    print("$$ No comment message found")
        except KeyError:
            print("$$ No comments returned in response; checking for pagination")

        try:
            next = r['comments']['paging']['next']
            url = next
            print("$$ Found pagination link")
        except KeyError:
            print("$$ No pagination link found")
            break

    print("$$ Done with post " + post + "\n")
    out_file.close()

# Fetch posts from pages
def fetch_posts(page):
    ## Prepare URL for get requests
    url = "https://graph.facebook.com"
    url += "/" + GRAPH_API_VERSION + "/" + page
    url += "?fields=posts.limit(" + POSTS_LIMIT + ")"
    url += "&access_token=" + TOKEN

    n = 0
    while n < POSTS:
        r = req.get(url)
        r = r.json()

        n += int(POSTS_LIMIT)

        if 'error' in r.keys():
            print(">> Error: " + r['error']['message'])
            return

        try:
            for post in r['posts']['data']:
                try:
                    id = post['id']
                    fetch_comments(id)
                except KeyError:
                    print(">> No post id found")
        except KeyError:
            print(">> No posts returned in response; checking for pagination")

        try:
            next = r['posts']['paging']['next']
            url = next
            print(">> Found pagination link")
        except KeyError:
            print(">> No pagination link found")
            break

    print(">> Done with page " + page + "\n")

# Retrieves all the pages to be scraped    
def scrape():
    global TOKEN
    global PAGES_FILE

    if TOKEN == "":
        TOKEN = input("TOKEN variable not set; enter access token to set manually: ")

    # Fetch pages to be scraped
    try:
        page_file = open(PAGES_FILE, 'r')
        pages = page_file.readlines()
        page_file.close()
    except FileNotFoundError:
        print(PAGES_FILE + " not found; cannot continue...")
        return

    # Remove newline from the end of every line
    for i in range(len(pages)):
        if i != len(pages) - 1:
            pages[i] = pages[i][:-1]

    for page in pages:
        fetch_posts(page)

# Initialises all parameters from the config file
def setup():
    global TOKEN
    global PAGES_FILE
    global POSTS
    global COMMENTS
    global GRAPH_API_VERSION
    global POSTS_LIMIT
    global COMMENTS_LIMIT

    try:
        s = open(SETUP_FILE, "r")
        params = s.readlines()
        s.close()

        for param in params:
            t = param.split("=")
            t[0] = t[0].strip()
            t[1] = t[1].strip()

            if 'TOKEN' in t[0]:
                TOKEN = t[1]
                print(TOKEN)
            elif 'PAGES_FILE' in t[0]:
                PAGES_FILE = t[1]
            elif 'POSTS' in t[0]:
                POSTS = int(t[1])
            elif 'COMMENTS' in t[0]:
                COMMENTS = int(t[1])
            elif 'GRAPH_API_VERSION' in t[0]:
                GRAPH_API_VERSION = t[1]
            elif 'POSTS_LIMIT' in t[0]:
                POSTS_LIMIT = t[1]
            elif 'COMMENTS_LIMIT' in t[0]:
                COMMENTS_LIMIT = t[1]
            else:
                print(">> E R R O R")
                print(">> Parameter unrecognised: " + t[0])
    except FileNotFoundError:
        print(">> Configuration file " + SETUP_FILE + " not found; loading defaults paramaters")
        print(">> You can change the configuration file to be loaded by manually changing the SETUP_FILE variable")

if __name__=='__main__':
    setup()
    scrape()