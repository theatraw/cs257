#Written by Thea Traw

import psycopg2
import config
import argparse


def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='Reports back specific info from Olympics database', add_help=False)
    parser.add_argument('--nocathletes', '-a',nargs='*', help='Print all athletes from a given NOC')
    parser.add_argument('--nocgolds', '-g',nargs='*', help='Print all nocs and their gold medal count')
    parser.add_argument('--podiumfinishers', '-p',nargs='*', help='Print all of the athletes who finished on the podium in a given event and Olympics year')
    parser.add_argument('--help', '-h','-?',action='store_true',help='Provides usage statements for each searching function')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def main():
    initialized_querier = Querier()
    arguments = get_parsed_arguments()
    
    if arguments.nocathletes is not None:
        initialized_querier.handle_nocathletes_call(arguments.nocathletes)
    elif arguments.nocgolds is not None:
        initialized_querier.handle_nocgolds_call()
    elif arguments.podiumfinishers is not None:
        initialized_querier.handle_podiumfinishers_call(arguments.podiumfinishers)
    elif arguments.help is not None:
        file = open('usage.txt', 'r')
        contents = file.read()
        print(contents)


    initialized_querier.close_connection()

class Querier:

    def __init__(self):

        try:
            self.connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)
            exit()

    def handle_nocathletes_call(self, noc_search_term):
        
        if len(noc_search_term) > 1:
            print('You have entered too many search terms')
            quit()
        if len(noc_search_term) == 0:
            print('Please enter a noc search term.')
        else:

            search_string = noc_search_term[0].upper()

            try:
                
                query = '''SELECT DISTINCT nocs.noc, athletes.surname, athletes.given_name, athletes.nickname, UPPER(athletes.surname) FROM athletes, nocs, nocs_athletes_events_games WHERE athletes.id = nocs_athletes_events_games.athlete_id AND nocs.id = nocs_athletes_events_games.noc_id AND nocs.noc = %s ORDER BY UPPER(athletes.surname);'''

                self.cursor.execute(query, (search_string,))

                print_heading_information = True
                for row in self.cursor:
                    if print_heading_information:
                        print('===Printing results for all of the athletes from {0}'.format(search_string)+'===')
                        print_heading_information = False
                    if row[3] == 'NA': #no nickname
                        print(row[1]+', '+row[2])
                    else:
                        print(row[1]+', '+row[2]+' "'+row[3]+'"')
            
            except Exception as e:
                print(e)
                quit()

    def handle_nocgolds_call(self):

        try:

            query = '''SELECT nocs.noc, COUNT(nocs_athletes_events_games.medal) FROM nocs, athletes, events, games, nocs_athletes_events_games WHERE nocs.id = nocs_athletes_events_games.noc_id AND athletes.id = nocs_athletes_events_games.athlete_id AND events.id = nocs_athletes_events_games.event_id AND games.id = nocs_athletes_events_games.games_id AND nocs_athletes_events_games.medal = 'Gold' GROUP BY nocs.noc ORDER BY COUNT(nocs_athletes_events_games.medal) DESC, nocs.noc;'''

            self.cursor.execute(query)

            print_heading_information = True
            for row in self.cursor:
                if print_heading_information:
                    print('===The total count of all gold medallions awarded to each NOC===')
                    print_heading_information = False
                if row[1] != 1:
                    print('Team '+row[0]+' has won '+ str(row[1])+' gold medals.')
                else:
                    print('Team '+row[0]+' has won '+str(row[1])+' gold medal.')
            print('All other teams have 0 gold medals.')

        except Exception as e:
            print(e)
            exit()

    def handle_podiumfinishers_call(self, arguments):

        if len(arguments) == 0 or len(arguments) > 3:
            print('Please enter proper search terms.')
        
        else:

            search_string_event = arguments[0]
            search_string_year = arguments[1]

            #catch type errors
            try:
                x = int(search_string_year)
            except ValueError:
                raise ValueError('sorry, invalid input') from None
                quit()
    
            try:
                #ORDER BY CASE from https://www.gab.lc/articles/order_by_custom_list/
                query = '''SELECT nocs.noc, athletes.surname, athletes.given_name, athletes.nickname, events.event, games.year, nocs_athletes_events_games.medal, games.season, games.city, UPPER(athletes.surname) FROM athletes, nocs, events, games, nocs_athletes_events_games WHERE athletes.id = nocs_athletes_events_games.athlete_id AND nocs.id = nocs_athletes_events_games.noc_id AND events.id = nocs_athletes_events_games.event_id AND games.id = nocs_athletes_events_games.games_id AND nocs_athletes_events_games.medal != 'NA' AND events.event LIKE %s AND games.year = %s ORDER BY CASE WHEN nocs_athletes_events_games.medal = 'Gold' THEN 1 WHEN nocs_athletes_events_games.medal = 'Silver' THEN 2 WHEN nocs_athletes_events_games.medal = 'Bronze' THEN 3 END, UPPER(athletes.surname);'''

                self.cursor.execute(query, (search_string_event, search_string_year))

                print_games_information_heading = True
                current_team_printing = '' #for when it's a team event, don't need to say NOC every time
                current_medal_printing = '' #multiple podium positions from same NOC
                for row in self.cursor:
                    if print_games_information_heading:
                        heading = '====Medaling athletes from the {0} in the {1} '+row[7]+' Olympics in '+row[8]+'===='
                        print(heading.format(search_string_event, search_string_year))
                        print_games_information_heading = False
                    if row[0] != current_team_printing or row[6] != current_medal_printing:
                        print('Team '+row[0]+', '+row[6])
                        current_team_printing = row[0]
                        current_medal_printing = row[6]
                    
                    if row[3] == 'NA': #no nickname
                        print('    '+row[1]+', '+row[2])
                    else:
                        print('    '+row[1]+', '+row[2]+' "'+row[3]+'"')


            except Exception as e:
                print(e)
                exit()

    def close_connection(self):
        self.connection.close()

if __name__ == '__main__':
    main()
