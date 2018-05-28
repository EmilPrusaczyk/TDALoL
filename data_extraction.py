from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import codecs
from pathlib import Path

file = Path('teams')
if not file.is_file():
    teams_url = 'http://www.gamesoflegends.com/teams/liste.php?season=S8&tournament=LCK%20Spring%202018&week=ALL'
    page = urlopen(teams_url)
    soup = BeautifulSoup(page, 'html.parser')
    teams = []
    teams_table = soup.find_all(class_='playerslist')[0].find_all('tr')[1:]

    for row in teams_table:
        url = 'http://www.gamesoflegends.com/teams/' + row.find('a').get('href')[1:]
        name = row.find('a').string
        teams.append((name, url))

    with open('teams', 'w') as file:
        for team, url in teams:
            file.write(team + ',' + url + '\n')
else:
    with open('teams', 'r') as file:
        teams = []
        for line in file:
            team = line.rstrip('\n').split(',')
            teams.append((team[0], team[1]))

file = Path('players')
if not file.is_file():
    players_url = 'http://www.gamesoflegends.com/players/liste.php?season=S8&tournament=LCK%20Spring%202018'
    page = urlopen(players_url)
    soup = BeautifulSoup(page, 'html.parser')

    player_table = soup.find(class_='playerslist')
    tags = []
    table_head = player_table.find('thead').find_all('th')
    for header in table_head:
        tags.append(header.string)

    players = [tags]
    rows = player_table.find_all('tr')[1:]
    for row in rows:
        player = []
        for value in row.find_all('td'):
            player.append(value.string)
        players.append(player)

    for row in players[1:]:
        for i in range(len(row)):
            value = row[i]
            if value[-1] == '%':
                row[i] = value.rstrip('%')

    tags = players[0]
    delete_list = ["Position","Games","Win rate","Penta Kills","Solo Kills","FB %","FB Victim"]
    players_copy = list(players)
    while delete_list:
        index = tags.index(delete_list[0])
        for row in players:
            del row[index]
        del delete_list[0]

    for row in players:
        print(row)

    with open('players', 'w') as file:
        for player in players:
            string = ''
            for value in player:
                string += value + ','
            string = string[:-1]
            file.write(string + '\n')
else:
    with open('players', 'r') as file:
        players = []
        for line in file:
            players.append(line.rstrip('\n').split(','))

for team, url in teams:
    file = Path('teamstats/' + team)
    if not file.is_file():
        url = url.replace(' ', '%20')
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        player_table = soup.find('table', class_='footable').find_all('tr')[2:7]
        player_names = []
        for tr in player_table:
            player_names.append(tr.find_all('a')[0].string)

        player_stats = [players[0]]
        for player_name in player_names:
            for player in players:
                if player[0] == player_name:
                    player_stats.append(player)

        with open('teamstats/' + team, 'w') as file:
            for player_stat in player_stats:
                file.write(','.join(player_stat) + '\n')

regions =  [('LCSEU', 'http://www.gamesoflegends.com/players/liste.php?season=ALL&tournament=EU%20LCS%20Spring%202018&position=ALL&week=ALL'),
            ('NALCS', 'http://www.gamesoflegends.com/players/liste.php?season=ALL&tournament=NA%20LCS%20Spring%202018&position=ALL&week=ALL'),
            ('LPL', 'http://www.gamesoflegends.com/players/liste.php?season=ALL&tournament=LPL%20Spring%202018&position=ALL&week=ALL'),
            ('LMS', 'http://www.gamesoflegends.com/players/liste.php?season=ALL&tournament=LMS%20Spring%202018&position=ALL&week=ALL'),
            ('LCK', 'http://www.gamesoflegends.com/players/liste.php?season=ALL&tournament=LCK%20Spring%202018&position=ALL&week=ALL')]

file = Path('regions')
if not file.is_file():
    with open('regions', 'w') as file:
        for region, url in regions:
            file.write(region + ',' + url + '\n')

playersEU = None
playersNA = None
playersLPL = None
playersLMS = None
playersLCK = None

for region, url in regions:
    region_players = None
    if region == 'LCSEU':
        region_players = playersEU
    elif region == 'NALCS':
        region_players = playersNA
    elif region == 'LPL':
        region_players = playersLPL
    elif region == 'LMS':
        region_players = playersLMS
    elif region == 'LCK':
        region_players = playersLCK

    file = Path('teamstats/' + region)
    if not file.is_file():
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        player_table = soup.find(class_='playerslist')
        tags = []
        table_head = player_table.find('thead').find_all('th')
        for header in table_head:
            tags.append(header.string)

        players = [tags]
        rows = player_table.find_all('tr')[1:]
        for row in rows:
            player = []
            for value in row.find_all('td'):
                player.append(value.string)
            players.append(player)

        for row in players[1:]:
            for i in range(len(row)):
                value = row[i]
                if value[-1] == '%':
                    row[i] = value.rstrip('%')

        tags = players[0]
        delete_list = ["Position", "Games", "Win rate", "Penta Kills", "Solo Kills", "FB %", "FB Victim", 'VSPM', 'GD@15', 'CSD@15', 'XPD@15']
        players_copy = list(players)
        while delete_list:
            index = tags.index(delete_list[0])
            for row in players:
                del row[index]
            del delete_list[0]

        region_players = [players[0]]
        with open('playerlists/' + region, 'r') as file:
            for line in file:
                for player in players:
                    if player[0] == line.rstrip('\n'):
                        region_players.append(player)
                        break

        players = region_players

        for row in players:
            print(row)

        with open('teamstats/' + region, 'w') as file:
            for player in players:
                string = ''
                for value in player:
                    string += value + ','
                string = string[:-1]
                file.write(string + '\n')
    else:
        with open('teamstats/' + region, 'r') as file:
            players = []
            for line in file:
                players.append(line.rstrip('\n').split(','))

