#! python3
# link_verification.py — An exercise in web scraping.
# For more information, see project_details.txt.

import bs4
import requests

urls = []


def make_soup(site):
    """Process website into bs4 file."""
    res = requests.get(site, timeout=60.0)
    res.raise_for_status()
    the_soup = bs4.BeautifulSoup(res.text, "lxml")
    return the_soup


def soup_urls(site_html):
    """Parse and extract all href links to urls list."""
    a_tags = site_html.find_all("a")
    for a_tag in a_tags:
        urls.append(a_tag["href"])


def check_save_urls(urls):
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


site = input("Please enter url here: ")
site_html = make_soup(site)
soup_urls(site_html)
check_save_urls(urls)
