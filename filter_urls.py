from bs4 import BeautifulSoup as soup
import requests as req
import re

from requesting_urls import get_html


def find_urls(html_str, baseurl=None, output=None):
    """Reads a html string and creates a list of all the urls from an wikipedia page.
    Does not count urls with colons and strips all text after #. 

    Args:
        html_str (str): Html code for the page we are interested in 
        baseurl (str, optional): The base of the article url. Defaults to None.
        output (str, optional): Filename, for writing result to file. Defaults to None.

    Returns:
        list: List of all the urls from the wikipedia page
    """
    if not baseurl:
        reg_base = re.compile(r'https:\/\/.+?\/')
        baseurl = reg_base.findall(html_str)[0]

    reg_a = re.compile(r'<a(.*?)<\/a>')
    reg = re.compile(r'href=\"([^\#\"]+)')
    reg_https = re.compile(r"https{0,1}:")
    reg_colon = re.compile(r"https:\/\/(.*)\:.+")

    urls = set()
    for a_str in reg_a.findall(html_str):
        for url in reg.findall(a_str):
            if url[0:2] == "//":
                url = "https:" + url
            elif reg_https.match(url):
                pass
            else:
                url = baseurl + url
            if not reg_colon.match(url):
                urls.add(url)

    if output != None:
        with open(output, 'w') as outfile:
            for url in urls:
                outfile.write(url + "\n")
    return urls


def find_articles(html_str, baseurl=None, output=None):
    """Generates a list of all the other wikipedia articles that are linked to from a wikipedia page.

    Args:
        html_str (str): The html code of the article
        baseurl (str, optional): The base url of the article. Defaults to None.
        output (str, optional): Filename, for writing results to file. Defaults to None.

    Returns:
        list: List of the urls to the linked wikipedia articles.
    """
    urls = find_urls(html_str, baseurl)
    wiki_reg = re.compile(rf"https:\/\/.+[^\.]\.wikipedia.+")
    colon_reg = re.compile(rf"https:\/\/(.*)\:.+")

    wiki_articles = []
    for url in urls:
        for article in wiki_reg.findall(url):
            if article not in wiki_articles:
                if not colon_reg.findall(article):
                    wiki_articles.append(article)

    if output != None:
        with open(output, 'w') as outfile:
            for url in wiki_articles:
                outfile.write(url + "\n")

    return wiki_articles


if __name__ == '__main__':
    # define urls
    nobel_url = 'https://en.wikipedia.org/wiki/Nobel_Prize'
    bundesliga_url = 'https://en.wikipedia.org/wiki/Bundesliga'
    ski_wc_url = 'https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup'

    # find the html from the url
    nobel_html = get_html(nobel_url)
    bundesliga_html = get_html(bundesliga_url)
    ski_wc_html = get_html(ski_wc_url)

    # find all the urls in the html
    nobel_url_list = find_urls(nobel_html, output='find_urls/nobel_urls.txt')
    bundesliga_url_list = find_urls(
        bundesliga_html, output='find_urls/bundesliga_urls.txt')
    ski_wc_url_list = find_urls(
        ski_wc_html, output='find_urls/ski_wc_urls.txt')

    # find only the urls which point back to wikipedia articles
    nobel_articles = find_articles(
        nobel_html, output='find_urls/nobel_articles.txt')
    bundesliga_articles = find_articles(
        bundesliga_html, output='find_urls/bundesliga_articles.txt')
    ski_wc_articles = find_articles(
        ski_wc_html, output='find_urls/ski_wc_articles.txt')
