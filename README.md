# Corpus Preprocessing Toolkit

## Prerequisites

- python3
- requests module for python3

## Setup

Create the following files in the same directory as `fb_scraper.py`:
- `pages.txt`
- `token.txt`

Put the IDs of the pages to be scraped in `pages.txt`, one per line.
Put the access-token in `token.txt`.

You can modify the number of posts retrieved and the number of comments fetched per post by modifying the variables `MAX_POSTS` and `MAX_COMMENTS` in `fb_scraper.txt`.

## Usage

Run the script `fb_scraper.py`.

If the file `output.csv` exists, output is appended to the file; else, the file is created on execution, in the same folder as the script.

## Notes

- Public Post search is no longer available on Graph API, hence hashtags cannot be searched