import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new-york': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_lst = ['chicago','new-york','washington']
mon_lst = ['jan','feb','mar','apr','may','jun','all']
day_lst = ['mon','tue','wed','thu','fri','sat','sun','all']
fil_lst = ['month', 'day','both']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city, month, day = '','',''
    
    #print('Hello! Let\'s explore some US bikeshare data!')
    print("Hello!, Welcome to the US Bikeshare Data Platform!","\n")
    print('*'*60)
    print('*'*4,"I am Chigo, Your favourite data analytic assistant",'*'*4)
    print('*'*60)
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Which city\'s data would you love to explore? Chicago, New-York, or Washington: ')
            if city.lower() in city_lst:
                city = city.lower() 
            else:
                if(not city.isalpha()):
                    raise TypeError
                else:
                    raise ValueError
            break
        except TypeError:
            print("\t","That\'s not a valid strings. Please try again!")    
        except ValueError:
            print("\t","That\'s not a valid city. Please try again!")
        except KeyboardInterrupt:
            print("\t","Program has been terminated by you. Thanks for exploring!")
    
    # TO DO: get user input to filter by what Parameters
    while True:
        try:
            fil_para = input('Would you love to explore Bikeshares data by? month, day, or both: ')
            if fil_para.lower() in fil_lst:
                fil_para = fil_para.lower()
            else:
                if(not fil_para.isalpha()):
                    raise TypeError
                else:
                    raise ValueError
            break
        except TypeError:
            print("\t","That\'s not a valid strings. Please try again!")    
        except ValueError:
            print("\t","That\'s not a valid filter parameter. Please try again!")
        except KeyboardInterrupt:
            print("\t","Program has been terminated by you. Thanks for exploring!")
    
     # TO DO: get user input for month if applicable (all, january, february, ... , june)
    if fil_para != 'day':
        while True:
            try:
                month = input('Which month\'s data would you love to explore? Jan, Feb, Mar, Apr, May, Jun or all: ')
                if month.lower() in mon_lst:
                    month = month.lower()
                else:
                    if(not month.isalpha()):
                        raise TypeError
                    else:
                        raise ValueError
                break
            except TypeError:
                print("\t","That\'s not a valid strings. Please try again!")    
            except ValueError:
                print("\t","That\'s not a valid month. Please try again!")
            except KeyboardInterrupt:
                print("\t","Program has been terminated by you. Thanks for exploring!")
    
    # TO DO: get user input for day of week if applicable (all, monday, tuesday, ... sunday)
    if fil_para != 'month':
        while True:
            try:
                day = input('Which day\'s data would you love to explore? Mon, Tue, Wed, Thu, Fri, Sat, Sun or all: ')
                if day.lower() in day_lst:
                    day = day.lower()
                else:
                    if(not day.isalpha()):
                        raise TypeError
                    else:
                        raise ValueError
                break
            except TypeError:
                print("\t","That\'s not a valid strings. Please try again!")    
            except ValueError:
                print("\t","That\'s not a valid day of the week. Please try again!")
            except KeyboardInterrupt:
                print("\t","Program has been terminated by you. Thanks for exploring!")
     
    print('-'*100)
    return city, month, day, fil_para


