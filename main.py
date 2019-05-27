# In the application you should be able to search for crimes based on the data
#   in the different columns in the dataset.

# The application should be able to take a gps point (lon-lat) and return a
#   list of crimes made within a radius of 5 km.

# TODO The data output should be readable (for normal users).

# TODO The application should furthermore be able to add new records to the dataset.
#   (this includes writing to the csv file.)

# TODO The application should be able to export the whole dataset into json and html
#   formats, and should be able to export search results in json and and html
#   formats as well.

import csv

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
        print('Is there anything else you want to do?\n' + menu)
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
        '7': search_by_ucr,
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
    is_running = True

    while is_running:
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

        selection = input('Do you want to search for a new date? (y/N)\n')
        if selection != 'y':
            is_running = False


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
                          '1 - Widen current search\n'
                          '2 - Narrow current search\n'
                          '3 - Make a new address search\n'
                          '0 - Go back to the previous menu\n')
        if selection == '1':
            input_address.extend(input('Please input additional search terms\n').upper().split(' '))
        elif selection == '2':
            pass  # TODO Make function to narrow address search
        elif selection == '3':
            input_address = input('Please input address\n').upper().split(' ')
        else:
            is_running = False


def search_by_district():
    is_running = True

    while is_running:
        input_district = input('Please input district number\n')
        file.seek(0)  # Resetting the iterator
        for row in reader:
            if list(row)[2] == input_district:
                print(row)

        selection = input('Do you wish to search in another district? (y/N)\n')
        if selection != 'y':
            is_running = False


def search_by_beat():
    is_running = True

    while is_running:
        input_beat = input('Please input beat\n').upper()
        file.seek(0)  # Resetting the iterator
        for row in reader:
            if list(row)[3] == input_beat:
                print(row)

        selection = input('Do you wish to search for another beat? (y/N)\n')
        if selection != 'y':
            is_running = False


def search_by_grid():
    is_running = True

    while is_running:
        input_grid = input('Please input grid number\n')
        file.seek(0)  # Resetting the iterator
        for row in reader:
            if list(row)[4] == input_grid:
                print(row)

        selection = input('Do you wish to search in another grid? (y/N)\n')
        if selection != 'y':
            is_running = False


def search_by_description():
    is_running = True

    input_description = input('Please input search terms\n').upper().split(' ')
    while is_running:
        i = 0
        for keyword in input_description:
            input_description[i] = keyword.replace('+', ' ')
            i += 1

        file.seek(0)  # Resetting the iterator
        for row in reader:
            for keyword in input_description:
                if list(row)[5].__contains__(keyword):
                    print(row)
                    break

        selection = input('What do you want to do now?\n'
                          '1 - Widen current search\n'
                          '2 - Narrow current search\n'
                          '3 - Make a new description search\n'
                          '0 - Go back to the previous menu\n')
        if selection == '1':
            input_description.extend(input('Please input additional search terms\n').upper().split(' '))
        elif selection == '2':
            pass  # TODO Make function to narrow description search
        elif selection == '3':
            input_description = input('Please input address\n').upper().split(' ')
        else:
            is_running = False


def search_by_ucr():
    is_running = True

    while is_running:
        input_ucr = input('Please input UCR number\n')
        file.seek(0)  # Resetting the iterator
        for row in reader:
            if list(row)[6] == input_ucr:
                print(row)

        selection = input('Do you wish to search for another UCR number? (y/N)\n')
        if selection != 'y':
            is_running = False


def search_by_radius():
    is_running = True

    input_coordinate = input('Please input a coordinate separated by a comma (latitude,longitude)\n').split(',')
    input_radius = float(input('Please input desired radius in miles\n')) * 0.0145  # converts miles to long/lat
    while is_running:
        file.seek(0)  # Resetting the iterator
        file.__next__()  # Avoids the header row
        for row in reader:
            if float(row[7]) - float(input_coordinate[0]) <= input_radius and \
                    float(input_coordinate[0]) - float(row[7]) <= input_radius:
                if float(row[8]) - float(input_coordinate[1]) <= input_radius and \
                        float(input_coordinate[1]) - float(row[8]) <= input_radius:
                    print(row)

        selection = input('What do you want to do now?\n'
                          '1 - Input new coordinate\n'
                          '2 - Adjust radius\n'
                          '0 - Go back to the previous menu\n')
        if selection == '1':
            input_coordinate = input('Please input a coordinate separated by a comma (latitude,longitude)\n').split(',')
        elif selection == '2':
            input_radius = float(input('Please input desired radius in miles\n')) * 0.0145  # converts miles to long/lat
        else:
            is_running = False


# Helper function to exit menus
def should_run(user_input):
    if user_input == '0' or len(user_input) < 1:
        return False
    else:
        return True


if __name__ == '__main__':
    welcome()
