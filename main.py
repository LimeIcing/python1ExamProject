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

reader = csv.reader(open('SacramentocrimeJanuary2006.csv'), delimiter=',')


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
    print("You've chosen search! Please select what you wish to search by:\n"
          "1 - Date and time\n"
          "2 - Address\n"
          "3 - District\n"
          "4 - Beat\n"
          "5 - Grid\n"
          "6 - Description\n"
          "7 - UCR NCIC code\n"
          "8 - Radius"
          "0 - Go back...")
    options[input()]()


def search_by_date():
    input_date = input('Please input date in this format: "MM/DD/YY"\n')
    input_date = input_date.split('/')

    search_date = ""
    d_i = 0
    for i in input_date:
        if d_i < 2:
            if i[0] == '0':
                search_date += i[1]
            else:
                search_date += i
            search_date += '/'
            d_i += 1
        else:
            if len(i) == 1:
                search_date += ('0' + i)
            else:
                search_date += i

    print('Searching for crimes registered on {0}'.format(search_date))

    for row in reader:
        if str(row[0]).startswith(search_date):
            print(row)


def search_by_address():
    pass


def search_by_district():
    pass


def search_by_beat():
    pass


def search_by_grid():
    pass


def search_by_description():
    pass


def search_by_ucr_ncic():
    pass


def search_by_radius():
    pass


if __name__ == '__main__':
    welcome()
