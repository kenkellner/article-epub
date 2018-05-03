article-epub
============

Description
-----------

A command-line tool written in Python to convert scientific articles available as HTML into ePub form for reading on a supported e-reader. 
Uses a plugin system with a "recipe" for each supported scientific publisher.
Takes an article URL, title, or (ideally) DOI as input.

Obviously, you need to be able to legally access any article you want to convert, e.g. via a university library.

Like most web scraping applications, the provided recipes are liable to break frequently.

Currently, the following publishers are supported:

* ScienceDirect (Elsevier)
* Springer
* Wiley
* Oxford
* BioOne
* Royal Society
* PLoS ONE
* National Institutes of Health
* NRC Research Press
* Taylor & Francis
* Annual Reviews
* Nature Publishing
* University of Chicago Press

Dependencies
------------

* Linux environment required
* [Calibre](https://calibre-ebook.com/) (to access `ebook-convert`)
* Firefox with headless support
* [Geckodriver](https://github.com/mozilla/geckodriver/releases) installed somewhere in `$PATH`
* [Pandoc](http://pandoc.org/)

    Python packages (available with `pip`):

* [Selenium](http://selenium-python.readthedocs.io/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [pypandoc](https://github.com/bebraw/pypandoc)

Installation
------------

I plan to properly package the application for installation with `pip` in the future, but for now it has to be installed manually.

1. Make sure the dependencies listed above are installed.

2. Clone the repository:

    ```sh
    git clone https://github.com/kenkellner/article-epub
    ```

3. Make `article-epub.py` executable and put it in your `$PATH`.

4. To allow importing the library for use in other Python scripts, copy (or symlink) the `article_epub` folder into your local Python 3 library (e.g. `~/.local/lib/python3.6/site-packages/`).

Usage
-----

```
usage: article-epub [-h] [-u URL] [-d DOI] [-t TITLE] [-o FILE] [-p]

optional arguments:
  -h, --help  show this help message and exit
  -u URL      URL of article
  -d DOI      DOI of article
  -t TITLE    Title of article
  -o FILE     Name of output file
  -p          List supported publishers
```
