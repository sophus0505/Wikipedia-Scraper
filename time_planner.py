from bs4 import BeautifulSoup
import requests as req
from collect_dates import find_dates
import re
import os

from requesting_urls import get_html

def extract_events(url):
    """ Extract date , venue and discipline for competitions .
    Your documentation here .
    Args :
    url (str): The url to extract events from .
    Returns :
        table_info (list of lists): A nested list where the rows represent each
            race date, and the columns are [date, venue, discipline].
    """
    disciplines = {
        "DH": " Downhill",
        "SL": " Slalom",
        "GS": " Giant Slalom",
        "SG": " Super Giant Slalom",
        "AC": " Alpine Combined",
        "PG": " Parallel Giant Slalom",}

    # get the html
    html = get_html(url)

    # make soup
    soup = BeautifulSoup(html, "html.parser")

    # Find the tag that contains the Calendar header span
    calendar_header = soup.find(id="Calendar")

    # Find the following table
    calendar_table = calendar_header.find_all_next("table")[0]

    # Find the rows of the first table
    rows = calendar_table.find_all("tr")

    events = []

    # parsing the row of ‘th‘ cells to identify the indices
    # for Event, Venue, and Type (discipline) and append the value to events
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            date = find_dates(str(row))
            date = date[0] if date else None
            elems = [col.text.strip() for col in cols]

            if len(elems) == 11:
                found_venue = elems[3]
                prev_venue = found_venue
                found_discipline = elems[5]
            elif len(elems) == 10:
                found_venue = prev_venue
                found_discipline = elems[4]
            else:
                found_venue = prev_venue
                found_discipline = elems[3]

            # convert discipline code to full name
            found_discipline = disciplines[found_discipline.split()[0]]

            events.append((date, found_venue, found_discipline))

    return events

def create_betting_slip(events, save_as):
    """ Saves a markdown format betting slip to the location
    ’./datetime_filter/<save_as>.md ’.
    
    Args :
        events ( list ): takes a list of 3- tuples containing date , venue and
        type for each event .
        save_as ( string ): filename to save the markdown betting slip as.
    """
    # ensure directory exists
    os.makedirs("datetime_filter", exist_ok = True)

    with open(f"./datetime_filter/{save_as}.md", "w") as out_file:
        out_file.write (f"# BETTING SLIP ({save_as})\n\nName: \n\n")
        out_file.write (" Date | Venue | Discipline | Who wins ?\n")
        out_file.write (" --- | --- | --- | --- \n")
        for e in events :
            date, venue, type = e
            out_file.write(f"{date}|{venue}|{type}|\n")


if __name__ == "__main__":


    url = "https://en.wikipedia.org/wiki/List_of_soups"

    # request url as we have already learned - yeah !
    request = req.get(url)
    soup = BeautifulSoup(request.text, "html.parser")

    # check the title of the wikipedia page

    # get the soup table
    soup_table = soup.find('table', {"class" : 'wikitablesortable'})

    fis_url = 'https://en.wikipedia.org/wiki/2021-22_FIS_Alpine_Ski_World_Cup'

    events = extract_events(fis_url)
    
    create_betting_slip(events, 'betting_slip_empty')