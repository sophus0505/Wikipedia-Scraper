import re
import bs4
import asyncio
import aiohttp

import requests as req

from collections import deque

def find_en_articles(url):
    response = req.get(url)
    html_str = response.text
    soup = bs4.BeautifulSoup(html_str, "lxml")
    content_header = soup.find(id="content")

    articles = []
    for a in content_header.find_all("a", href=True):
        url = a["href"]
        if re.match(r".+\:", url):
            continue
        if re.match(r"^/\w.+", url):
            articles.append("https://en.wikipedia.org" + url)

    return articles

def find_en_articles_html(html_str):

    soup = bs4.BeautifulSoup(html_str, "lxml")
    content_header = soup.find(id="content")

    articles = []
    for a in content_header.find_all("a", href=True):
        url = a["href"]
        if re.match(r".+\:", url):
            continue
        if re.match(r"^/\w.+", url):
            articles.append("https://en.wikipedia.org" + url)

    return articles


def wiki_race(src_url, dst_url):
    parents = get_parents(src_url, dst_url)

    path = []
    
    first = dst_url
    while first:
        path.append(first)
        first = parents[first]

    path.reverse()
    return path


def get_parents(src_url, dst_url):
    parents = {src_url: None}
    queue = deque([src_url])

    while queue:
        first = deque.popleft(queue)
        print(first)
        articles = find_en_articles(first)

        for article in articles:
            article =  article

            if article == dst_url:
                return parents

            if article not in parents:
                parents[article] = first
                queue.append(article)


def first_list_urls(src_url):
    return find_en_articles(src_url)

async def fetch(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.text()

async def fetch_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main(urls):    
    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all(session, urls)
    return htmls

def get_urls(html):
    urls = find_en_articles_html(html)
    htmls = asyncio.run(main(urls))
    return urls



if __name__ == "__main__":

    src_url = "https://en.wikipedia.org/wiki/Parque_18_de_marzo_de_1938"
    dst_url = "https://en.wikipedia.org/wiki/Bill_Mundell"


    urls = find_en_articles(src_url)
    htmls = asyncio.run(main(urls)) 

    while True:
        for html in htmls:
            urls = get_urls(html)
            print(urls[0])
            if dst_url in urls:
                print('fucking hell')






    # wiki_race(src_url, dst_url)