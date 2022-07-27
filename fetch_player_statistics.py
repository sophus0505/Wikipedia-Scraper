from bs4 import BeautifulSoup
from requesting_urls import get_html
from filter_urls import find_articles

import matplotlib.pyplot as plt 
import numpy as np 

import re

import time


def extract_teams():
    """Extract team names and urls from the NBA Playoff 'Bracket' section table.
    Returns:
        team_names (list): A list of team names that made it to the conference
            semifinals.
        team_urls (list): A list of absolute Wikipedia urls corresponding to team_names.
    """
    url = 'https://en.wikipedia.org/wiki/2021_NBA_playoffs'
    # get html using for example get_html from requesting_urls
    html = get_html(url)

    # create soup
    soup = BeautifulSoup(html, "lxml")
    # find bracket we are interested in
    bracket_header = soup.find(id="Bracket")
    bracket_table = bracket_header.find_next("table")
    rows = bracket_table.find_all("tr")

    # create list of teams
    team_list = []
    name_counter = {}
    for i in range(1, len(rows)):
        cells = rows[i].find_all("td")
        cells_text = [cell.get_text(strip=True) for cell in cells]
        
        # Filter out the cells that are empty
        cells_text = [cell for cell in cells_text if cell]
        # Find the rows that contain seeding, team name and games won
        if len(cells_text) > 1:
            seeding, name, games_won = cells_text
            name = name.strip("*")
            team_list.append((seeding, name, games_won))
            if name in name_counter: name_counter[name] += 1
            else: name_counter[name] = 1


    # Filter out the teams that appear more than once, which means they made it
    # to the conference semifinals
    team_list_filtered = [(seed, name, games_won) for seed, name, games_won in team_list if name_counter[name] > 1]

     # create lists of team names and urls to the team website
    team_names = set()
    team_urls = []
    for seed, name, games_won in team_list_filtered:
        team_names.add(name)


     # find the urls to the wiki page of the teams
    articles = find_articles(str(bracket_table), baseurl='https://en.wikipedia.org/')
    real_names = {}
    article_to_team = {}
    for article in articles:
        for name in team_names:
            if len(name.split()) > 1:
                if re.findall(rf"{name.split()[0]}|{name.split()[1]}", article) != []: # re.match didn't work
                    article_to_team[name] = article
                    real_name = re.findall(rf"https:\/\/.+?_(.+)_", article)[0].replace("_", " ")
                    real_names[name] = real_name
            else:
                if re.findall(rf"{name}", article) != []:
                    article_to_team[name] = article
                    real_name = re.findall(rf"https:\/\/.+?_(.+)_", article)[0].replace("_", " ")
                    real_names[name] = real_name

    cooler_names = [real_names[name] for name in team_names]
    team_urls = [article_to_team[name] for name in team_names]

    return cooler_names, team_urls


def extract_players(team_url):
    """Extract players that played for a specific team in the NBA playoffs.
    Args:
        team_url (str): URL to the Wikipedia article of the season of a given
            team.
    Returns:
        player_names (list): A list of players names corresponding to the team whos URL was passed.
            semifinals.
        player_urls (list): A list of Wikipedia URLs corresponding to
            player_names of the team whos URL was passed.
    """

    # keep base url
    base_url = "https://en.wikipedia.org"

    # get html for each page using the team url you extracted before
    html = get_html(team_url)

    # make soup
    soup = BeautifulSoup(html, "lxml")
    # get the header of the Roster
    roster_header = soup.find(id="Roster")
    # identify table
    roster_table = roster_header.find_next("table")
    rows = roster_table.find_all("tr")

    # prepare lists for player names and urls
    player_names = []
    player_urls = []

    for i in range(0, len(rows)):
        cells = rows[i].find_all("td")
        cells_text = [cell.get_text(strip=True) for cell in cells]

        if len(cells_text) == 7:
            rel_url = cells[2].find_next("a").attrs["href"]

            # Use e.g. regex to remove information in parenthesis following the name
            rel_url = re.sub('_\(.+', '', rel_url)

            # find the player name
            player_name = re.findall(r'[^/wiki/].+', rel_url)[0].replace('_', ' ')
            player_names.append(player_name)

            # need to create absolute urls combining the base and the relative url
            player_urls.append(base_url + rel_url)

    return player_names, player_urls


