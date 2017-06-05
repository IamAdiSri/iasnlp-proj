# Corpus Preprocessing Toolkit

## Requirements

- python3
- [Requests module for python3](http://docs.python-requests.org/en/master/)
- [alphabet-detector package for python3](https://github.com/EliFinkelshteyn/alphabet-detector)
- [emoji module for python3](https://pypi.python.org/pypi/emoji)
- 

## Configuration

There are a total of eight tunable parameters.

- `PAGES_FILE`          :   Absolute address of the file with the list of pages to be scraped, one per line
- `POSTS`               :   Number of posts to be scraped per page
- `COMMENTS`            :   Number of comments to be scraped per post
- `GRAPH_API_VERSION`   :   Version of Facebook's Graph API being called
- `POSTS_LIMIT`         :   Number of posts to be fetched in one API call; it is recommended that you do not change this parameter
- `COMMENTS_LIMIT`      :   Number of comments to be fetched in one API call; it is recommended that you do not change this parameter
- `TOKEN`               :   API access token
- `SETUP_FILE`          :   Absolute address of the file with the above seven config parameters

The first seven parameters can be set in the config file. The config file is set to `scraper.conf` by default. This can be changed by altering the `SCRAPER_FILE` variable after importing the module in your code itself.

All the other parameters are also exposed and can be changed after importing.

## Usage

### As a Script

Run the script `fb_scraper.py`.

### As a Python Module

```
import fb_scraper as fbs

# Initialise all control parameters
fbs.setup()

# Start scraping data
fbs.scrape()
```
The control parameters are loaded from the file specified by the `SETUP_FILE` variable, which is set to `scraper.conf` by default. This variable can be manually changed.

If the configuration file as defined by `SETUP_FILE` is not found, the module loads default values for all parameters. The access token will still have to be set manually.

### Exposed Functions and Parameters

All eight parameters are exposed and can be reset after being imported.

There are two more functions that can be called after setting the `TOKEN` variable;
```
# page_name is the name_id of the page to be scraped
fbs.fetch_posts(page_name)
```
```
# post_id is the id of the post to be scraped
fbs.fetch_comments(post_id)
```

### Output

If the file `output.csv` exists, output is **appended** to the file; else, the file is created on execution, in the same folder as the script.

## Notes

- Public posts' search is no longer available on Graph API, hence hashtags cannot be searched