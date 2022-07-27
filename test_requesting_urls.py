import pytest

from requesting_urls import get_html

def test_ghibli():
	"""Asserts get_html for Studio_Ghibli
        Returns:
            void.
    """
	result = get_html("https://en.wikipedia.org/wiki/Studio_Ghibli", output="TestOutput/ghibli.txt")
	assert result != None
	assert result != ""

def test_starwars():
	"""Asserts get_html for Star_Wars
        Returns:
            void.
    """
	result = get_html("https://en.wikipedia.org/wiki/Star_Wars", output="TestOutput/starwars.txt")
	assert result != None
	assert result != ""

def test_wiki_params():
	"""Asserts get_html for en.wikipedia.org
        Returns:
            void.
    """
	result = get_html("https://en.wikipedia.org/w/index.php", params={"title":"Main_Page", "action":"info"}, output="TestOutput/wiki.txt")
	assert result != None
	assert result != ""

