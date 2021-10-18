#Written by Thea Traw

import csv

#USING noc_regions.csv

nocs = {}

noc_regions_data_file = open('noc_regions.csv')
noc_regions_reader = csv.reader(noc_regions_data_file)

nocs_data_file = open('nocs.csv', 'w')
nocs_writer = csv.writer(nocs_data_file)

heading_row = next(noc_regions_reader)
for row in noc_regions_reader:
    noc = row[0]
    region = row[1]
    if noc not in nocs:

        #deal with Singapore
        if noc == "SIN":
            noc = "SGP"

        noc_id = len(nocs) + 1
        nocs[noc] = [noc_id, region] 
        nocs_writer.writerow([noc_id, noc, region])

for key in nocs:
    print(key, nocs[key][0], nocs[key][1])

nocs_data_file.close()

#USING athletes_events.csv

#dictionaries
athletes = {}
events = {}
games = {}

athlete_events_data_file = open('athlete_events.csv')
athlete_events_reader = csv.reader(athlete_events_data_file)

#all file writers
athletes_file = open('athletes.csv', 'w')
athletes_writer = csv.writer(athletes_file)

events_file = open('events.csv', 'w')
events_writer = csv.writer(events_file)

games_file = open('games.csv', 'w')
games_writer = csv.writer(games_file)

athletes_events_file = open('athletes_events.csv', 'w')
athletes_events_writer = csv.writer(athletes_events_file)

nocs_athletes_file = open('nocs_athletes.csv', 'w')
nocs_athletes_writer = csv.writer(nocs_athletes_file)

events_games_file = open('events_games.csv', 'w')
events_games_writer = csv.writer(events_games_file)

athletes_events_games_file = open('athletes_events_games.csv', 'w')
athletes_events_games_writer = csv.writer(athletes_events_games_file)


#helper functions

def add_athlete_entry(row, writer):
    athlete_id = row[0]

    full_name = row[1]

    #will only consider very last word to be surname

    name_components = full_name.split(' ')

    surname = name_components[-1]
    surname_index = -1

    if surname == 'Jr.' or surname.find('(') != -1 or surname == 'III':
        surname = name_components[-2] + ' ' + surname
        surname_index = -2

    #given name is the rest
    given_name = ''
    for component in name_components[:surname_index]:
        given_name += component + ' '
    given_name = given_name[:len(given_name) - 1] #eliminates final space after given name

    #handle nickname
    nickname = 'NA'
    if given_name.find('"') != -1:
        given_name_components = given_name.split('"')
        given_name = given_name_components[0].strip(' ')
        nickname = given_name_components[1].strip('"')
    
    if athlete_id not in athletes:
        athletes[athlete_id] = [surname, given_name, nickname]
        writer.writerow([athlete_id, surname, given_name, nickname])

def add_event_entry(row, writer):
    event_name = row[13]
    sport = row[12]
    if event_name not in events:
        event_id = len(events) + 1
        events[event_name] = [event_id, sport]
        writer.writerow([event_id, event_name, sport])

def add_games_entry(row, writer):
    #each key will be the year of the given Olympic games                                  
    games_year = row[9]
    season = row[10]
    city = row[11]
    if games_year not in games:
        games_id = len(games) + 1
        games[games_year] = [games_id, season, city]
        writer.writerow([games_id, games_year, season, city])

nocs_athletes = set() #set so it doesn't take forever to search
def add_nocs_athletes_entry(row, writer):
    noc = row[7]
    noc_id = nocs[noc][0]
    athlete_id = row[0]

    entry_to_add = [noc_id, athlete_id]

    if tuple(entry_to_add) not in nocs_athletes:
        writer.writerow(entry_to_add)
        nocs_athletes.add(tuple(entry_to_add))
        
def add_athletes_events_entry(row, writer):
    athlete_id = row[0]
    event_name = row[13]
    event_id = events[event_name][0]

    medal = row[14]

    writer.writerow([athlete_id, event_id, medal])

events_games = set()
def add_events_games_entry(row, writer):
    event_name = row[13]
    event_id = events[event_name][0]
    games_year = row[9]
    games_id = games[games_year][0]

    entry_to_add = [event_id, games_id]

    if tuple(entry_to_add) not in events_games:
        writer.writerow(entry_to_add)
        events_games.add(tuple(entry_to_add))

def add_athletes_events_games_entry(row, writer):

    athlete_id = row[0]
    event_name = row[13]
    medal = row[14]
    games_year = row[9]
    
    games_id = games[games_year][0]
    event_id = events[event_name][0]

    writer.writerow([athlete_id, event_id, games_id, medal])


#go through all in lines in athlete_events.csv (except first line)
heading_row = next(athlete_events_reader) #skip first line (from Jeff's example code)
for row in athlete_events_reader:

    #first, add new information to dictionaries & write to respective files
    
    add_athlete_entry(row, athletes_writer)

    add_event_entry(row, events_writer)

    add_games_entry(row, games_writer)

    add_nocs_athletes_entry(row, nocs_athletes_writer)

    add_athletes_events_entry(row, athletes_events_writer)

    add_events_games_entry(row, events_games_writer)

    add_athletes_events_games_entry(row, athletes_events_games_writer)

    '''
    athlete_id = row[0]
    event_name = row[13]
    event_id = events[event_name] # this is guaranteed to work by section (2)
    medal = row[14]
    writer.writerow([athlete_id, event_id, medal])
    '''

athlete_events_data_file.close()
athletes_file.close()
events_file.close()

#helper functions
'''
def add_athlete_entry(row, writer):
    athlete_id = row[0]

    full_name = row[1]
    #will only consider very last word to be surname
    name_split_index = full_name.rfind(' ')
    given_name = full_name[:name_split_index]
    surname = full_name[name_split_index + 1:]

    if athlete_id not in athletes:
        athletes[athlete_id] = [surname, given_name]
        writer.writerow([athlete_id, surname, given_name])

def add_event_entry(row, writer):
    event_name = row[13]
    sport = row[12]
    if event_name not in events:
        event_id = len(events) + 1
        events[event_name] = [event_id, sport]
        writer.writerow([event_id, event_name, sport])

def add_games_entry(row, writer):
    #each key will be the year of the given Olympic games
    games_year = row[9]
    season = row[10]
    city = row[11]
    if games_year not in games:
        games_id = len(games) + 1
        games[games_year] = [games_id, season, city]
        writer.writerow([games_id, games_year, season, city])

'''
