# In the application you should be able to search for crimes based on the data
#   in the different columns in the dataset.

# The application should be able to take a gps point (lon-lat) and return a
#   list of crimes made within a radius of 5 km.

# The data output should be readable (for normal users).

# The application should furthermore be able to add new records to the dataset.
#   (this includes writing to the csv file.)

# The application should be able to export the whole dataset into json and html
#   formats, and should be able to export search results in json and and html
#   formats as well.
import csv


def welcome():
    options = {
        '1': search
    }

    print('Hello! Welcome to the Sacramento Police Database!\n'
          'How can I help you today?\n'
          '1 - Search for a crime in the archive')
    options[input()]()


def search():
    options = {
        '1': search_by_date
    }
    print("You've chosen search! Please select what you wish to search for:\n"
          "1 - Search by date and time")
    options[input()]()


def search_by_date():
    print('Please input date in this format, using 24h time: MM/DD/YY/hh/mm')


if __name__ == '__main__':
    welcome()
