import inline as inline
import matplotlib as matplotlib
import pandas as pd


#project working dir
pwd = '/manny/Manny/Projects/NetflixWatchCheck/'


df = pd.read_csv('Netflix/Content_Interaction/ViewingActivity.csv')

df.shape

df.head(1)

df = df.drop(['Profile Name', 'Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark', 'Country'], axis=1)
df.head(1)

df.dtypes

df['Start Time'] = pd.to_datetime(df['Start Time'], utc=True)

df.dtypes

# change the Start Time column into the dataframe's index
df = df.set_index('Start Time')

# convert from UTC timezone to eastern time
df.index = df.index.tz_convert('Africa/Johannesburg')

# reset the index so that Start Time becomes a column again
df = df.reset_index()

#double-check that it worked
df.head(1)

df['Duration'] = pd.to_timedelta(df['Duration'])
df.dtypes



# create a new dataframe called sister that that takes from df
# only the rows in which the Title column contains 'Sister, Sister'
sister = df[df['Title'].str.contains('Sister, Sister', regex=False)]

sister.shape


sister = sister[(sister['Duration'] > '0 days 00:01:00')]
sister.shape


#how much time has Tania spent watching sister, sister
sister['Duration'].sum()

sister['weekday'] = sister['Start Time'].dt.weekday
sister['hour'] = sister['Start Time'].dt.hour

# check to make sure the columns were added correctly
sister.head(1)


#%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt


# set our categorical and define the order so the days are plotted Monday-Sunday
sister['weekday'] = pd.Categorical(sister['weekday'], categories=
    [0,1,2,3,4,5,6],
    ordered=True)

# create sister_by_day and count the rows for each weekday, assigning the result to that variable
sister_by_day = sister['weekday'].value_counts()

# sort the index using our categorical, so that Monday (0) is first, Tuesday (1) is second, etc.
sister_by_day = sister_by_day.sort_index()

# optional: update the font size to make it a bit larger and easier to read
matplotlib.rcParams.update({'font.size': 22})

# plot sister_by_day as a bar chart with the listed size and title
sister_by_day.plot(kind='bar', figsize=(20,10), title='sister Episodes Watched by Day')
plt.plot(kind='bar', figsize=(20,10), title='sister Episodes Watched by Day')
plt.savefig('/manny/Manny/Projects/NetflixWatchCheck/test.png')


# set our categorical and define the order so the hours are plotted 0-23
sister['hour'] = pd.Categorical(sister['hour'], categories=
    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
    ordered=True)

# create sister_by_hour and count the rows for each hour, assigning the result to that variable
sister_by_hour = sister['hour'].value_counts()

# sort the index using our categorical, so that midnight (0) is first, 1 a.m. (1) is second, etc.
sister_by_hour = sister_by_hour.sort_index()

# plot sister_by_hour as a bar chart with the listed size and title
sister_by_hour.plot(kind='bar', figsize=(20,10), title='sister Episodes Watched by Hour')
plt.plot(kind='bar', figsize=(20,10), title='sister Episodes Watched by Hour')
plt.savefig(pwd + 'test2.png')