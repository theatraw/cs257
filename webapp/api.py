'''
    api.py
    Rodrick and Thea, 09 November 2021

'''
import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

@api.route('/help/')
def get_help():
    return flask.render_template('help.html')
#need to edit



@api.route('/<worldcup>/matches') 
def get_matches(worldcup):
    #tms = teams.split(",")
    teams = flask.request.args.get('teams')
    
    if (teams):
        tms = teams.split(",") 
    else:  
        tms = []
        tms.append('all')
    ylist = []
    yrs = worldcup.split(",")
    ylist = [int(i) for i in yrs]
    print(tms)
    print(ylist)
    #how do we want to identify matches...
    query = '''SELECT teams.team_abbreviation, teams.team_name, worldcups.year, matches.id
                FROM teams, worldcups, players_teams_matches_worldcups, matches
                WHERE players_teams_matches_worldcups.team_id = teams.id
                AND players_teams_matches_worldcups.worldcup_id = worldcups.id
                AND players_teams_matches_worldcups.match_id = matches.id
                ORDER BY teams.team_name;'''
    
    team_list = []
    ylist =[]
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query,)
        for row in cursor:
            if ( (row[1] in tms) or ('all' in tms)): 
                if(row[2] in ylist):
                    team = {
                        'Team Name':row[1],
                        'Abbreviation':row[0],
                        'Worldcup':row[2],
                        'Match':row[3]
                    }
                    
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

@api.route('/cups/<team>') 
def get_cups(team):
    tms = team.split(",")
    print(tms)
    query = '''SELECT teams.team_abbreviation, teams.team_name, worldcups.year, worldcups.firstplace
                FROM teams, worldcups, players_teams_matches_worldcups
                WHERE players_teams_matches_worldcups.team_id = teams.id
                 AND players_teams_matches_worldcups.worldcup_id = worldcups.id
                 
                ORDER BY worldcups.year;'''
    
    team_list = []
    ylist =[]
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query,)
        for row in cursor:
            if ( row[1] in tms):
                
                if( row[2] not in ylist):
                    team = {
                        'Team Name':row[1],
                        'Worldcup':row[2]
                    }
                    ylist.append(row[2])
                    team_list.append(team)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

#need to edit
@api.route('/medals') 
def get_medals():
    
    query = '''SELECT teams.team_abbreviation, teams.team_name, worldcups.year, worldcups.firstplace, worldcups.secoundplace,
                worldcups.thirdplace, worldcups.fourthplace
                FROM worldcups, players_teams_matches_worldcups, teams
                WHERE players_teams_matches_worldcups.team_id = teams.id
                 AND players_teams_matches_worldcups.worldcup_id = worldcups.id
                ORDER BY worldcups.year;'''
    team_list = []
    year_list = []

    years = flask.request.args.get('years')
    ylist = []
    if (years):
        yrs = years.split(",")
        ylist = [int(i) for i in yrs]
        print(ylist)
        
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query,)
        for row in cursor:
            
            if(row[2] in ylist):
                tvals = [value for elem in team_list
                        for value in elem.values()]
                if ( row[1] not in tvals):
                    team = {
                            'Team Name':row[1],
                            'Worldcup':row[2],
                            'Medals':0}
                    team_list.append(team)
                tvals = [value for elem in team_list
                        for value in elem.values()]
                if( row[2] not in year_list):
                    year_list.append(row[2])
                    if(row[3] not in tvals):
                        team = {
                                'Team Name':row[3],
                                'Worldcup':row[2],
                                'Medals':1}
                        team_list.append(team)
                    else:
                        tname = row[3]
                        for t in team_list:
                            if t['Team Name'] == tname:
                                t['Medals'] += 1
                    if(row[4] not in tvals):
                        team = {
                                'Team Name':row[4],
                                'Worldcup':row[2],
                                'Medals':1}
                        team_list.append(team)
                    else:
                        tname = row[4]
                        for t in team_list:
                            if t['Team Name'] == tname:
                                t['Medals'] += 1
                    if(row[5] not in tvals):
                        team = {
                                'Team Name':row[5],
                                'Worldcup':row[2],
                                'Medals':1}
                        team_list.append(team)
                    else:
                        tname = row[5]
                        for t in team_list:
                            if t['Team Name'] == tname:
                                t['Medals'] += 1
                    if(row[6] not in tvals):
                        team = {
                                'Team Name':row[6],
                                'Worldcup':row[2],
                                'Medals':1}
                        team_list.append(team)
                    else:
                        tname = row[6]
                        for t in team_list:
                            if t['Team Name'] == tname:
                                t['Medals'] += 1
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(team_list)

