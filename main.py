import os
import csv
import json

file = open('SacramentocrimeJanuary2006.csv', 'r')
fieldnames = ['cdatetime', 'address', 'district', 'beat', 'grid',
              'crimedescr', 'ucr_ncic_code', 'latitude', 'longitude']
reader = csv.DictReader(file, delimiter=',', fieldnames=fieldnames)


def welcome():
    options = {
        '1': search,
        '2': new_entry,
        '3': export_to_json,
        '4': export_to_html
    }
    menu = '1 - Search for a crime in the archive\n' \
           '2 - Add a new record to the database\n' \
           '3 - Export the database to JSON\n' \
           '4 - Export the database to HTML\n' \
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
    file.close()


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

        print(f'Searching for crimes registered on {search_date}...')
        result_set = []
        file.seek(0)  # Resetting the iterator
        for row in reader:
            if str(row[fieldnames[0]]).startswith(search_date):
                print(json.dumps(row, indent=4))
                result_set.append(row)

        selection = input('Do you want to specify the search with a time of day? (y/N)\n')
        if selection.lower() == 'y':
            input_hour = input('Please input the hour in 24h time\n')
            for row in result_set:
                if str(row[fieldnames[0]]).split(':')[0].endswith(input_hour):
                    print(json.dumps(row, indent=4))

        selection = input('Do you want to search for a new date? (y/N)\n')
        if selection.lower() != 'y':
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
                if row[fieldnames[1]].__contains__(keyword):
                    print(json.dumps(row, indent=4))
                    break
                elif list(address_abbreviations.keys()).__contains__(keyword):
                    if row[fieldnames[1]].__contains__(address_abbreviations[keyword]):
                        print(json.dumps(row, indent=4))
                        break

        selection = input('What do you want to do now?\n'
                          '1 - Widen current search\n'
                          '2 - Narrow current search (NOT AVAILABLE IN DEMO)\n'
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
            if row[fieldnames[2]] == input_district:
                print(json.dumps(row, indent=4))

        selection = input('Do you wish to search in another district? (y/N)\n')
        if selection.lower() != 'y':
            is_running = False


def search_by_beat():
    is_running = True

    while is_running:
        input_beat = input('Please input beat\n').upper()
        file.seek(0)  # Resetting the iterator
        for row in reader:
            if str(row[fieldnames[3]]).startswith(input_beat):
                print(json.dumps(row, indent=4))

        selection = input('Do you wish to search for another beat? (y/N)\n')
        if selection.lower() != 'y':
            is_running = False


def search_by_grid():
    is_running = True

    while is_running:
        input_grid = input('Please input grid number\n')
        file.seek(0)  # Resetting the iterator
        for row in reader:
            if row[fieldnames[4]] == input_grid:
                print(json.dumps(row, indent=4))

        selection = input('Do you wish to search in another grid? (y/N)\n')
        if selection.lower() != 'y':
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
                if row[fieldnames[5]].__contains__(keyword):
                    print(json.dumps(row, indent=4))
                    break

        selection = input('What do you want to do now?\n'
                          '1 - Widen current search\n'
                          '2 - Narrow current search (NOT AVAILABLE IN DEMO)\n'
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
            if row[fieldnames[6]] == input_ucr:
                print(json.dumps(row, indent=4))

        selection = input('Do you wish to search for another UCR number? (y/N)\n')
        if selection.lower() != 'y':
            is_running = False


def search_by_radius():
    is_running = True

    input_coordinate = input('Please input a coordinate separated by a comma (latitude,longitude)\n').split(',')
    input_radius = float(input('Please input desired radius in miles\n')) * 0.0145  # converts miles to long/lat
    while is_running:
        file.seek(0)  # Resetting the iterator
        file.__next__()  # Avoids the header row
        for row in reader:
            if float(row[fieldnames[7]]) - float(input_coordinate[0]) <= input_radius and \
                    float(input_coordinate[0]) - float(row[fieldnames[7]]) <= input_radius:
                if float(row[fieldnames[8]]) - float(input_coordinate[1]) <= input_radius and \
                        float(input_coordinate[1]) - float(row[fieldnames[8]]) <= input_radius:
                    print(json.dumps(row, indent=4))

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


# TODO Test for crashes via invalid input
def new_entry():
    file_write = open('SacramentocrimeJanuary2006.csv', 'a', newline='')
    writer = csv.DictWriter(file_write, delimiter=',', fieldnames=fieldnames)
    base_query = 'Please input {0}\n'
    base_example = 'Ex.: "{0}"\n'
    base_confirmation = 'Is this the correct {0} (Y/n)? {1}\n'
    new_row = {}

    is_unconfirmed = True
    while is_unconfirmed:
        date_fragment_list = [input(base_query.format('month')).upper() + '/',
                              input(base_query.format('day of month')) + '/',
                              input(base_query.format('year')) + ' ',
                              input(base_query.format('hour')) + ':',
                              input(base_query.format('minute'))]

        date = format_date(date_fragment_list)
        selection = input(base_confirmation.format('date', date))
        if selection.lower() != 'n':
            is_unconfirmed = False
            new_row['cdatetime'] = date

    is_unconfirmed = True
    while is_unconfirmed:
        address = input(base_query.format('address') + base_example.format('3421 AUBURN BLVD')).upper()
        selection = input(base_confirmation.format('address', address))
        if selection.lower() != 'n':
            is_unconfirmed = False
            new_row['address'] = address

    is_unconfirmed = True
    while is_unconfirmed:
        district = input(base_query.format('district number') + base_example.format('2'))
        selection = input(base_confirmation.format('district', district))
        if selection.lower() != 'n':
            is_unconfirmed = False
            new_row['district'] = district

    is_unconfirmed = True
    while is_unconfirmed:
        beat = input(base_query.format('beat') + base_example.format('2A')).upper()
        selection = input(base_confirmation.format('beat', beat))
        if selection.lower() != 'n':
            is_unconfirmed = False
            new_row['beat'] = beat + '        '

    is_unconfirmed = True
    while is_unconfirmed:
        grid = input(base_query.format('grid') + base_example.format('508'))
        selection = input(base_confirmation.format('grid', grid))
        if selection.lower() != 'n':
            is_unconfirmed = False
            new_row['grid'] = grid

    is_unconfirmed = True
    while is_unconfirmed:
        description = input(base_query.format('a description') +
                            base_example.format('459 PC  BURGLARY-UNSPECIFIED')).upper()
        selection = input(base_confirmation.format('description', description))
        if selection.lower() != 'n':
            is_unconfirmed = False
            new_row['crimedescr'] = description

    is_unconfirmed = True
    while is_unconfirmed:
        ucr = input(base_query.format('UCR number') + base_example.format('2299'))
        selection = input(base_confirmation.format('UCR number', ucr))
        if selection.lower() != 'n':
            is_unconfirmed = False
            new_row['ucr_ncic_code'] = ucr

    is_unconfirmed = True
    while is_unconfirmed:
        coordinates = input(base_query.format('coordinates, latitude first')
                            + base_example.format('38.6374478,-121.3846125'))
        selection = input(f'Are these the correct coordinates (Y/n)? {coordinates}\n')
        if selection.lower() != 'n':
            is_unconfirmed = False
            coordinates = coordinates.split(',')
            new_row['latitude'] = coordinates[0]
            if coordinates[1][0] == ' ':
                new_row['longitude'] = coordinates[1][1:]
            else:
                new_row['longitude'] = coordinates[1]

    is_unconfirmed = True
    while is_unconfirmed:
        selection = input(f'Is this record correct (y/N)? {new_row}\n')
        if selection.lower() == 'y':
            is_unconfirmed = False
            writer.writerow(new_row)
            print('Record stored in the system!')
        else:
            # TODO Make a system to edit a specific value instead of just cancelling
            selection = input('Are you sure you want to cancel (y/N)? Unsaved data will be lost\n')
            if selection.lower() == 'y':
                is_unconfirmed = False

    file_write.close()


def export_to_json():
    remove_header_from_csv()
    file_to_json = open('noHeader.csv', 'r')
    dict_reader = csv.DictReader(file_to_json, delimiter=',', fieldnames=fieldnames)
    out = json.dumps([row for row in dict_reader], indent=4)
    json_file = open('SacramentoCrimeDB.json', 'w')
    json_file.write(out)
    file_to_json.close()
    print('CSV file exported to JSON!')
    os.remove('noHeader.csv')


def export_to_html():
    file.seek(0)
    file.__next__()
    html = '<table>\n' \
           '  <tr>\n' \
        f'    <th>{fieldnames[0]}</th>\n' \
        f'    <th>{fieldnames[1]}</th>\n' \
        f'    <th>{fieldnames[2]}</th>\n' \
        f'    <th>{fieldnames[3]}</th>\n' \
        f'    <th>{fieldnames[4]}</th>\n' \
        f'    <th>{fieldnames[5]}</th>\n' \
        f'    <th>{fieldnames[6]}</th>\n' \
        f'    <th>{fieldnames[7]}</th>\n' \
        f'    <th>{fieldnames[8]}</th>\n' \
           '  </tr>\n'

    for row in reader:
        html += '  <tr>\n' \
            f'    <td>{row[0]}</td>\n' \
            f'    <td>{row[1]}</td>\n' \
            f'    <td>{row[2]}</td>\n' \
            f'    <td>{row[3]}</td>\n' \
            f'    <td>{row[4]}</td>\n' \
            f'    <td>{row[5]}</td>\n' \
            f'    <td>{row[6]}</td>\n' \
            f'    <td>{row[7]}</td>\n' \
            f'    <td>{row[8]}</td>\n' \
            '  </tr>\n'

    html += '</table>\n'
    html_file = open('SacramentoCrimeDB.html', 'w')
    html_file.write(html)
    html_file.close()
    print('CSV file exported to HTML!')


# Helper function to format the date
def format_date(date_fragment_list):
    months = {'JANUARY': '1', 'FEBRUARY': '2', 'MARCH': '3', 'APRIL': '4', 'MAY': '5', 'JUNE': '6', 'JULY': '7',
              'AUGUST': '8', 'SEPTEMBER': '9', 'OCTOBER': '10', 'NOVEMBER': '11', 'DECEMBER': '12'}

    if len(date_fragment_list[0]) > 3:
        date_fragment_list[0] = months[date_fragment_list[0][:-1]] + '/'
    elif date_fragment_list[0][0] == '0':
        date_fragment_list[0] = date_fragment_list[0][1:]

    if len(date_fragment_list[1]) > 3:
        date_fragment_list[1] = date_fragment_list[1][:2] + '/'

    if len(date_fragment_list[2]) > 3:
        date_fragment_list[2] = date_fragment_list[2][-3:]

    if len(date_fragment_list[3]) > 3:
        if date_fragment_list[3][:2] == '12':
            if date_fragment_list[3][-3:].upper() == 'AM:':
                date_fragment_list[3] = '0:'
            elif date_fragment_list[3][-3:].upper() == 'PM:':
                date_fragment_list[3] = '12:'
        elif date_fragment_list[3][-3:].upper() == 'AM:':
            if date_fragment_list[3].__contains__(' '):
                date_fragment_list[3] = date_fragment_list[3][:-4] + ':'
            else:
                date_fragment_list[3] = date_fragment_list[3][:-3] + ':'
        elif date_fragment_list[3][-3:].upper() == 'PM:':
            if date_fragment_list[3].__contains__(' '):
                date_fragment_list[3] = str(int(date_fragment_list[3][:-4]) + 12) + ':'
            else:
                date_fragment_list[3] = str(int(date_fragment_list[3][:-3]) + 12) + ':'
        if len(date_fragment_list[3]) == 3 and date_fragment_list[3][0] == '0':
            date_fragment_list[3] = date_fragment_list[3][1:]

    if len(date_fragment_list[4]) == 1:
        date_fragment_list[4] = '0' + date_fragment_list[4]

    date = ''
    for fragment in date_fragment_list:
        date += fragment

    return date


# Helper function to exit menu loops
def should_run(user_input):
    if user_input == '0' or len(user_input) < 1:
        return False
    else:
        return True


def remove_header_from_csv():
    no_header = open('noHeader.csv', 'a')
    writer = csv.writer(no_header, delimiter=',')
    file.seek(0)
    file.__next__()

    for row in reader:
        writer.writerow(row)

    no_header.close()


if __name__ == '__main__':
    welcome()