def extract_player_statistics(player_url):
    """Extract player statistics for NBA player.
    # Note: Make yourself familiar with the 2020-2021 player statistics wikipedia page and adapt the code accordingly.
    Args:
        player_url (str): URL to the Wikipedia article of a player.
    Returns:
        ppg (float): Points per Game.
        bpg (float): Blocks per Game.
        rpg (float): Rebounds per Game.
    """
    # As some players have incomplete statistics/information, you can set a default score, if you want.

    ppg = 0.0
    bpg = 0.0
    rpg = 0.0

    # get html
    html = get_html(player_url)

    # make soup
    soup = BeautifulSoup(html, "lxml")

    # find header of NBA career statistics
    nba_header = soup.find(id="NBA_career_statistics")

    # check for alternative name of header
    if nba_header is None:
        nba_header = soup.find(id="NBA")

    try:
        # find regular season header
        # You might want to check for different spellings, e.g. capitalization
        # You also want to take into account the different orders of header and table
        regular_season_header = nba_header.find_next(id="Regular_season")

        # next we should identify the table
        nba_table = regular_season_header.find_next("table")

    except:
        try:
            # table might be right after NBA career statistics header
            nba_table = nba_header.find_next("table")

        except:
            return ppg, bpg, rpg

    # find nba table header and extract rows
    table_header = nba_table.find_all("th")

    rows = nba_table.find_all('tr')
    ppg = []
    bpg = []
    rpg = []
    for row in rows[1:]:
        row = row.text.split()

        for col in row:
            if re.findall(r'2020', col) != []:
                ppg.append(float(row[12].replace('*', '')))
                bpg.append(float(row[11].replace('*', '')))
                rpg.append(float(row[8].replace('*', '')))

    return ppg, bpg, rpg

def find_3_best_players(team_url):
    """Finds the three best players in a team measured by ppg.

    Args:
        team_url (str): url to the wikipedia page of the team

    Returns:
        team (list of dicts): A list containing three dictionaries that each contain name, ppg, bpg and rpg of a player
    """
    player_names, player_urls = extract_players(team_url)

    num1, num2, num3 = ("", "", 0, 0, 0), ("", "", 0, 0, 0), ("", "", 0, 0, 0)
    for player_name, player_url in zip(player_names, player_urls):
        ppg, bpg, rpg = extract_player_statistics(player_url)
        
        if ppg != 0 and ppg != []:
            ppg, bpg, rpg = max(ppg), max(bpg), max(rpg) # some players have played for several clubs the same year
   
            if ppg > num1[2]:
                num3 = num2
                num2 = num1
                num1 = (player_name, player_url, ppg, bpg, rpg)
            elif ppg > num2[2]:
                num3 = num2
                num2 = (player_name, player_url, ppg, bpg, rpg)
            elif ppg > num3[2]:
                num3 = (player_name, player_url, ppg, bpg, rpg)
    
    # make team dictionary

    team =  [
            {
                'name' : num1[0], 
                'ppg' : num1[2], 
                'bpg' : num1[3], 
                'rpg' : num1[4]
            },
            {
                'name' : num2[0], 
                'ppg' : num2[2], 
                'bpg' : num2[3], 
                'rpg' : num2[4]
            },
            {
                'name' : num3[0], 
                'ppg' : num3[2], 
                'bpg' : num3[3], 
                'rpg' : num3[4]
            },
    ]

    return team