@api.route('/silver/teams/') 
def get_silver():
    query = '''SELECT teams.team_abbreviation, teams.team_name, worldcups.year, worldcups.secondplace
                FROM teams, worldcups, players_teams_matches_worldcups
                WHERE players_teams_matches_worldcups.team_id = teams.id
                 AND players_teams_matches_worldcups.worldcup_id = worldcups.id
                ORDER BY worldcups.year;'''
    team_list = []
    years = flask.request.args.get('years')
    tlist =[]
    ylist = []
    yr = []
    if (years):
        yrs = years.split(",")
        ylist = [int(i) for i in yrs]
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query,)
        for row in cursor:
            if(row[2] not in yr):                         
                if(row[2] in ylist):                   
                    if( row[3] == row[1]):
                        team = {'Abbreviation':row[0],
                                'Team Name':row[1],
                                'Worldcup':row[2]}
                        team_list.append(team)

                        yr.append(row[2])
                
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(team_list)

@api.route('/bronze/teams/') 
def get_bronze():
    query = '''SELECT teams.team_abbreviation, teams.team_name, worldcups.year, worldcups.thirdplace
                FROM teams, worldcups, players_teams_matches_worldcups
                WHERE players_teams_matches_worldcups.team_id = teams.id
                 AND players_teams_matches_worldcups.worldcup_id = worldcups.id
                ORDER BY worldcups.year;'''
    team_list = []
    years = flask.request.args.get('years')
    tlist =[]
    ylist = []
    yr = []
    if (years):
        yrs = years.split(",")
        ylist = [int(i) for i in yrs]
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query,)
        for row in cursor:
            if(row[2] not in yr):                         
                if(row[2] in ylist):                   
                    if( row[3] == row[1]):
                        team = {'Abbreviation':row[0],
                                'Team Name':row[1],
                                'Worldcup':row[2]}
                        team_list.append(team)

                        yr.append(row[2])
                
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(team_list)

@api.route('/gold/teams/') 
def get_gold():
    
    query = '''SELECT teams.team_abbreviation, teams.team_name, worldcups.year, worldcups.firstplace
                FROM teams, worldcups, players_teams_matches_worldcups
                WHERE players_teams_matches_worldcups.team_id = teams.id
                 AND players_teams_matches_worldcups.worldcup_id = worldcups.id
                ORDER BY worldcups.year;'''
    team_list = []
    years = flask.request.args.get('years')
    tlist =[]
    ylist = []
    yr = []
    if (years):
        yrs = years.split(",")

        ylist = [int(i) for i in yrs]
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query,)
        for row in cursor:
            if(row[2] not in yr):                         
                if(row[2] in ylist):                   
                    if( row[3] == row[1]):
                        team = {'Abbreviation':row[0],
                                'Team Name':row[1],
                                'Worldcup':row[2]}
                        team_list.append(team)

                        yr.append(row[2])
                
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(team_list)


@api.route('/Allcups/teams/') 
def get_all_teams():
    
    query = '''SELECT teams.team_abbreviation, teams.team_name, teams.id 
                FROM teams ORDER BY teams.team_name;'''

    # sort_argument = flask.request.args.get('sort')
    # if sort_argument == 'birth_year':
    #     query += 'birth_year'
    # else:
    #     query += 'surname, given_name'
    #query += 'team_name'
    
    team_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            team = {  'team_abbreviation':row[0],
                      'team_name':row[1],
                      'id':row[2]}
            team_list.append(team)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(team_list)


@api.route('/medals/<year>/') 
def get_all_medals(year):
    ylist = []
    yrs = year.split(',')
    ylist = [int(i) for i in yrs]
    query = '''SELECT DISTINCT worldcups.year, worldcups.firstplace, worldcups.secoundplace, worldcups.thirdplace, worldcups.id
                FROM worldcups
                ORDER BY worldcups.year;'''
    medal_list = []
    try:
        
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (year,))
        for row in cursor:
            if(row[0] in ylist):
                podium = {'year':row[0],  'wc_id':row[4], 'firstplace':row[1], 'secondplace':row[2], 'thirdplace':row[3]}
                medal_list.append(podium)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(medal_list)







@api.route('/Allcups/')
def get_all_worldcups():
    
    query = '''SELECT worldcups.year, worldcups.location, worldcups.id FROM worldcups ORDER BY worldcups.year;'''

    wc_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        
        for row in cursor:
            
            wc = {  'wc_year':row[0],
                    'wc_location':row[1],
                    'wc_id':row[2]}
            wc_list.append(wc)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(wc_list)


@api.route('/<years>/teams/') 
def get_teams_by_year(years):
    # print(years)
    ylist = []
    yrs = years.split(',')
    ylist = [int(i) for i in yrs]
    query = '''SELECT DISTINCT teams.team_abbreviation, teams.team_name, worldcups.year, worldcups.id, teams.id
               FROM worldcups, teams, players_teams_matches_worldcups
               WHERE players_teams_matches_worldcups.team_id = teams.id
                 AND players_teams_matches_worldcups.worldcup_id = worldcups.id
               ORDER BY worldcups.year'''
    team_list = []
    tms = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (years,))
        for row in cursor:
            
            if ((row[2] in ylist) and (row[0] not in tms)):
                team = {'year':row[2], 'team_abbreviation':row[0], 'team_name':row[1], 'wc_id':row[3], 'team_id':row[4]}
                team_list.append(team)
                tms.append(row[0])
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(team_list)


