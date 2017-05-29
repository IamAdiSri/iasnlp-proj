#! /usr/bin/python3

# Script for scraping comments from public pages on facebook
# Put the name_id of the pages to be scraped in pages.txt
# Put the access token in token.conf
# Output is APPENDED to output.csv

import requests as req
import csv

MAX_POSTS = 2000
MAX_COMMENTS = 300

GRAPH_API_VERSION = 'v2.9'
POSTS_LIMIT = '50'
COMMENTS_LIMIT = '100'

token = ""

# Remove special characters and then append comments to output.csv
def fetch_comments(post):
    ## Prepare URL for get requests
    url = "https://graph.facebook.com"
    url += "/" + GRAPH_API_VERSION + "/" + post
    url += "?fields=comments.limit(" + COMMENTS_LIMIT + ")"
    url += "&access_token=" + token

    out_file = open('output.csv', 'a+')
    out = csv.writer(out_file)

    n = 0
    while n < MAX_COMMENTS:
        r = req.get(url)
        r = r.json()

        n += int(COMMENTS_LIMIT)

        try:
            for comment in r['comments']['data']:
                try:
                    msg = comment['message']
                    out.writerow([msg.encode('ascii', errors='ignore').decode('ascii')])
                except KeyError:
                    print("$$ W A R N I N G")
                    print("$$$$ Unable to find comment message\n")
        except KeyError:
            print("$$ W A R N I N G")
            print("$$$$ No comments returned in response; checking for pagination\n")

        try:
            next = r['comments']['paging']['next']
            url = next
            print("$$$$ Found pagination link\n")
        except KeyError:
            print("$$ W A R N I N G")
            print("$$$$ Unable to find pagination link\n")
            break

    print("$$ Done with post " + post + "\n")
    out_file.close()


def fetch_posts(page):
    ## Prepare URL for get requests
    url = "https://graph.facebook.com"
    url += "/" + GRAPH_API_VERSION + "/" + page
    url += "?fields=posts.limit(" + POSTS_LIMIT + ")"
    url += "&access_token=" + token

    n = 0
    while n < MAX_POSTS:
        r = req.get(url)
        r = r.json()

        n += int(POSTS_LIMIT)

        if 'error' in r.keys():
            print("> " + r['error']['message'])
            return

        try:
            for post in r['posts']['data']:
                try:
                    id = post['id']
                    fetch_comments(id)
                except KeyError:
                    print(">> W A R N I N G")
                    print(">>>> Unable to find post id\n")
        except KeyError:
            print(">> W A R N I N G")
            print(">>>> No posts returned in response; checking for pagination\n")

        try:
            next = r['posts']['paging']['next']
            url = next
            print(">>>> Found pagination link\n")
        except KeyError:
            print(">> W A R N I N G")
            print(">>>> Unable to find pagination link\n")
            break

    print(">> Done with page " + page + "\n")
    
def scrape():
    global token

    # Fetch token from file
    try:
        token_file = open('token.conf', 'r')
        token = token_file.read()
        token_file.close()
    except FileNotFoundError:   
        token = input("token.conf not found; set token variable manually: ")        

    # Fetch pages to be scraped
    try:
        page_file = open('pages.txt', 'r')
        pages = page_file.readlines()
        page_file.close()
    except FileNotFoundError:
        print("pages.txt not found; cannot continue...")
        return

    ## Remove newline from the end of every line
    for i in range(len(pages)):
        if i != len(pages) - 1:
            pages[i] = pages[i][:-1]

    for page in pages:
        fetch_posts(page)

if __name__=='__main__':
    scrape()