def load_data(city, month, day,fil_para):
    """
    Loads data for the specified city 
    Perform some feature engineering to correct missing values in Gender and Birth Year columns
    and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Reading data from the selected city record file
    df_city = pd.read_csv(CITY_DATA[city])
    
    ## Perform some feature Engineering on missing data set and
    # TO DO: Excluding washington data set because Gender and birth year column are not present 
    if city != "washington":
        while (df_city['Birth Year'].isnull().sum() != 0):
            df_city['Birth Year'].interpolate(inplace=True) 

        while (df_city['Gender'].isnull().sum() != 0):
            df_city['Gender'].interpolate(method='pad', limit=2, inplace=True)

    df_city['Start Time'] = pd.to_datetime(df_city['Start Time'])
    df_city['month_rec'] = df_city['Start Time'].dt.month
    df_city['day_rec'] = df_city['Start Time'].dt.weekday
    df_city['hour_rec'] = df_city['Start Time'].dt.hour
    
    # TO DO: Excluding washington data set because Gender and birth year column are not present   
    if city != "washington":
        df_city['Birth Year'] = df_city[['Birth Year']].astype(int)
    

    # Confirming the parameter to filter by
    if fil_para == 'both':
        # Applying the month filter parameter
        if month != 'all':
            month = mon_lst.index(month) + 1
            df_city = df_city[df_city['month_rec'] == month]

        # Applying the day filter parameter
        if day != 'all':
            #print(mon_lst.index(month) + 1)
            day = day_lst.index(day)
            df_city = df_city[df_city['day_rec'] == day]
    elif fil_para == 'month':
        # Applying the month filter parameter
        if month != 'all':
            month = mon_lst.index(month) + 1
            df_city = df_city[df_city['month_rec'] == month]
    else:
        # Applying the day filter parameter
        if day != 'all':
            #print(mon_lst.index(month) + 1)
            day = day_lst.index(day)
            df_city = df_city[df_city['day_rec'] == day]
            
    print(f'\n{city.title()} City\'s Data is now loaded for further analysis......\n')
        
    return df_city


def time_stats(df_city,city, month, day,fil_para):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    freq_mon = mon_lst[df_city['month_rec'].mode()[0] - 1] 
    low_mon = mon_lst[df_city['month_rec'].value_counts().idxmin()-1]
   
    print(f"The month with the highest bike ride is : {freq_mon} and the least month is : {low_mon} !!!","\n")
    
    # TO DO: display the most common day of week
    freq_day = day_lst[df_city['day_rec'].mode()[0]] 
    low_day = day_lst[df_city['day_rec'].value_counts().idxmin()]
   
    print(f"The day of the week with the highest bike ride is : {freq_day} and the least day is : {low_day} !!!","\n")
    
    # TO DO: display the most common start hour
    freq_hr = df_city['hour_rec'].mode()[0] 
    low_hr = df_city['hour_rec'].value_counts().idxmin()
    print(f"The hour of the day with the highest bike ride is the : {freq_hr}th hour and the least hour is the : {low_hr}th hour !!!")

    print("\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def station_stats(df_city,city, month, day,fil_para):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    freq_strs = df_city['Start Station'].mode()[0]
    print(f"The station with the most bike ride starting point in {city.title()} city is : {freq_strs} station !!!")
    
    # TO DO: display most commonly used end station
    freq_stps = df_city['End Station'].mode()[0]
    print(f"The station with the most bike ride starting point in {city.title()} city is : {freq_stps} station !!!")

    # TO DO: display most frequent combination of start station and end station trip
    freq_cbm = df_city[df_city['End Station'] == df_city['Start Station']]['Start Station'].value_counts().idxmax()
    print(f"The station with same bike ride start and end station occuring the most in {city.title()} city is : {freq_cbm} station !!!")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df_city,city, month, day,fil_para):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

   # TO DO: display total travel time
    trp_dur = df_city['Trip Duration'].sum()
    if month == 'all' and day == 'all' :
        print(f"The total trip duration for {city.title()} city is : {trp_dur} seconds !!!")
    elif month == 'all' and day != 'all':
        print(f"The total trip duration for {city.title()} city for {day} in all months is : {trp_dur} seconds !!!")
    elif month != 'all' and day == 'all':
        print(f"The total trip duration for {city.title()} city for all days in the months of {month} is : {trp_dur} seconds !!!")
    else:
        print(f"The total trip duration for {city.title()} city for {day}\'s in the month of {month} is : {trp_dur} seconds !!!") 

    print("\n")
    # TO DO: display mean travel time
    trp_avg = df_city['Trip Duration'].mean()

    if month == 'all' and day == 'all' :
        print(f"The Average trip time for {city.title()} city is : {round(trp_avg,2)} seconds in two decimal place !!!")
    elif month == 'all' and day != 'all':
        print(f"The Average trip time for {city.title()} city for {day} in all months is : {round(trp_avg,2)} seconds in two decimal place  !!!")
    elif month != 'all' and day == 'all':
        print(f"The Average trip time for {city.title()} city for all days in the months of {month} is : {round(trp_avg,2)} seconds in two decimal place  !!!")
    else:
        print(f"The Average trip time for {city.title()} city for {day}\'s in the month of {month} is : {round(trp_avg,2)} seconds in two decimal place !!!") 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


    
def user_stats(df_city,city, month, day,fil_para):   
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    # TO DO: Display counts of user types

    #df_k = df_city['User Type'].mode()[0]
    df_k = df_city['User Type'].value_counts()
    df_k = df_k.to_frame()

    sub_no = df_k.loc['Subscriber']['User Type']
    cust_no = df_k.loc['Customer']['User Type']
    print(f"The total number of Subscriber users for the filtered data set in {city.title()} city is : {sub_no} !!!","\n")
    print(f"The total number of Customer users for the filtered data set in {city.title()} city is : {cust_no} !!!")

    print("\n")
    
    # TO DO: Excluding washington data set because Gender and birth year column are not present 
    if city != "washington":
        # TO DO: Display counts of gender
        df_g = df_city['Gender'].value_counts()
        df_g = df_g.to_frame()
        mal_no = df_g.loc['Male']['Gender']
        fem_no = df_g.loc['Female']['Gender']
        print(f"The total number of Male users for the filtered data set in {city.title()} city is : {mal_no} !!!","\n")
        print(f"The total number of Female users for the filtered data set in {city.title()} city is : {fem_no} !!!")

        print("\n")
        # TO DO: Display earliest, most recent, and most common year of birth
        br_cnt = df_city['Birth Year'].mode()[0]
        br_rcn = df_city['Birth Year'].max()
        br_ear = df_city['Birth Year'].min()

        print(f"The following are the different analysis of bikeshare ride in {city.title()} city :")
        print(f"The Earliest date of birth is : {br_ear}")
        print(f"The Most date of birth is : {br_rcn}")
        print(f"The Most occurring date of birth is : {br_cnt}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)
    
def display_data(df_city):   
    """
    Get the bikeshares data
    Remove the feature Engineering from columns
    Displays raw data on bikeshare riders to the users.
    """

    print('\nExtracting bikeshare riders information...\n')

    start_time = time.time()
    
    # TO DO: Drop the feature columns from the data frames
    df_city.drop(['month_rec','day_rec','hour_rec'], axis=1, inplace=True)
    df_city.rename(columns={'Unnamed: 0':'Customer ID'}, inplace=True)
    df_city['Start Time'] = df_city['Start Time'] .astype(str)
    
    view_display = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    start_loc = 0
    while (view_display == "yes"):
        print(df_city.iloc[start_loc:start_loc+5].to_dict('records'))
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)
    
    print('*'*5,' ',"Thank you for using Chigo, Your favourite data analytic assistant to explore Bikeshares Data",' ','*'*5)
    

def main():
    while True:
        city, month, day, fil_para = get_filters()
        df = load_data(city, month, day, fil_para)

        time_stats(df,city, month, day,fil_para)
        station_stats(df,city, month, day,fil_para)
        trip_duration_stats(df,city, month, day,fil_para)
        user_stats(df,city, month, day,fil_para)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            


if __name__ == "__main__":
	main()
