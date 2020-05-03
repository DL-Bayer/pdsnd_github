#!/usr/bin/python3

# code written in Linux-KDE-editor Kate and runs tested in bash

import time
import pandas as pd
import numpy as np

# city name and csv file definition
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# names of some months (locale independent) and a designation for all months ('all')
# this list is also used for the input processing
months = ['all', 'January', 'February', 'March', 'April', 'May', 'June']

# names of the weekdays (locale independent) and a designation for all weekdays ('all')
# this list is also used for the input processing
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    # subfunctions
    def request_list_element(request_description,list):
        """
        Definition of function "request_list_element" with 2 arguments.
        Prints 'request_description'. Then requests an element from
        the passed 'list' of strings. Ensures input element is part of
        the list.

        Args:
           (str) request_description: Descriptive text for the requested value.
           (lst of str) list: List of available alternatives / names to select from.

        Returns:
           (str) element: selected element

        """
        while True:
            print(request_description,'(', end = '')
            counter = 0
            for element in list:
                counter=counter+1
                print('"', element, '"', end = '', sep = '')
                if counter != len(list):
                    print(', ', end = '')
            print('): ', end = '')
            element = input().lower()
            if element in list:
                return element
            else:
                print('"', element, '" is not an available option. Please enter again.', sep = '')

 

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = request_list_element('Which city would you like to explore?', CITY_DATA.keys())

    # get user input for month (all, january, february, ... , june)
    month = request_list_element('Data of which month would you like to explore?', months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = request_list_element('Data of which day in the week would you like to explore?', days)

    print('-'*40)
    return city, month, day
    # city, month, day = local variables valid in scope of "get_filters()"


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Variables:
    # A) global variables with scope independent of any function: 
    #       1) CITY_DATA, 2) months, 3) days - as defined in first code bloc
    # B) local variable "city" (scope: main() ) hands over city-value according to filter
    # C) Here: local variable "city" (scope: load_data() ) is used (same for month, day)

    df = pd.read_csv(CITY_DATA[city])
    # read csv file of city into a Pandas DataFrame (using standard "read_csv")
    # Pandas root object defined as 'pd' above
    # file name derived from above defined "CITY_DATA"
    # CITY_DATA[city]: index call for "CITY_DATA" getting key = city names

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # returns column from csv when called - here column "Start Time"
    # in DataFrame object / df: index chosen according to column name in read_csv
    # pd.to_datetime: pandas standard (convert string in csv column into date-time-object to filter by date and time)
    # format example: 2017-06-23 15:09:32 from csv cannot be used 'as is' --> transform into usable format

    # if not 'all' months are selected, reduce 'df' to only the
    # "lines" of the 'month' (aka "filter")
    if month != 'all':
 #       print(month,'=', months.index(month)) # used for DEBUGGING
        df = df[df['Start Time'].dt.month == months.index(month)]
        # This statement about list index position is True: months[0]=='all' (all is in first (0) position in list)
        # df['Start Time'].dt.month: delivers integer number for month (1...6 for Jan...June)
        # months.index(month): delivers index number of month-name (for selected month-string)
        # [df['Start Time'].dt.month == months.index(month)]: index operator to match string-text to integer-index number
        # output: delivers "month" only ("Start Time" contains year, month, day, time down to seconds)
        # use Pandas-datetime object to deduct "sub-variable": month (from "Start Time" string)
        
    # "index()" should not 'Throw' 'ValueError' as the user input is
    # sanitized so 'month' should always be an item in 'months'
    # *** CAVEAT ***: dt.month runs between 1 (Monday) and 7 (Sunday)
    # in pandas 0.22 (and 1.0.1)
    # I.e. months.index(month) currently does not have to be re-indexed
    
    # if not 'all' weekdays are selected, reduce 'df' to only the
    # "lines" of the 'day' (aka "filter")
    if day != 'all':
#        print(day,'=', days.index(day)-1) # DEBUG
        df = df[df['Start Time'].dt.weekday == days.index(day) - 1]
        # see above explanation for month-DataFrame filtering: 
        # for weekdays we have index values 0...6 in Pandas datetime object (monday...sunday vs. months with 1...12)
        # that is why we need to subtract 1 to shift weekdays index
        # our index for weekdays runs from 1...7 (moday...sunday - as we have "all" in position 0)
        # whereas for months, "all" in position 0 spares us shifting "accidentally"
        # filtered df / DataFrame object handed back to main() function: df = load_data(city, month, day)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    # 'months' runs months[0]='january' to months[5]='june' and
    # dt.month returns 0 (January) to 5 (June), so no re-indexing is necessary

    print('The most common month is ', months[(df['Start Time'].dt.month).mode()[0]].capitalize(), '.', sep = '')
    # output formatting: .capitalize(), '.', and sep
    # months[] gets name of month (derived from index number, using global "months" (contains all, january,...))
    # Pandas "datetime" above delivers month as index-integer, here we convert into string-name to display name not number
    # mode(): sorts months by frequency with most frequent ascending
    # mode()[0]: pick 0th-element of return value from mode() to get most frequent element 

    # display the most common day of week

    # *** CAVEAT ***: 'days' runs days[1]='monday' to days[6]='sunday' and
    # 'dt.weekday' returns 0 (Monday) to 6 (Sunday), so re-indexing (+1)
    # is necessary
    print('The most common weekday is ', days[df['Start Time'].dt.weekday.mode()[0] + 1].capitalize(), '.', sep = '')
    # see description above for months - but for weekdays we need to shift index again
    # here we need to add 1 (instead of subtracting) because above we converted our 1...7 notation into 0...6 (datetime) 
    # and here we receive an output from datetime
    # in index format 0...6 and need to convert into our 1...7 index structure

    # display the most common start hour
    print('The most common hour of the day to start is ', df['Start Time'].dt.hour.mode()[0], ' o\'clock.', sep = '')
    # see logic for months and days - but NOT needed here: index shifting and integer to string look-up 
    # because output for hour is returned "as is" - as number from DataFrame column (0...23 hours)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is "', df['Start Station'].mode()[0], '".', sep = '')
    # see above - same logic as for trip-hours

    # display most commonly used end station
    print('The most commonly used end station is "', df['End Station'].mode()[0], '".', sep = '')
    # see above - same logic as for trip-hours

    # Display most frequent combination of start station and end station trip:

    # Method 1: 
#    print(('The most frequent combination of start station and end station trip is "' + df['Start Station'] + '" to "' + df['End Station'] + '"').mode()[0]+'.', sep = '')
    # is straightforward but least performant / slow operation: approx. 0.6 s
    # approach: 
    # addition of strings into one column in DataFrame and 
    # get most frequent value for new/joint string via mode()

    # Method 2: 
    # using df.groupby(), needs string manipulation but is faster: approx. 0.1 s
    print('The most frequent combination of start station and end station trip is ', str(df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1).index[0]).replace('(', '').replace(')', '').replace("'", '"').replace(',', ' to').strip(), '.', sep = '')

    # df.groupby: standard functionality of Pandas
    # df.groupby(['Start Station', 'End Station']): groups by combination of columns Start and End Station and delivers object
    # size(): counts frequency of (combined) values, default order is ascending --> to get most frequent we need ascending=False
    # head(1): delivers 1st line from top
    # .index[0]: delivers result as list and 0th-element in list
    # note: output from "size()" delivers 2 columns: 0 = name of combined Stations, 1 = frequency / count of combined stations
    # we need name only as output --> choose index[0] from this temporary variable output
    # to get readable output, the result object returned by "groupby / size() / head() / index" 
    # needs to be converted into string in format - raw returned format = 
    # ('Lake Shore Dr & Monroe St', 'Streeter Dr & Grand Ave') 
    # --> need to get rid of brackets (), apostrophes '', replace comma by "to", spaces via:
    # str(), replace, and strip
    # further formatting: '.', sep

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time of all selected trips is', df['Trip Duration'].sum(), 's.')
    # df['Trip Duration']: selects column 'Trip Duration' from DataFrame
    # use Pandas standard functions sum() and mean() for statistics
    # print() function with 3 arguments: 
    # 1) constant (The total travel time...)
    # 2) number-output: df[...].sum() - sum of column 'Trip Duration'
    # 3) space + string-constant "s" (for seconds)

    # display mean travel time
    print('The mean travel time per trip is {:.0f} s.'.format(df['Trip Duration'].mean()))
    # same logic as for sum()
    # mean displays high precicion - round by handing over mean-result to format-string {:.0f}
    # format is member-function of string-object
    # note: sum of Trip Duration does NOT need such action as output = full seconds
    # note: compare approach to int-solution for Birth Year, which truncates


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    print('Counts of User Type:\n', df['User Type'].value_counts(), sep = '')
    # print() function with 2 arguments: 
    # 1) constant (Counts of...)
    # 2) take column 'User Type' from df / DataFrame and run Pandas standard member-function value_counts() on it
    # formatting: \n used to enforce line break

    # Display counts of gender
    # else: handle cities without Gender columns in data set
    if 'Gender' in df:
        print('Total Gender count:\n', df['Gender'].value_counts(), sep = '')
    else:
        print('Gender information is not available for this city.')

    # Display earliest, most recent, and most common year of birth
    # else: handle cities without Birth Year information in data set
    if 'Birth Year' in df:
        print('Earliest birth year: ', int(df['Birth Year'].min()), sep = '')
        print('Most recent birth year: ', int(df['Birth Year'].max()), sep = '')
        print('Most common birth year: ', int(df['Birth Year'].mode()[0]), sep = '')
    else:
        print('Birth year information is not available for this city.')
        # note: it is NOT necessary to create local variables for earliest/recent/common
        # but one can directly add df[] as argument to print() function, which auto-delivers temporary variables
        # creating variables is only needed, if further operations are required on them 
        # (e.g. substacting earliest minus recent birth year)
        # in this case, one would add the name of the temporary variable as 2nd argument to print()
        # year values are float-point numbers (e.g. 1999.0) in raw data
        # to achieve precision as full years cast floats to integers via int() function
        # as no mathematical rounding is required (vs. mean travel time), int is sufficient (truncate values)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def interactive_output_raw_data(df):
    """ ask user if (s)he wants to output 10 lines of raw data of filtered DataFrame df, do so, ask user if (s)he wants 5 lines more """

    line = 0
    answer = input('Would you like to see 10 lines of the filtered raw data? Enter "yes" or "y" to continue, anything else to abort: ').lower()
    while answer == 'yes' or answer == 'y':
        endline = line + 10
        if endline < len(df):
            print(df.iloc[line:endline])
        else:
            print(df.iloc[line:len(df)])
            print('End of filtered raw data. No more lines to print.')
            return            
        line = endline
        answer = input('Would you like to see 10 more lines of the filtered raw data? Enter "yes" or "y" to continue, anything else to abort: ').lower()

        # line: local variable in scope of function interactive_output_raw_data(df))
        # answer: local variable set with input() function to display question-text string
        # lower(): set answer to lower case to avoid entry errors
        # endline: local variable as "line + 10" (to avoid changing "line" numbers in different places)
        # if + iloc: 
        # if variable endline is smaller or equal to number of DataFrame rows (calculated via len(df)) 
        # then print lines via using iloc()-function, which displays lines of Pandas DataFrame
        # as long as endline < size of DataFrame: print 10 lines
        # else: if end of DataFrame is reached:
        # print until end of DataFrame and display comment (End of filtered...)
        # line = endline: value after last iteration of while-loop, to re-start with new line-value in case user answers "yes" again

def main():
    while True:
        city, month, day = get_filters()
        # get filters according to input filters defined at beginning of code - see above
        df = load_data(city, month, day)
        # get data frame obbject via "df" / table used by Pandas - see "load_data" function above
        # DataFrame object contains filtered rows/values only due to above operations to then carry out statistics

#        print(df['Start Time'].to_string()) # used for DEBUG
#        print(df['Start Time'].dt.month) # used for DEBUG
#        print(df['Start Time'].dt.weekday) # usedfor DEBUG

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        interactive_output_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