def plot_NBA_player_statistics_ppg(teams):
    """Plot NBA player statistics. In this case, just PPG"""
    count_so_far = 0
    all_names = []

    plt.figure(figsize=(10,10))
    # iterate through each team and the
    for team, players in teams.items():
        # pick the color for the team, from the table above
        # color = color_table[team]
        # collect the ppg and name of each player on the team
        # you'll want to repeat with other stats as well
        ppg = []
        names = []
        for player in players:
            names.append(player["name"])
            ppg.append(player["ppg"])
        # record all the names, for use later in x label
        all_names.extend(names)

        # the position of bars is shifted by the number of players so far
        x = range(count_so_far, count_so_far + len(players))
        count_so_far += len(players)
        # make bars for this team's players ppg,
        # with the team name as the label
        bars = plt.bar(x, ppg, label=team)

  
    
    # use the names, rotated 90 degrees as the labels for the bars
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    # add the legend with the colors  for each team
    plt.legend(loc=0)
    # turn off gridlines
    plt.grid(False)
    # set the title
    plt.title("points per game")
    plt.tight_layout()
    # save the figure to a file
    plt.savefig("NBA_player_statistics/players_over_ppg.png")


def plot_NBA_player_statistics_bpg(teams):
    """Plot NBA player statistics. In this case, just BPG"""
    count_so_far = 0
    all_names = []
    plt.figure(figsize=(10,10))

    # iterate through each team and the
    for team, players in teams.items():
        # pick the color for the team, from the table above
        # color = color_table[team]
        # collect the bpg and name of each player on the team
        # you'll want to repeat with other stats as well
        bpg = []
        names = []
        for player in players:
            names.append(player["name"])
            bpg.append(player["bpg"])
        # record all the names, for use later in x label
        all_names.extend(names)

        # the position of bars is shifted by the number of players so far
        x = range(count_so_far, count_so_far + len(players))
        count_so_far += len(players)
        # make bars for this team's players bpg,
        # with the team name as the label
        bars = plt.bar(x, bpg, label=team)

    

    # use the names, rotated 90 degrees as the labels for the bars
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    # add the legend with the colors  for each team
    plt.legend(loc=0)
    # turn off gridlines
    plt.grid(False)
    # set the title
    plt.title("blocks per game")
    plt.tight_layout()
    # save the figure to a file
    plt.savefig("NBA_player_statistics/players_over_bpg.png")

def plot_NBA_player_statistics_rpg(teams):
    """Plot NBA player statistics. In this case, just RPG"""
    count_so_far = 0
    all_names = []
    plt.figure(figsize=(10,10))

    # iterate through each team and the
    for team, players in teams.items():
        # pick the color for the team, from the table above
        # color = color_table[team]
        # collect the rpg and name of each player on the team
        # you'll want to repeat with other stats as well
        rpg = []
        names = []
        for player in players:
            names.append(player["name"])
            rpg.append(player["rpg"])
        # record all the names, for use later in x label
        all_names.extend(names)

        # the position of bars is shifted by the number of players so far
        x = range(count_so_far, count_so_far + len(players))
        count_so_far += len(players)
        # make bars for this team's players rpg,
        # with the team name as the label
        bars = plt.bar(x, rpg, label=team)
    
    

    # use the names, rotated 90 degrees as the labels for the bars
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    # add the legend with the colors  for each team
    plt.legend(loc=0)

    # turn off gridlines
    plt.grid(False)
    # set the title
    plt.title("rebounds per game")
    plt.tight_layout()
    # save the figure to a file
    plt.savefig("NBA_player_statistics/players_over_rpg.png")


if __name__ == "__main__":
    s = time.time()
    team_names, team_urls = extract_teams()
    teams = {}

    for team_name, team_url in zip(team_names, team_urls):
        player_names, player_urls = extract_players(team_url)
        team = find_3_best_players(team_url)
        teams[team_name] = team

    plot_NBA_player_statistics_ppg(teams)
    plot_NBA_player_statistics_bpg(teams)
    plot_NBA_player_statistics_rpg(teams)

    e = time.time()
    time = e-s
    print(f"{time =}")


