#!/usr/bin/env python3
# link_verification.py — An exercise in web scraping.
# For more information, see README.md

import bs4
import requests
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
# logging.disable(logging.CRITICAL)  # Note out to enable logging.


def make_soup(site):
    """Process website into bs4 file."""
    res = requests.get(site, timeout=60.0)
    res.raise_for_status()
    the_soup = bs4.BeautifulSoup(res.text, "lxml")
    return the_soup


def soup_urls(site_html):
    """Parse and extract all href links to urls list."""
    a_tags = [a_tag.get("href") for a_tag in site_html.find_all("a")]
    urls = [a_tag for a_tag in a_tags if a_tag[:4] == "http"]
    return urls


def check_save_urls(urls):
    """Checks status of url and scrapes html if result is 200."""
    for index, url in enumerate(urls):
        url_name = f"Page_{index + 1}"
        res = requests.get(url, timeout=60.0)
        res.raise_for_status()
        if res.status_code == 200:
            print(f"Downloading {url_name} ... ")
            with open(f"{url_name}.html", "wb") as url_file:
                for chunk in res.iter_content(100_000):
                    url_file.write(chunk)
        else:
            print(f"Error {res.status_code} on {url}.")


def main():
    site = input("Please enter url here: ")
    site_html = make_soup(site)
    urls = soup_urls(site_html)
    check_save_urls(urls)


if __name__ == "__main__":
    main()
