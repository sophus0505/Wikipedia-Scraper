import pytest
from filter_urls import find_urls, find_articles
from requesting_urls import get_html


def test_find_urls() :
	"""Asserts find_urls for examples given in assignment
        Returns:
            void.
    """
	html = """
		3 <a href ="# fragment - only " > anchor link </a>
		4 <a id =" some -id" href ="/ relative / path # fragment " > relative link </a>
		5 <a href ="// other . host /same - protocol ">same - protocol link </a>
		<a href =" https :// example .com "> absolute URL </a>
		"""
	urls = find_urls ( html , baseurl ="https://en.wikipedia.org")
	assert urls == [
		"https://en.wikipedia.org/relative/path",
		"https://other.host/same-protocol",
		"https://example.com",
	]

def test_find_nobel():
	"""Asserts find_urls and find_articles for Nobel_Prize
        Returns:
            void.
    """
	html = get_html("https://en.wikipedia.org/wiki/Nobel_Prize")
	urls = find_urls (html, baseurl="https://en.wikipedia.org", output="TestOutput/Nobel_prize_urls.txt")
	articles = find_articles(html, output="TestOutput/Nobel_prize_articles.txt")

	assert len(urls) > 0
	assert len(articles) > 0

def test_find_bundesliga():
	"""Asserts find_urls and find_articles for Bundesliga
        Returns:
            void.
    """
	html = get_html("https://en.wikipedia.org/wiki/Bundesliga")
	urls = find_urls (html, baseurl="https://en.wikipedia.org", output="TestOutput/Bundesliga_urls.txt")
	articles = find_articles(html, output="TestOutput/Bundesliga_articles.txt")

	assert len(urls) > 0
	assert len(articles) > 0

def test_find_alpine():
	"""Asserts find_urls and find_articles for 2019%E2%80%9320_FIS_Alpine_Ski_World_Cup
        Returns:
            void.
    """
	html = get_html(r"https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup")
	urls = find_urls (html, baseurl="https://en.wikipedia.org", output="TestOutput/FIS_Alpine_urls.txt")
	articles = find_articles(html, output="TestOutput/FIS_Alpine_articles.txt")

	assert len(urls) > 0
	assert len(articles) > 0