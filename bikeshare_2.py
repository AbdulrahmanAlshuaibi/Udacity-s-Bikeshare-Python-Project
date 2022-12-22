import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_name = input('Please choose a city from these three: chicago, new york city, washington \n').lower()

    while city_name not in CITY_DATA.keys():
        print('sorry, you have entered a wrong city name. Please enter a correct city name')
        city_name = input('Please choose a city from these three: chicago, new york city, washington \n').lower()

    # get user input for month (all, january, february, ... , june)
    while True:
        month_name = input('please select one of these month to filter by. (all, january, february, march, april, may, june)').lower()
        if month_name in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('sorry, you have entered a wrong month name')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_of_week = input('please enter any day of the week or type "all" to filter by. \n').lower()
        if day_of_week in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
            break
        else:
            print('sorry, you have entered a wrong day name')

    print('-' * 40)

    return city_name, month_name, day_of_week


def load_data(city_name, month_name, day_of_week):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city_name])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month_name'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month_name != 'all':
        month = ['january', 'february', 'march', 'april', 'may', 'june']
        month_name = month.index(month_name) + 1  # because the indexing start at zero in python, and we need to make january's index to 1
        df = df[df['month_name'] == month_name]


    if day_of_week != 'all':
        df = df[df['day_of_week'] == day_of_week.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month_name'].mode()[0]
    print('The most common month is:', common_month)
    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is:', common_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour is', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is', common_start_station)
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common End station is', common_end_station)

    # display most frequent combination of start station and end station trip
    combination = common_start_station + " , " + common_end_station
    print('The combination of the most common start and end stations are:', combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is ', total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('This is the number of users in each type\n', user_types)
    # Display counts of gender
    try:
        genders = df['Gender'].value_counts()
        print('This is the number of users in each gender: \n', genders)
    except KeyError:
        print('No data for number of users ')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = (df['Birth Year'].min())
        print('The earliest birth year is ', int(earliest_birth_year))
    except KeyError:
        print('No data for earliest')

    try:
        recent_birth_year = df['Birth Year'].max()
        print('The most recent birth year is ', int(recent_birth_year))
    except KeyError:
        print('no data for recent birth')

    try:
        common_birth_year = df['Birth Year'].mode()[0]
        print('The most common birth year is ', int(common_birth_year))
    except KeyError:
        print('No data for common birth year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)



def moredata(df):
    i = 0
    while True:
        raw_data = input('Would you like to see more raw data? Enter yes or no please \n')
        if raw_data == 'yes':
            print(df.iloc[i: i+5])
            i += 5
        elif raw_data =='no':
            break

        else:
            print('you have entered wrong answer')



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        moredata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
