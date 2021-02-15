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
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    days = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city =(input('To see data, enter one of the cities listed below:\nChicago\nNew York City\nWashington\n')).lower()
            if city not in CITY_DATA:
                raise ValueError
            break
        except ValueError:
            print('\nYour input is: "{}" and does not match any of the cities from the provided list.'.format(city))

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month =(input('\nIf you would like to filter data by month, type one of the months listed below or type "all" for no month-filter: \nJanuary \nFebruary \nMarch \nApril \nMay \nJune\n')).lower()
            if month not in months:
                raise ValueError
            break
        except ValueError:
            print('\nYour input is: "{}" and does not match any of the provided options.'.format(month))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day =(input('\nTo filter data by day, enter one of the following days or type "all" for no day filter: \nMonday \nTuesady \nWednesday \nThursday \nFriday \nSaturday \nSunday \n')).lower()
            if day not in days:
                raise ValueError
            break
        except ValueError:
            print('\nYour input is: "{}" and does not match any of the provided options from the list.'.format(day))
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month']==month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
       Function uses mode stats.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # if month filter was applied, do not dispaly month stats
    if df['month'].nunique()>1:
            popular_month = df['month'].mode()[0]
            print('Most common month:', popular_month)
    else:
        print('To see most common month, don\'t apply Month filter')

    # TO DO: display the most common day of week
    # if day filter was applied, do not display day stats
    if df['day_of_week'].nunique()>1:
        popular_day = df['day_of_week'].mode()[0]
        print('Most common day:', popular_day)
    else:
        print('To see most common day, don\'t apply Day filter')

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start trip hour:', popular_hour)

    # TO DO: display the latest hour in a day that the trip started at
    latest_hour = df['hour'].max()

    print('The latest hour in a day of the start trip:', latest_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    pd.set_option('precision', 0)
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The Most Popular Start Station is:\n{}'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The Most Popular End Station is:\n{}'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' - ' + df['End Station']
    print('The most frequent trip is:\n{}'.format(df['combination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    pd.set_option('precision', 0)
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time is:',int(total_time//3600),'hours',int((total_time%3600)//60),'minutes',int(total_time%60),'seconds')


    # TO DO: display mean travel time
    travel_time_mean = round(df['Trip Duration'].mean(),3)
    print("The average travel time is {} seconds".format(travel_time_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    pd.set_option('precision', 0)
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts().to_frame(name='counts')
    print('The breakdown of users is:\n{}\n'.format(user_type_count))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts().to_frame(name='counts')
        print('The breakdown of gender is:\n{}\n'.format(gender_counts))
    else:
        print('To see gender distribution data, restart program and select either Chicago or New York City')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('The earliest year of birth is:', int(df['Birth Year'].min()))
        print('The most recent year of birth is:', int(df['Birth Year'].max()))
        print('The most common year of birth is:', int(df['Birth Year'].mode()[0]))
    else:
        print('To see stats about user\'s birth year, restart program and select either Chicago or New York City')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Asks user if wants to see raw data.
    If user input is:
                    1) 'no' -> it terminates the loop
                    2) 'yes' ->  prints first 5 lines of data and asks again
                     if user wants to see next 5 lines in the sequence
    Prints:
        (DataFrame)  - df - prints slices of df data frame in chunks of 5 lines
    """
    i = 0
    raw = (input("Would you like to view individual trip data? Type 'yes' or 'no':\n")).lower()
    pd.set_option('display.max_columns',200)
    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i+5])
            raw = input("Would you like to view more data? Type 'yes' or 'no':\n").lower()
            i += 5
        else:
            raw = (input("\nYour input is invalid. Please enter only 'yes' or 'no'\n")).lower()

def restart_program():
    """
    Asks user if wants to restart the program or exit it.
    If user input is:
                    1) 'no' -> exits the program
                    2) 'yes' ->  terminates the loop and goes to the start of main()

    """

    while True:
        try:
            restart = input("\nWould you like to restart? Enter 'yes' or 'no'.\n")
            if restart.lower() == 'yes':
                break
            elif restart.lower() == 'no':
                exit()
            else:
                raise ValueError
            break
        except ValueError:
           print("\nYour input is incorrect. Please type only 'yes' or 'no'")




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart_program()

if __name__ == "__main__":
	main()
