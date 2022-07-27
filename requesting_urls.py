import numpy as np 
import requests as req

from bs4 import BeautifulSoup as soup

import re
import os

def get_html(url, params = None ,output = None ):
    """Retrieves the html code from an url.

    Args:
        url (str): The url of the website.
        params (dict, optional): The params. Defaults to None.
        output (str, optional): Filename if user wants the html written to file. Defaults to None.

    Returns:
        str: The html code
    """

    # passing the optional paramters argument to the get function
    response = req.get(url, params = params)

    # test if request is successfull
    assert response.status_code == 200, f'status code is {response.status_code}'

    html_str = url + "\n" +  response.text


    if output:
        with open(output, "w") as infile:
            infile.write(html_str)

    return html_str


if __name__ == '__main__':
    studio_ghibli_url = 'https://en.wikipedia.org/wiki/Studio_Ghibli'
    star_wars_url = 'https://en.wikipedia.org/wiki/Star_Wars'
    main_page_url = 'https://en.wikipedia.org/wiki/Main_Page'
    
    get_html(studio_ghibli_url, output="requesting_urls/studio_ghibli.txt ")
    get_html(star_wars_url, output="requesting_urls/star_wars.txt ")
    get_html(main_page_url, params={"title" : "Main_Page", "action" : "info"}, output="requesting_urls/main_page.txt ")
























