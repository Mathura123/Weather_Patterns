
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# # Preparation of DataFrame for Line Plot

# In[21]:

def line_plot_df():
    import pandas as pd
    import numpy as np
    df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
    df = df.set_index('Date')
    df.index=pd.to_datetime(df.index)
    df = df[df.index.year!=2015]
    df= df[(df.index.month!=2) | (df.index.day!=29)]
    df['Month']= df.index.month
    df['Day']= df.index.day
    df= df.reset_index()
    df= df.set_index(['Month','Day','Element'])
    df= df.sort_index()
    maxlist = df.groupby(level=[0,1,2])['Data_Value'].agg({'maxtemp': np.max})
    maxlist = maxlist[maxlist.index.get_level_values(2)=='TMAX']
    maxlist['maxtemp']= maxlist['maxtemp']/10
    minlist = df.groupby(level=[0,1,2])['Data_Value'].agg({'mintemp': np.min})
    minlist = minlist[minlist.index.get_level_values(2)=='TMIN']
    minlist['mintemp']= minlist['mintemp']/10
    temp=pd.merge(maxlist,minlist,how='outer',left_index=True,right_index=True)
    temp = temp.reset_index()
    temp = temp.drop('Element',axis=1)
    temp = temp.set_index(['Month','Day'])
    temp['maxtemp'] = temp['maxtemp'].fillna(method='ffill')
    temp['mintemp'] = temp['mintemp'].fillna(method='bfill')
    temp= temp.reset_index()
    temp= temp.drop_duplicates()
    temp= temp.set_index(['Month','Day'])
    return temp
line_plot_df().head(40)


# # Preparation of Data Frame for Scatter Plot

# In[22]:

def scatter_plot_df():
    import pandas as pd
    import numpy as np
    df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
    df = df.set_index('Date')
    df.index=pd.to_datetime(df.index)
    df = df[df.index.year==2015]
    df= df[(df.index.month!=2) | (df.index.day!=29)]
    df['Month']= df.index.month
    df['Day']= df.index.day
    df= df.reset_index()
    df= df.set_index(['Month','Day','Element'])
    df= df.sort_index()
    maxlist = df.groupby(level=[0,1,2])['Data_Value'].agg({'maxtemp15': np.max})
    maxlist = maxlist[maxlist.index.get_level_values(2)=='TMAX']
    maxlist['maxtemp15']= maxlist['maxtemp15']/10
    minlist = df.groupby(level=[0,1,2])['Data_Value'].agg({'mintemp15': np.min})
    minlist = minlist[minlist.index.get_level_values(2)=='TMIN']
    minlist['mintemp15']= minlist['mintemp15']/10
    temp15 =pd.merge(maxlist,minlist,how='outer',left_index=True,right_index=True)
    temp15 = temp15.reset_index()
    temp15 = temp15.drop('Element',axis=1)
    temp15 = temp15.set_index(['Month','Day'])
    temp15['maxtemp15'] = temp15['maxtemp15'].fillna(method='ffill')
    temp15['mintemp15'] = temp15['mintemp15'].fillna(method='bfill')
    temp15= temp15.reset_index()
    temp15= temp15.drop_duplicates()
    temp15= temp15.set_index(['Month','Day'])
    return temp15
scatter_plot_df().head(40)


# # Prepartion of Plot

# In[26]:

get_ipython().magic('matplotlib notebook')
import matplotlib.pyplot as plt
import pandas as pd

def preapare_plot(temp,temp15):
    #preparation of line plot
    dfx=temp.reset_index()
    x_val=dfx.index.values
    x_ticks=dfx[dfx['Day']==1].index.tolist()
    ax1=temp.plot.line(x_val, figsize=(9, 4), xticks=x_ticks) # plot 2 lines
    ax1.fill_between(x_val, temp['maxtemp'], temp['mintemp'], facecolor='gainsboro') # fill betwee 2 lines
    
    #preparation of scatter plot upon line plot
    df=pd.merge(temp.reset_index(), temp15.reset_index(), how='inner')
    df['ind']=df.index
    dfMx=df[df['maxtemp15']>df['maxtemp']]
    dfMn=df[df['mintemp15']<df['mintemp']]
    dfMx.plot.scatter(x='ind', y='maxtemp15', label='a', ax=ax1, color='darkred', s=7)
    dfMn.plot.scatter(x='ind', y='mintemp15', label='b',ax=ax1, color='darkblue', s=7)
    
    #formatting the plot
    ax1.spines['bottom'].set_color('black')
    ax1.spines['left'].set_color('black')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_axis_bgcolor('white')
    h, l = ax1.get_legend_handles_labels()
    lines=(h[0], h[1]) #ax1.get_lines()
    ax1.legend(h, ('Max 2005-2014', 'Min 2005-2014', '2015 above Max', '2015 below Min'), loc=0, frameon=False)
    ax1.set_xticklabels(['Jan','Feb','Mar','April','May','June','July','Aug','Sep','Oct','Nov','Dec'])
    ax1.set_title('Assignment 2: The interval of minimum and maximum temperatures for 2005-2014 \n and temperatures of 2015, dropping out of the interval')
    ax1.set_xlabel('')
    ax1.set_ylabel('Temperatue in C')
    plt.setp(lines, linewidth=0.5)
    return ax1
preapare_plot(line_plot_df(),scatter_plot_df())


# In[50]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[ ]:



