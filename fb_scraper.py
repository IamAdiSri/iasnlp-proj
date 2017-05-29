#! /usr/bin/python3

# Script for scraping comments from public pages on facebook
# Put the name_id of the pages to be scraped in pages.txt
# Put the access token in token.txt
# Output is appended to output.csv

import requests as req
import csv

GRAPH_API_VERSION = 'v2.9'
POSTS_LIMIT = '100'
COMMENTS_LIMIT = '100'

pages = []
token = ""

# Fetch data
def fetch_data():
    global pages

    for page in pages:
        if page[0] != '#':
            ## Prepare URL for get requests
            url = "https://graph.facebook.com"
            url += "/" + GRAPH_API_VERSION + "/" + page
            url += "?fields=posts.limit(" + POSTS_LIMIT + "){comments.limit(" + COMMENTS_LIMIT + ")}"
            url += "&access_token=" + token

            print(url)

            # Make GET request and append response to data
            r = req.get(url)
            r = r.json()

            isolate_comments(r)

# Remove special characters and then append comments to output.csv
def isolate_comments(page):
    out_file = open('output.csv', 'a+')
    out = csv.writer(out_file)
    
    try:
        for post in page['posts']['data']:
            try:
                for obj in post['comments']['data']:
                    out.writerow([obj['message'].encode('ascii', errors='ignore').decode('ascii')])

            except KeyError:
                print(">> No comments to isolate")
    except KeyError:
        if 'error' in page.keys():
            print(page['error']['message'])
        else:
            print(">> Unknown error")
    out_file.close()
    
def main():
    global pages
    global token
    global comments

    # Fetch token from file
    token_file = open('token.txt', 'r')
    token = token_file.read()
    token_file.close()

    # Fetch pages to be scraped
    page_file = open('pages.txt', 'r')
    pages = page_file.readlines()
    page_file.close()

    ## Remove newline from the end of every line
    for i in range(len(pages)):
        if i != len(pages) - 1:
            pages[i] = pages[i][:-1]

    fetch_data()

if __name__=='__main__':
    main()