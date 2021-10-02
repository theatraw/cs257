#This is code by Lysander Miller and Thea Traw

import argparse
import booksdatasource

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='Sorts books and authors')
    parser.add_argument('searchterms', metavar='search', nargs='+', help='search function--put in your search term here')
    parser.add_argument('--titles', '-t', default='--titles', help='sort by titles')
    parser.add_argument('--authors', '-a', default=None,  help='sort by authors')
    parser.add_argument('--years', '-y', default=None, help='sort by years')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def main():
    arguments = get_parsed_arguments()
    print(arguments)
    print(len(arguments.titles))
    for title in arguments.titles:
        #FIX THIS LATER
        print("HIOI")
        print(booksdatasource.BooksDataSource.books(title, "year"))
    for author in arguments.authors:
        print(booksdatasource.BooksDataSource.authors(author))
    print(booksdatasource.BooksDataSource.books_between_years(arguments.years[0], arguments.years[1]))

if __name__ == '__main__':
    main()
