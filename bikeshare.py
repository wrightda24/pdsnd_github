import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june',]
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',]
filters = ['month', 'day', 'none', 'both']
checks = ['yes', 'no']

city = 'none'
month = 'all'
day = 'all'


def key_and_count(column):
    '''
    Calculates the value counts for a given column, returns the highest count and its corresponding key
    '''
    global count, key
    count = column.value_counts().tolist()[0]
    key = column.value_counts().keys().tolist()[0]
    return(key, count)

def get_month():
    '''
    Gets the month the user would like to filter the data by
    '''
    month = input('\nWhich month would you like to dive into? (January, February, March, April, May, or June)\n').lower()
    while month not in months:
        month = input('Please enter a valid month.\n').lower()
    # Converts from month name to month number
    month = months.index(month) + 1
    return(month)

def get_day():
    '''
    Gets the day of the week the user would like to filter the data by
    '''
    day = input('\nWhat day of the week would you like to know about?\n').lower()
    while day not in days:
        day = input('Please enter a valid day.\n').lower()
    # Converts from day name to day number
    day = days.index(day)
    return(day)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Asks the user for a city to explor data in.
    city = input('What city would you like to explor New York City, Chicago, or Washington?\n').lower()
    while city not in cities:
        city = input('Please enter a valit city.\n').lower()

    # Asks the user if they would like to filter the data by month, day, none, or both
    filter_check = input('\nWould you like to filter by month, day, none, or both?\n').lower()
    while filter_check not in filters:
        filter_check = input('Please enter a valid filter.\n').lower()

    # If the user wants to filter by month, this finds out which month
    if filter_check == 'month':
        month = get_month()
        day = 'all'

    # If the user wants to filter by both month and day, this finds out which day and month
    elif filter_check == 'both':
        month = get_month()
        day = get_day()

    #If the user wants to filter by day, this finds out which day
    elif filter_check == 'day':
        day = get_day()
        month = 'all'

    # This is run if the user does not want to filter by either month or day
    elif filter_check == 'none':
        month = 'all'
        day = 'all'

    print('-'*40)
    print('\n')
    return(city, month, day)


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
    # Creates a DataFrame from the appropriate file in CITY_DATA
    city_file = pd.read_csv(CITY_DATA[city])
    df = pd.DataFrame(city_file)
    # Converts the column Start Time to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Creates a month column
    df['Month'] = df['Start Time'].dt.month
    # Creates day of week column
    df['Day_Of_Week'] = df['Start Time'].dt.dayofweek
    # Creates hour column
    df['Start Hour'] = df['Start Time'].dt.hour

    # Filters the data by the user specified month
    if month != 'all':
       df = df.loc[df['Month'] == month]

    # Filters the data by the user specified day of the week
    if day != 'all':
        df = df.loc[df['Day_Of_Week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # If the user did not want to filter by month, this displays the most common month
    if month == 'all':
        # Gets the most common month and its usage count
        pop_month, pop_month_count = key_and_count(df['Month'])

        print('\nThe most common month is {} with a usage of {}.'.format(pop_month, pop_month_count))

    # If the user did not want to filter by day, this gets the most common day
    if day == 'all':
        # Gets the most common day and its usage count
        pop_day, pop_day_count = key_and_count(df['Day_Of_Week'])

        print('\nThe most common day is {} with a count of {}.'.format(pop_day, pop_day_count))

    # Gets the most common start hour and its usage count
    pop_hour, pop_hour_count = key_and_count(df['Start Hour'])

    print('\nThe most common start hour is {} having {} users start rides during the hour.'.format(pop_hour, pop_hour_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Finds the most common start station and its count
    pop_s_station, pop_s_station_count = key_and_count(df['Start Station'])

    print('\nThe most common start station is {} with a usage of {}.'.format(pop_s_station, pop_s_station_count))

    # Finds the most common end station and its count
    pop_e_station, pop_e_station_count = key_and_count(df['End Station'])

    print('\nThe most common end station is {} with {} users ending their ride there.'.format(pop_e_station, pop_e_station_count))

    # Get the most common trip
    com_s_station = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).keys()[0][0]
    com_e_station = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).keys()[0][1]
    com_station_count = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)[0]

    print('\nThe most common route starts at {} and ends at {} with {} users taking that path.'.format(com_s_station, com_e_station, com_station_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Sums all of the travel times
    total_travel_time = df['Trip Duration'].sum()

    print('\nThe total travel time is {}.'.format(total_travel_time))

    # Finds the average trip time
    mean_travel_time = df['Trip Duration'].mean()

    print('\nThe average trip duration is {}.'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Get the counts for each user type
    user_type_0 = df['User Type'].value_counts().keys()[0]
    user_type_1 = df['User Type'].value_counts().keys()[1]
    user_type_0_count = df['User Type'].value_counts()[0]
    user_type_1_count = df['User Type'].value_counts()[1]

    print('\nThe two user types are {} and {} with counts of {} and {} respectively.'.format(user_type_0, user_type_1, user_type_0_count, user_type_1_count))

    if 'Gender' in df.columns:
        # Gets gender count information
        gender_0 = df['Gender'].value_counts().keys()[0]
        gender_1 = df['Gender'].value_counts().keys()[1]
        gender_0_count = df['Gender'].value_counts()[0]
        gender_1_count = df['Gender'].value_counts()[1]

        print('\nThe user count is {} for {} and {} for {}.'.format(gender_0_count, gender_0, gender_1_count, gender_1))

    if 'Birth Year' in df.columns:
        # Gets birth year information
        early_bday = df['Birth Year'].min()
        late_bday = df['Birth Year'].max()
        com_bday = df['Birth Year'].value_counts().keys()[0]

        print('\nThe earliest user birth year is {}.'.format(int(early_bday)))
        print('\nThe latest user birth year is {}.'.format(int(late_bday)))
        print('\nThe most common user birth year is {}.'.format(int(com_bday)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)

        station = input('Are you ready to see station stats? (yes or no)').lower()
        while station != 'yes'
            if station not in checks:
                station = input('Please enter yes or no.\n').lower()
            else:
                station = input('Enter yes when ready')
        station_stats(df)

        trip = input('Are you ready to see trip duration stats? (yes or no)')
        while trip != 'yes'
            if trip not in checks:
                trip = input('Please enter yes or no.\n').lower()
            else:
                trip = input('Enter yes when ready')
        trip_duration_stats(df)

        user = input('Are you ready to see user stats? (yes or no)')
        while user != 'yes'
            if user not in checks:
                user = input('Please enter yes or no.\n').lower()
            else:
                user = input('Enter yes when ready')
        user_stats(df)

        n = 0
        m = 5
        raw_data = input('\nWould you like to see individual trip data? (yes or no)\n')
        while raw_data == 'yes':
            print(df.iloc[n:m])
            n += 5
            m += 5
            raw_data = input('\nWould you like to see more? (yes or no)\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        while restart not in checks:
            restart = input('Please enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
