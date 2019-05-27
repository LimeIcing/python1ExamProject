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
import sys

file = open('SacramentocrimeJanuary2006.csv', 'r')
reader = csv.reader(file, delimiter=',')


def welcome():
    options = {
        '1': search
    }
    menu = '1 - Search for a crime in the archive\n' \
           '0 - Exit'

    print('Hello! Welcome to the Sacramento Police Database!\n'
          'How can I help you today?\n' + menu)
    selection = input()
    is_running = should_run(selection)
    while is_running:
        options[selection]()
        print('Is there anything else?\n' + menu)
        selection = input()
        is_running = should_run(selection)

    print('Thank you for using the Sacramento Police Database!')


def search():
    options = {
        '1': search_by_date,
        '2': search_by_address,
        '3': search_by_district,
        '4': search_by_beat,
        '5': search_by_grid,
        '6': search_by_description,
        '7': search_by_ucr_ncic,
        '8': search_by_radius
    }
    menu = '1 - Date and time\n' \
           '2 - Address\n' \
           '3 - District\n' \
           '4 - Beat\n5 - Grid\n' \
           '6 - Description\n' \
           '7 - UCR NCIC code\n' \
           '8 - Radius\n' \
           '0 - Go back to main menu...'

    print("You've chosen search! Please select what you wish to search by:\n" + menu)
    selection = input()
    is_running = should_run(selection)
    while is_running:
        options[selection]()
        print('Is there anything else you want to search for?\n' + menu)
        selection = input()
        is_running = should_run(selection)


def search_by_date():
    input_date = input('Please input date in this format: "MM/DD/YY"\n').split('/')
    if len(input_date[0]) < 1:
        print("You didn't input anything...")
        return

    search_date = ""
    d_i = 0
    # Formatting the input to work with the search function
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

    print('Searching for crimes registered on {0}...'.format(search_date))
    result_set = []
    file.seek(0)  # Resetting the iterator
    for row in reader:
        if str(row[0]).startswith(search_date):
            print(row)
            result_set.append(row)

    selection = input('Do you want to specify the search with a time of day? (y/N)\n')
    if selection == 'y':
        input_hour = input('Please input the hour in 24h time\n')
        for row in result_set:
            if str(row[0]).split(':')[0].endswith(input_hour):
                print(row)

    selection = input('Do you want to return to the previous menu? (Y/n)\n')
    if selection == 'n':
        sys.exit()


def search_by_address():
    address_abbreviations = {'AVENUE': 'AVE', 'BOULEVARD': 'BLVD', 'CENTER': 'CTR', 'CIRCLE': 'CIR', 'COURT': 'CT',
                             'DRIVE': 'DR', 'EXPRESSWAY': 'EXPY', 'HEIGHTS': 'HTS', 'HIGHWAY': 'HWY', 'ISLAND': 'IS',
                             'JUNCTION': 'JCT', 'LAKE': 'LK', 'LANE': 'LN', 'MOUNTAIN': 'MTN', 'PARKWAY': 'PKWY',
                             'PLACE': 'PL', 'PLAZA': 'PLZ', 'RIDGE': 'RDG', 'ROAD': 'RD', 'SQUARE': 'SQ',
                             'STREET': 'ST', 'STATION': 'STA', 'TERRACE': 'TER', 'TRAIL': 'TRL', 'TURNPIKE': 'TPKE',
                             'VALLEY': 'VLY',
                             'APARTMENT': 'APT', 'ROOM': 'RM', 'SUITE': 'STE',
                             'NORTH': 'N', 'EAST': 'E', 'SOUTH': 'WEST', 'NORTHEAST': 'NE', 'NORTHWEST': 'NW',
                             'SOUTHEAST': 'SE', 'SOUTHWEST': 'SW'}
    is_running = True

    input_address = input('Please input address\n').upper().split(' ')
    while is_running:
        i = 0
        for keyword in input_address:
            input_address[i] = keyword.replace('+', ' ')
            i += 1

        file.seek(0)  # Resetting the iterator
        for row in reader:
            for keyword in input_address:
                if list(row)[1].__contains__(keyword):
                    print(row)
                    break
                elif list(address_abbreviations.keys()).__contains__(keyword):
                    if list(row)[1].__contains__(address_abbreviations[keyword]):
                        print(row)
                        break

        selection = input('What do you want to do now?\n'
                          '1 - Widen current search'
                          '2 - Narrow current search'
                          '3 - Make a new address search'
                          '0 - Go back to the previous menu')
        if selection == '1':
            input_address.extend(input('Please input address\n').upper().split(' '))
        elif selection == '2':
            pass # TODO Make function to narrow address search
        elif selection == '3':
            input_address = input('Please input address\n').upper().split(' ')
        else:
            is_running = False


# TODO
def search_by_district():
    pass


# TODO
def search_by_beat():
    pass


# TODO
def search_by_grid():
    pass


# TODO
def search_by_description():
    pass


# TODO
def search_by_ucr_ncic():
    pass


# TODO
def search_by_radius():
    pass


# Helper function to exit menus
def should_run(user_input):
    if user_input == '0' or len(user_input) < 1:
        return False
    else:
        return True


if __name__ == '__main__':
    welcome()
