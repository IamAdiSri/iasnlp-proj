# Corpus Preprocessing Toolkit

## Requirements

- python3
- [Requests module for python3](http://docs.python-requests.org/en/master/)
- [alphabet-detector package for python3](https://github.com/EliFinkelshteyn/alphabet-detector)
- [emoji module for python3](https://pypi.python.org/pypi/emoji)

## Configuration

### Scraper

There are a total of eight tunable parameters.

- `PAGES_FILE`          :   Absolute address of the file with the list of pages to be scraped, one per line
- `POSTS`               :   Number of posts to be scraped per page
- `COMMENTS`            :   Number of comments to be scraped per post
- `GRAPH_API_VERSION`   :   Version of Facebook's Graph API being called
- `POSTS_LIMIT`         :   Number of posts to be fetched in one API call; it is recommended that you do not change this parameter
- `COMMENTS_LIMIT`      :   Number of comments to be fetched in one API call; it is recommended that you do not change this parameter
- `TOKEN`               :   API access token
- `SETUP_FILE`          :   Absolute address of the file with the above seven config parameters

The first seven parameters can be set in the config file. The config file is set to `scraper.conf` by default. This can be changed by altering the `SETUP_FILE` variable after importing the module in your code itself.

All the other parameters are also exposed and can be changed after importing.

### Cleaner

There are two parameters that are to be set in `cleaner.conf`;
- `INPUT_FILE`          :   Absolute location on file containing the data to be cleaned
- `WORDS_FILE`          :   Contains a list of words in order of their relative frequency, with the more frequently used words at the top

Both parameters are exposed and can also be modified after importing.

## Usage

### Scraper

#### As a Script

Run the script `fb_scraper.py`.

#### As a Python Module

```
import fb_scraper as fbs

# Initialise all control parameters
fbs.setup()

# Start scraping data
fbs.scrape()
```
The control parameters are loaded from the file specified by the `SETUP_FILE` variable, which is set to `scraper.conf` by default. This variable can be manually changed.

If the configuration file as defined by `SETUP_FILE` is not found, the module loads default values for all parameters. The access token will still have to be set manually.

#### Exposed Functions and Parameters

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

### Cleaner

#### As a Script

Run the script `cleaner.py`.

#### As a Python Module

```
import cleaner as c

# Initialise all control parameters
c.setup()

# Make a backup of the input file and call cleaning functions
c.clean()
```
You may pass a tuple which specifies the cleaning functions to be performed in `clean()`. This is shown below:
```
# Not passing a tuple automatically calls ALL the cleaning functions
c.clean((REMOVE_REDUNDANT_ROWS, TAG_HASHTAGS))
```
The flags that can be passed in the tuple are `REMOVE_REDUNDANT_ROWS`, `TAG_HASHTAGS`, `TAG_WEB_LINKS`, `REMOVE_REPEATED_CHARS`, `TAG_EMOTICONS`.

The control parameters are loaded from the file specified by the `SETUP_FILE` variable, which is set to `cleaner.conf` by default. This variable can be manually changed.

If the configuration file as defined by `SETUP_FILE` is not found, the module loads default values for all parameters.

#### Exposed Functions and Parameters

All parameters are exposed and can be reset after being imported.

There are a few more functions that can be called after setting the `INPUT_FILE` variable;
```
# All of the below functions will replace the file specied by INPUT_FILE
c.remove_redundant_rows()
c.remove_repeated_chars(),
c.tag_hashtags()
c.tag_web_links()
c.tag_emoticons()
```

The function below needs the `WORDS_FILE` variable to be set first;
```
# s is a string of words missing spaces between them; like "timesnow"
c.separate_ht(s)
```

#### Output
The original file is backed up as `original_filename` and a copy of the same name is modified.

## Notes

- Public posts' search is no longer available on Graph API, hence hashtags cannot be searched