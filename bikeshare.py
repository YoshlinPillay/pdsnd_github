import time
import pandas as pd

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}
days = {'Mon': 0,
        'Tue': 1,
        'Wed': 2,
        'Thu': 3,
        'Fri': 4,
        'Sat': 5,
        'Sun': 6,
        'all': -1}

months = {'Jan': 1,
          'Feb': 2,
          'Mar': 3,
          'Apr': 4,
          'May': 5,
          'Jun': 6,
          'all': -1}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("\nWhich city would you like data on? New York City, Chicago or Washington?\n")
        if city not in CITY_DATA:
            print("Sorry, I didn't quite get that, please re-enter.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input(
            "\nDo you want to specify a particular Month?If so, choose a month from : Jan, Feb, Mar, Apr, May, "
            "Jun or type 'all' if you do not have any preference?\n")
        if month.lower().capitalize() not in months:
            print("Sorry, I didn't quite get that, please re-enter.")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input(
            "\nDo you want to specify a particular day?If so, choose a day from : Sun, Mon, Tue, Wed, Thu, Fri, "
            "Sat or type 'all' if you do not have any preference.\n")
        if day.lower().capitalize() not in days:
            print("Sorry, I didn't quite get that, please re-enter.")
            continue
        else:
            break

    print('-' * 40)
    return city, month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable

    if month != 'all':
        # use the index of the months list to get the corresponding int

        # filter by month to create the new dataframe
        df = df[df['month'] == (months[month])]

        # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == (days[day])]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    popular_month = df['month'].mode()[0]
    if popular_month == 0:
        print('Most Common Month:', 'Jan')
    elif popular_month == 1:
        print('Most Common Month:', 'Feb')
    elif popular_month == 2:
        print('Most Common Month:', 'Mar')
    elif popular_month == 3:
        print('Most Common Month:', 'Apr')
    elif popular_month == 4:
        print('Most Common Month:', 'May')
    elif popular_month == 5:
        print('Most Common Month:', 'Jun')
    else:
        print('Data not available')

    # display the most common day of week

    popular_day = df['day_of_week'].mode()[0]

    if popular_day == 0:
        print('Most Common day:', 'Mon')
    elif popular_day == 1:
        print('Most Common day:', 'Tue')
    elif popular_day == 2:
        print('Most Common day:', 'Wed')
    elif popular_day == 3:
        print('Most Common day:', 'Thu')
    elif popular_day == 4:
        print('Most Common day:', 'Fri')
    elif popular_day == 5:
        print('Most Common day:', 'Sat')
    elif popular_day == 6:
        print('Most Common day:', 'Sun')
    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour, ':00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    start_station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', start_station)

    # display most commonly used end station

    end_station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', end_station)

    # display most frequent combination of start station and end station trip

    combination_station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)

    print('\nMost Commonly used combination of start and end station trip:', combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = sum(df['Trip Duration'])
    print('Total travel time:', total_travel_time / 86400, " Days")

    # display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time / 60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    # print(user_types)
    print('User Types:\n', user_types)

    # Display counts of gender

    try:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    except KeyError:
        print("\nGender Types:\nNo data available for this month.")

    # Display earliest, most recent, and most common year of birth

    try:
        earliest_year = df['Birth Year'].min()
        print('\nEarliest Year:', earliest_year)
    except KeyError:
        print("\nEarliest Year:\nNo data available.")

    try:
        most_recent_year = df['Birth Year'].max()
        print('\nMost Recent Year:', most_recent_year)
    except KeyError:
        print("\nMost Recent Year:\nNo data available.")

    try:
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('\nMost Common Year:', most_common_year)
    except KeyError:
        print("\nMost Common Year:\nNo data available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Displays raw data on bikeshare users."""
    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, row_length, 5):

        yes = input('\nWould you like to examine the particular user trip data? Type \'Yes\' or \'No\'\n> ')
        if yes.lower() != 'yes':
            break
        row_data = df.iloc[i: i + 5]
        print(row_data)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter Y or N.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()