@api.route('/Allcups/<team>/cups/')
def get_team_worldcups(team):

    query = '''SELECT DISTINCT worldcups.year, worldcups.location, worldcups.id 
FROM worldcups, teams, players_teams_matches_worldcups 
WHERE players_teams_matches_worldcups.worldcup_id = worldcups.id
AND players_teams_matches_worldcups.team_id = teams.id
AND teams.id = %s
ORDER BY worldcups.year;'''

    wc_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (team,))
        for row in cursor:
            wc = {  'wc_year':row[0],
                    'wc_location':row[1],
                    'id':row[2]}
            wc_list.append(wc)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(wc_list)

@api.route('/<year>/<team>/roster') 
def get_players(year, team):
    # print(year)
    # print(team)
    # tms = team.split(",")
    # ylist = []
    # yrs = year.split(",")
    # ylist = [int(i) for i in yrs]
    query = '''SELECT DISTINCT players.surname, players.given_name, players.id
               FROM worldcups, teams, players_teams_matches_worldcups, players
               WHERE players_teams_matches_worldcups.team_id = teams.id
                 AND players_teams_matches_worldcups.worldcup_id = worldcups.id
                 AND players_teams_matches_worldcups.player_id = players.id
                     AND teams.id = %s
                AND worldcups.year = %s
                 

               ORDER BY players.surname;'''
    player_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (team, year))
        for row in cursor:
            # if ( (row[1] in tms) and (row[2] in ylist) ):
            player = {'surname':row[0], 'given_name':row[1], 'id':row[2]}
            player_list.append(player)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(player_list)



@api.route('/allmatches/<year>')
def get_all_matches(year):

    query = '''SELECT DISTINCT  matches.id, matches.date_time, matches.stage, matches.stadium,
           matches.city, matches.home_team, matches.home_score, matches.away_team, 
           matches.away_score, matches.home_first_half_goals, 
           matches.home_second_half_goals, matches.away_first_half_goals, 
           matches.away_second_half_goals
           FROM matches, worldcups, players_teams_matches_worldcups 
           WHERE matches.id = players_teams_matches_worldcups.match_id
           AND worldcups.id = players_teams_matches_worldcups.worldcup_id
           AND worldcups.year = %s
           ORDER BY matches.date_time;'''
    
    match_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (year,))
        for row in cursor:
            match = {'match_id':row[0],
                      'date':row[1],
                      'stage':row[2],
                      'stadium':row[3],
                      'city':row[4],
                      'home_team':row[5],
                      'home_score':row[6],
                      'away_team':row[7],
                      'away_score':row[8],
                      'home_first_half_score':row[9],
                      'home_second_half_score':row[10],
                      'away_first_half_score':row[11],
                      'away_second_half_score':row[12]}
            match_list.append(match)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return json.dumps(match_list)

    










@api.route('/<teams>/players/') 
def get_players1():
    ''' Returns a list of all the authors in our database. See
        get_author_by_id below for description of the author
        resource representation.
        By default, the list is presented in alphabetical order
        by surname, then given_name. You may, however, use
        the GET parameter sort to request sorting by birth year.
            http://.../authors/?sort=birth_year
        Returns an empty list if there's any database failure.
    '''

    query = '''SELECT players.playerid, players.tmid, players.firstname, players.lastname, players.captain, players.starter, 
                teams.team_abbreviation, players.pnumber, players.position
               FROM players, teams 
               WHERE teams.teamid = players.tmid
               AND teams.year = %s
               ORDER BY teams.team_abbreviation'''

    # sort_argument = flask.request.args.get('sort')
    # if sort_argument == 'birth_year':
    #     query += 'birth_year'
    # else:
    #     query += 'surname, given_name'
    query += 'lastname, surname'
    
    player_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, teams)
        for row in cursor:
            player = {'plaerid':row[0],
                      'tmid':row[1],
                      'firstname':row[2],
                      'lastname':row[3],
                      'captain':row[4],
                      'starter':row[4],
                      'team_abbreviation':row[5],
                      'number':row[6],
                      'position':row[7]}
            player_list.append(player)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(player_list)

@api.route('/Allcups/attendance')
def get_attendance():

    query = '''SELECT worldcups.attendance, worldcups.year 
                FROM worldcups ORDER BY worldcups.year;'''
    attendance_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            wc = {  'attendance':row[0],
                      'year':row[1]}
            attendance_list.append(wc)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return json.dumps(attendance_list)
