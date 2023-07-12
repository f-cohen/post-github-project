import time
import pandas as pd


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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city data are you interested in analysing?... ').lower()     
    while city not in CITY_DATA:
        print('There\'s no data available for {}'.format(city))
        print('Please inset one of these cities: {}... '.format(list(CITY_DATA.keys())))
        city = input().lower()
        
    # get user input for month (all, january, february, ... , june)
    month = input("Which month do you want to filter by? If not, write: all... ").title()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day? If all, write all... ').title()
   
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
    month_list = ['January', 'February', 'March', 'April', 'May','June', 'July', 'August', 'September', 'October', 'November', 'December']
    day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] 
        
    df = pd.read_csv(CITY_DATA[city])
        
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.strftime('%B')
    df['Day_of_week'] = df['Start Time'].dt.day_name() 
    df['Hour'] = df['Start Time'].dt.hour
        
    try:    
            
        if month != 'All' and month not in month_list:
            raise ValueError ('Incorrect month value')
            
        elif month != 'All' and month in month_list: 
            df = df[df['Month'] == month]
            
        if day != 'All' and day not in day_list:
            
            raise ValueError ('Incorrect day value')
                     
        elif day != 'All' and day in day_list:
            df = df[df['Day_of_week'] == day]
        
            
    except:
        
        print('It wasn\'t possible to filter the data because one of your inputs was incorrect. \nPlease select the filters again.')    
        
           
        for i, month in enumerate(month_list):
                                     
            m = input('Did you mean {}?... Y/N '.format(month)).lower()
                
            if i == len(month_list) - 1:
                
                month = 'All'
                print('No filter applied for month')
                
            elif m == 'y': 
                
                month = month_list[i]
                df = df[df['Month'] == month]
                break
        
        for i, day in enumerate(day_list):
                                     
            d = input('Did you mean {}?... Y/N '.format(day)).lower()
                
            if i == len(day_list) - 1:
                
                day = 'All'
                print('No filter applied for day')
                
            elif d == 'y': 
                
                day = day_list[i]
                df = df[df['Day_of_week'] == day]
                break
        
    return df


def display_data(df):
    'Displays raw data upon request by the user'
    
    display = input('Would you like to display the first 5 rows of data? ... Y/N ').lower()

    if display == 'y':
        
        print(df[:5])
        i = 5
        
        while True:
                    
            more = input('Would you like to display the next 5 rows? ... Y/N ').lower() 
            if more != 'y': 
                break
         
            elif i+5 >= df.shape[0]:
                print(df[i:])
                break  
            
            else:
                print(df[i:i+5])
                i+=5


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month   
    print('Most common month is: {}'.format(df['Month'].value_counts().idxmax()))
          
    
    # display the most common day of week
    print('Most common day of week is: {}'.format(df['Day_of_week'].value_counts().idxmax()))

    # display the most common start hour
    
    print('Most common start hour is: {}'.format(df['Hour'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Start station mostly used {}:'.format(df['Start Station'].value_counts().idxmax()))

    # display most commonly used end station
    print('End station mostly used {}:'.format(df['End Station'].value_counts().idxmax()))

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' - ' + df['End Station']
    print('Most frequent combination of start staion and end station trip is: {}'.format(df['Route'].value_counts().idxmax()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The minimun trip duration is {}:'.format(df['Trip Duration'].value_counts().idxmin()))
    print('The maximun trip duration is {}:'.format(df['Trip Duration'].value_counts().idxmax()))
    
    # display mean travel time
    print('The mean trip duration is {}:'.format(df['Trip Duration'].mean()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts for each user types are {}'.format(df['User Type'].value_counts()))

    # Only access Gender column in this case
    if 'Gender' in df:
        # Display counts of gender
        print('The counts for each gender are {}'.format(df['Gender'].value_counts()))
    else:
        print('Gender stats cannot be calculated because gender does not appear in the dataframe')

    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        print('The earliest year of birth is {}:'.format((df['Birth Year'].min())))
        print('The most recent year of birth is {}:'.format((df['Birth Year'].max())))
        print('The most common year of birth is {}:'.format((df['Birth Year'].value_counts().idxmax())))
    else:
        print('Birth Year stats cannot be calculated because birth year does not appear in the dataframe')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Y/N.\n').lower()
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
