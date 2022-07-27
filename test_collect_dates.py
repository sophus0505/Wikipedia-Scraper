import pytest

from requesting_urls import get_html
from collect_dates import find_dates


def test_rowling():
	"""Asserts get_html and find_dates for J._K._Rowling
        Returns:
            void.
    """
	html = get_html("https://en.wikipedia.org/wiki/J._K._Rowling")
	result = find_dates(html, "TestOutput/J._K._Rowling.txt")
	assert len(result) > 0

def test_feynman():
	"""Asserts get_html and find_dates for Richard_Feynman
        Returns:
            void.
    """
	html = get_html("https://en.wikipedia.org/wiki/Richard_Feynman")
	result = find_dates(html, "TestOutput/Richard_Feynman.txt")
	assert len(result) > 0

def test_rosling():
	"""Asserts get_html and find_dates for Hans_Rosling
        Returns:
            void.
    """
	html = get_html("https://en.wikipedia.org/wiki/Hans_Rosling")
	result = find_dates(html, "TestOutput/Hans_Rosling.txt")
	assert len(result) > 0