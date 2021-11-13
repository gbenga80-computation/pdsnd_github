import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Enter city (Chicago, New York City or Washington) you would like to analyze: ")
    while city.lower() not in CITY_DATA.keys():
        city = input ("Entry not valid: please enter either Chicago, New York City or Washington! ")

    city = city.lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Enter a month between January through June or enter 'ALL' to select all the months: ")
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    while month.lower() not in months:
        month = input("Entry not valid: Please enter in a month between January through June or enter ALL to select all the months: ")

    month = month.lower()


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    dow = input("Enter a day of the week (i.e. Monday, Tuesday..., Sunday) or enter ALL to choose the whole week: ")
    days_of_week = ['monday', 'tuesday', 'wednesday' , 'thursday', 'friday', 'saturday', 'sunday', 'all']

    while dow.lower() not in days_of_week:
        dow = input("Entry not valid: Please enter oa day of the week  (i.e. Monday, Tuesday..., Sunday) or enter ALL to choose the whole week:")

    day = dow.lower()


    print('-'*40)
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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    ## convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month   # extract month
    try:
        top_month = df['month'].value_counts().idxmax()      #most common month
        print("The most common month for bike rentals is: {}".format(top_month))
    except ValueError:
        pass



    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek  # extract day of week
    top_day = df['day_of_week'].value_counts().idxmax()          # most popular day
    print("The most frequent day for bike rentals is: {}".format(top_day))


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour  # extract hour
    popular_hour = df['hour'].value_counts().idxmax()     # most popular hour
    print("The most popular hour to rent bikes is: {}".format(popular_hour))




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    top_start = df['Start Station'].value_counts().idxmax()

    # TO DO: display most commonly used end station
    top_end = df['End Station'].value_counts().idxmax()

    print(" The most common Start Station is: {}\n The most common End Station is: {}".format(top_start, top_end))


    # TO DO: display most frequent combination of start station and end station trip
    max_route=df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("\n\n The most frequent route for start station and end station is:\n{} \n ".format(max_route.to_string()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Duration'] = df['End Time'].subtract(df['Start Time'])


    # TO DO: display total travel time
    total_travel_time  = df['Duration'].sum()

    # TO DO: display mean travel time
    mean_travel_time = df['Duration'].mean()

    print(" Total travel time for all trips is: {} \n Mean travel time is: {}".format(total_travel_time, mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())



    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender.to_string())


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode())

        print(" The earliest year of birth is: {}\n The most recent year of birth is: {}\n The most common year of birth is: {}".format(earliest, recent, common_year))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    index=0
    user_input=input('would you like to display 5 rows of raw data? (Yes/No) ').lower()
    while user_input in ['yes','y'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data? ').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you for taking time to explore the bike sharing dataset")
            break


if __name__ == "__main__":
    main()
