import time
import pandas as pd
import numpy as np
CITY_DATA = { 'ch': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'wt': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input('\nEnter of Which city(chicago-ch, new york city-nyc, washington-wt) you want to analyze data ? ch or nyc or wt\n').lower()
        if city not in ('ch', 'nyc', 'wt'):
            print("WRONG INPUT !!! PLEASE ENTER CITY NAME GIVEN")
            continue
        break    
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nIf you want to filter on months enter any ( jan, feb, mar, apr, may, jun), If not enter "all"\n').lower()
        if month not in ('all','jan', 'feb', 'mar', 'apr', 'may', 'jun'):
            print("WRONG INPUT !!! PLEASE ENTER CORRECT INPUT")
            continue
        break    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nIf you want to filter on day of week enter any ( mon, tue, wed, thu, fri, sat, sun), If not enter "all"\n').lower()
        if day not in ('all','mon','tue','wed','thu','fri','sat','sun'):
            print("WRONG INPUT !!! PLEASE ENTER CORRECT INPUT")
            continue
        break    
    

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
    df = pd.read_csv(CITY_DATA[city], parse_dates=['Start Time'])
    # removing unnamed column at index 0
    df = df.drop(df.columns[0], axis=1)

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month']== month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days of week list to get the corresponding int
        weekdays = ['mon','tue','wed','thu','fri','sat','sun']
        weekday = weekdays.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']== weekday]
   
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # find the most common month(from 1 to 6)
    popular_month = df['month'].mode()[0]
    #convert to month name
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[popular_month-1]
    # display the most common month
    print('Most Common Month:', popular_month)

    # find the most common day of week (from 0 to 6)
    popular_weekday = df['day_of_week'].mode()[0]
    #convert to weekday name
    weekdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    popular_weekday = weekdays[popular_weekday]
    #display the most common day of week
    print('Most Common Week:', popular_weekday)

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    # display the most common start hour
    print('Most Frequent Start Hour of day:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # find most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    # display most commonly used start station
    print('Most Commonly Used Start Station:', popular_start_station)
   
    # find most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    # display most commonly used end station
    print('Most Commonly Used End Station:', popular_end_station)

    # find most frequent combination of start station and end station trip
    combined_station = (df['Start Station']+ ' -TO- ' + df['End Station']).mode()[0]
    # display most frequent combination of start station and end station trip
    print('Most Common Trip From Start To End:',combined_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # find total travel time
    total_travel_time = df['Trip Duration'].sum()
    # display total travel time
    print('Total Travel Time:', total_travel_time)
    
    # find mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    # display mean travel time
    print('Average Travel Time:', avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # find counts of user types
    user_types = df['User Type'].value_counts()
    # display counts of user types
    print('Count of each User Type'.center(30,'*'),user_types,sep ='\n',end='\n\n')
    
    # check if Gender Column exists
    if "Gender" in df:
        gender_count = df['Gender'].value_counts()  # find counts of gender
        # display counts of gender
        print('Count of Gender'.center(22,'*'), gender_count,sep ='\n',end='\n\n')
        
        # find earliest, most recent, and most common year of birth
        earliest_yob = df['Birth Year'].min()
        recent_yob = df['Birth Year'].max()
        popular_yob = df['Birth Year'].mode()[0]
        # display earliest, most recent, and most common year of birth
        print("Earliest Year of Birth:",int(earliest_yob))
        print("Most Recent Year of Birth:",int(recent_yob))
        print("Most Common Year of Birth:",int(popular_yob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def see_raw_data(df):
    """ Displays Individuals data(5 rows at a time). """
    count = 0
    see_data = input('\nWould you like to see individuals data?"Yes" or "No"\n')
    if see_data.lower() == 'yes':
        while True:
            print(df[count:count+5])    # get 5 rows of data
            count += 5
            see_data = input('\nWould you like to see more individuals data?"Yes" or "No"\n')
            if see_data.lower() == 'no':
                   break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('-'*15,city.upper(),'-',month.upper(),'-',day.upper(),'-'*15) # heading that displays choosed city,month,day
        time_stats(df)
        print('-'*15,city.upper(),'-',month.upper(),'-',day.upper(),'-'*15) # heading that displays choosed city,month,day
        station_stats(df)
        print('-'*15,city.upper(),'-',month.upper(),'-',day.upper(),'-'*15) # heading that displays choosed city,month,day 
        trip_duration_stats(df)
        print('-'*15,city.upper(),'-',month.upper(),'-',day.upper(),'-'*15) # heading that displays choosed city,month,day
        user_stats(df)
        print('-'*15,city.upper(),'-',month.upper(),'-',day.upper(),'-'*15) # heading that displays choosed city,month,day
        see_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
