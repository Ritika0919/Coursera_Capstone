#!/usr/bin/env python
# coding: utf-8

# # Battle of the Neighborhoods: Examining the Diversity in Cuisines from the East to the West of Toronto

# ##     1. Introduction:

# ##### _According to the article in https://theculturetrip.com/north-america/usa/california/articles/the-10-most-multicultural-cities-in-the-world/, Toronto is one of the most multicultural cities in the world. With millions of people migrating to Canada annually, it's cultural diversity has been enriched over the years, as has the cusine of this country._ 
# 
# ##### _For my Capstone Project, I have chosen to explore the variance in cuisines of two different boroughs of Toronto, to truly fathom the impact of immigration on Canada's gastronomic diversity._
# 
# ##### _As we will see later in the project, the Folium map of the Toronto neighborhoods shows us that the neighborhoods are spread out in a roughly rectangular shape. Hence, there is a greater probability of variety in cuisines in the East-West direction, than there is in the North-South direction. Therefore, I have chosen to explore Scarborough (a borough from the East of Toronto) and Etobicoke (a borough from the West of Toronto), to understand the true diversity in cuisines of Toronto as a result of immigration._

# #### 1.1. Assumptions:
# 

# #####  _This project assumes a direct proportionality between the number of restaurants of a particular cuisine and the popularity of that cuisine._
# 
# 
# ##### _Also, with the exponential expansion of fast food joints worldwide, it will be impossible not to come across at least one such establishment in our database. Since standalone fast food joints, mall food courts (containing a mix of fast food joints and restaurants), pizza and sandwich places, pubs, BBQ joints diners, breakfast spots, office canteens and miscellaneous restaurants (Asian or otherwise) do not project any cuisine in particular, they will be excluded from the gastronomic diversity analysis._

# ## 2. Data Collection: 

# ##### _This project gathers the Toronto neighborhood data from https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M. The page is a comprehensive database of all the Postal Codes of  the neighbourhoods and their subsequent boroughs, in Toronto. For accurate results, neighborhoods with unassigned boroughs will retain their neighborhood name. Unassigned boroughs will also be eliminated. Neighborhoods with the same postal codes will be grouped, for the ease of mapping. Mapping the neighborhoods will help me shortlist the boroughs I want to evaluate._
# 
# ##### _The postal codes (from the source above) will also help me find the coordinates of each neighborhood in the Geospatial_Coordinates file. The file http://cocl.us/Geospatial_data ,contains the longitude and latitude locations of each postal code. With the neighborhood coordinates, I will be able to focus my Foursquare search queries to the venues of the boroughs I want to analyze_
# 
# ##### _Using Foursquare API (https://developer.foursquare.com),I will be able to retrieve the features of restaurants (in this case category and number) in each borough for my analysis. Learning about the cuisines in the boroughs, will help me evaluate their gastronomic diversity._

# ## 3. Methodology:

# ##### _1. Import libraries necessary to execute this project._
# ##### _2. Create the Toronto dataframe containing PostalCode, Borough, Neighborhood, latitude and longitude information._
# ##### _3. Map the neighborhoods in Toronto._
# ##### _4. Plot a bar graph the number of neighborhoods in each borough._
# ##### _5. Shortlist two boroughs with the same or similar number of neighborhoods from East and West Toronto respectively. Create datasets for each borough._
# ##### _6. Use Foursquare API to search for venues._
# ##### _7. Analyze each borough for its restaurants and their features._
# ##### _8. Plot a bar graph for the most popular restaurants from each borough. Use Folium to map the locations._
# 

# ### 3.1. Importing libraries:

# In[1]:


# to transform raw data into numpy arrays
import numpy as np 

#to create a Pandas dataframe from the raw data
import pandas as pd 
pd.set_option('display.max_columns',None) #displays all columns
pd.set_option('display.max_rows',None) #displays all rows

#to get the latitude and longitude data for each city
get_ipython().system('conda install -c conda-forge geopy --yes')
from geopy.geocoders import Nominatim

#to make it easier to share data between code and URL easier
import requests 
from pandas.io.json import json_normalize

#to retrieve data from URL 
get_ipython().system('pip install beautifulsoup4')
from bs4 import BeautifulSoup

#import data visualization libraries
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.pyplot as plt


get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium

print("All the necessary libraries have been imported")


# ### 3.2.  Creating the Toronto dataframe:

# In[2]:


#extract table from Wikipedia page
source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup = BeautifulSoup(source)
table  = soup.find('table',{'class':'wikitable sortable'})

#format pandas dataframe
col_names = ['PostalCode','Borough','Neighborhood']
df = pd.DataFrame(columns = col_names)


# In[3]:


#Collecting all the data for Postal Codes, Boroughs and Neighborhoods

for a in table.find_all('tr'):
    row = []
    for b in a.find_all('td'):
        row.append(b.text.strip())
    if len(row)==3:
        df.loc[len(df)] = row  


# In[4]:


#eliminate Boroughs that are Not Assigned
df = df[df['Borough'] != 'Not assigned']

#Display neighborhoods with same post codes in one row
df = df.groupby(['PostalCode','Borough'],sort = False).agg(', '.join)
df.reset_index(inplace = True)

#Neighborhood = Borough, for those boroughs without an assigned Neighborhood
df.loc[df['Neighborhood'] == 'Not assigned','Neighborhood'] = df['Borough']


# In[5]:


#read in the geospatial coordinates
df_geo = pd.read_csv('Geospatial_Coordinates.csv')
df_geo.rename(columns = {'Postal Code': 'PostalCode'}, inplace = True)
df_geo = pd.merge(df,df_geo,on = 'PostalCode')
df_geo.head()


# In[6]:


print('The dataframe has {} boroughs and {} neighborhoods.'.format(
        len(df_geo['Borough'].unique()),
        df_geo.shape[0]
    )
)


# ### 3.3. Mapping out the neighborhoods in Toronto:

# In[7]:


#get the geospatial data for Toronto
address = 'Toronto, ON'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of New York City are {}, {}.'.format(latitude, longitude))


# In[8]:


# create map of New York using latitude and longitude values
map_toronto = folium.Map(location=[43.6534817, -79.3839347], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(df_geo['Latitude'], df_geo['Longitude'], df_geo['Borough'], df_geo['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# ### 3.4. Number of Neighborhoods in Toronto:

# In[9]:


#bar graph for number of neighborhoods for every borough in Toronto
plt.figure(figsize=(7,7), dpi = 80)
# title
plt.title('Number of Neighborhoods in Toronto')
#On x-axis
plt.xlabel('Boroughs', fontsize = 15)
#On y-axis
plt.ylabel('Number of Neighborhoods', fontsize=15)
#giving a bar plot
df_geo.groupby('Borough')['Neighborhood'].count().plot(kind='bar', color='red')
#legend
plt.legend()
#displays the plot
plt.show()


# ### 3.5. Shortlisting neighborhoods for assesment:

# ##### _From the bar graph, we can see that Scarborough has 18 neighborhoods and Etobicoke has 12 neighborhoods. Although the number of neighborhoods is not the same, the locations of these boroughs serves the purpose of this project._

# In[10]:


Scarborough_data = df_geo[df_geo['Borough'] == 'Scarborough'].reset_index(drop=True)
Scarborough_data.head()


# In[11]:


Etobicoke_data = df_geo[df_geo['Borough'] == 'Etobicoke'].reset_index(drop=True)
Etobicoke_data.head()


# ### 3.6. Foursquare

# ##### _Foursquare login_

# In[12]:


CLIENT_ID = 'PGGUSXZ4ZLRK2RQDRUI0QN3UZFQ1YNKTUELSWYZNMJIUFKVO' # your Foursquare ID
CLIENT_SECRET = 'L2VOBN33JLX1W0CXGR2HCEWA3I0KFN0XBE01EP5QCHW0AGFC' # your Foursquare Secret
VERSION = '20180604' # Foursquare API version


# ##### _Define a function that uses Foursquare API to retrieve (LIMIT) venues for a given radius around any coordinates._

# In[13]:


def get_venues(lat,lng):
    #set variables
    radius= 5000
    LIMIT=100
    #Foursquare API
    url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
    # get all the data
    results = requests.get(url).json()
    venue_data=results["response"]['groups'][0]['items']
    venue_list=[]
    for row in venue_data:
        try:
            venue_id=row['venue']['id']
            venue_name=row['venue']['name']
            venue_category=row['venue']['categories'][0]['name']
            venue_list.append([venue_id,venue_name,venue_category])
        except KeyError:
            pass
    column_names=['ID','Name','Category']
    venues = pd.DataFrame(venue_list,columns=column_names)
    return venues


# ### 3.7. Analyzing the Boroughs 

# #### 3.7.1. Scarborough

# ##### _Getting the coordinates of the borough_

# In[14]:


address = 'Scarborough, ON'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# ##### _Searching for restaurants in the Scarborough._

# In[15]:


LIMIT = 100
search_query = 'Restaurant'
radius = 5000 #in meters
print(search_query + ' .... OK!')


# In[16]:


#URL to access Foursquare API
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# #####  _Creating a database of restaurants in Scarborough within a given radius._ 

# In[17]:


# Scarborough Venues Dataframe
results = requests.get(url).json()
venues = results['response']['venues']

# tranform venues into a dataframe
Scarborough_venues = pd.json_normalize(venues)
Scarborough_venues.head()


# ##### _Refining the dataset._

# In[18]:


# keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories'] + [col for col in Scarborough_venues.columns if col.startswith('location.')] + ['id']
Scarborough_filtered = Scarborough_venues.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
Scarborough_filtered['categories'] = Scarborough_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
Scarborough_filtered.columns = [column.split('.')[-1] for column in Scarborough_filtered.columns]

Scarborough_filtered.head()


# ##### _Finding the frequency of each type of cuisine._

# In[19]:


#find frequencies of restaurants of top cuisines
column_names=['Borough', 'Neighborhood', 'ID','Name']
venues=pd.DataFrame(columns=column_names)
i=1
for row in Scarborough_data.values.tolist():
    PostalCode,Borough, Neighborhood, Latitude, Longitude=row
    locations = get_venues(Latitude,Longitude)
    resturants=locations[locations['Category']=='Restaurant'] 
    print('(',i,'/',len(Scarborough_data),')','Resturants in '+Neighborhood+', '+Borough+':'+str(len(resturants)))
    print(row)
    for resturant_info in resturants.values.tolist():
        id, name , category=resturant_info
        venues = venues.append({'Borough': Borough,
                                'Neighborhood': Neighborhood, 
                                'ID': id,
                                'Name' : name
                                }, ignore_index=True)
    i=i+1


# #### 3.7.2. Etobicoke

# ##### _Getting the coordinates of the borough_

# In[20]:


address = 'Etobicoke, ON'
geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# ##### _Searching for restaurants in the Etobicoke._

# In[21]:


LIMIT = 100
search_query = 'Restaurant'
radius = 5000 #in meters
print(search_query + ' .... OK!')


# In[22]:


#URL to access Foursquare API
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# ##### _Creating a database of restaurants in Etobicoke within a given radius._

# In[23]:


# Etobicoke Venues Dataframe
results = requests.get(url).json()
venues = results['response']['venues']
# tranform venues into a dataframe
Etobicoke_venues = pd.json_normalize(venues)
Etobicoke_venues.head()


# ##### _Refining the dataset._

# In[24]:


# keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories'] + [col for col in Etobicoke_venues.columns if col.startswith('location.')] + ['id']
Etobicoke_filtered = Etobicoke_venues.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
Etobicoke_filtered['categories'] = Etobicoke_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
Etobicoke_filtered.columns = [column.split('.')[-1] for column in Etobicoke_filtered.columns]

Etobicoke_filtered.head()


# ##### _Finding the frequency of each type of cuisine._

# In[25]:


#find frequencies of restaurants of top cuisines
column_names=['Borough', 'Neighborhood', 'ID','Name']
venues=pd.DataFrame(columns=column_names)
i=1
for row in Etobicoke_data.values.tolist():
    PostalCode,Borough, Neighborhood, Latitude, Longitude=row
    locations = get_venues(Latitude,Longitude)
    resturants=locations[locations['Category']=='Restaurant'] 
    print('(',i,'/',len(Etobicoke_data),')','Resturants in '+Neighborhood+', '+Borough+':'+str(len(resturants)))
    print(row)
    for resturant_info in resturants.values.tolist():
        id, name , category=resturant_info
        venues = venues.append({'Borough': Borough,
                                'Neighborhood': Neighborhood, 
                                'ID': id,
                                'Name' : name
                                }, ignore_index=True)
    i=i+1


# ### 3.8. Data Visualization: Graphs and Maps

# #### 3.8.1. Graphs:

# ##### _Scarborough:_

# In[26]:


Scarborough_filtered.groupby('categories')['name'].count().plot.barh(figsize=(10,5), color = 'red')
plt.title('Popular cuisines in Scarborough', fontsize = 10)
plt.xlabel('Number of Resturants', fontsize = 10)
plt.ylabel('Types of Restaurants', fontsize= 10)
plt.xticks(rotation = 'horizontal')
plt.show()


# ##### _Etobicoke:_

# In[27]:


Etobicoke_filtered.groupby('categories')['name'].count().plot.barh(figsize=(10,6), color = 'red')
plt.title('Popular cuisines in Etobicoke', fontsize = 10)
plt.xlabel('Number of Resturants', fontsize = 10)
plt.ylabel('Types of Restaurants ', fontsize= 10)
plt.xticks(rotation = 'horizontal')
plt.show()


# #### 3.8.2. Maps:

# ##### _Scarborough:_

# In[28]:


Scarborough_map = folium.Map(location=[43.773077,-79.257774], zoom_start=10) # generate map centred around the Scarborough

# add a red circle marker to represent Scarborough
folium.features.CircleMarker(
    [43.773077,-79.257774],
    radius=10,
    color='red',
    popup='Scarborough',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(Scarborough_map)

# add the restaurants as blue circle markers
for lat, lng, label in zip(Scarborough_filtered.lat, Scarborough_filtered.lng, Scarborough_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(Scarborough_map)

# display map
Scarborough_map


# ##### _Etobicoke:_

# In[29]:



Etobicoke_map = folium.Map(location=[43.6435559,-79.5656326], zoom_start=13) # generate map centred around the Conrad Hotel

# add a red circle marker to represent Etobicoke
folium.features.CircleMarker(
    [43.6435559,-79.5656326],
    radius=10,
    color='red',
    popup='Etobicoke',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(Etobicoke_map)

# add the restaurants as blue circle markers
for lat, lng, label in zip(Etobicoke_filtered.lat, Etobicoke_filtered.lng, Etobicoke_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(Etobicoke_map)

# display map
Etobicoke_map


# ## 4. Results:

# ##### _Chinese cuisine is the most popular in both boroughs._
# 
# ##### _American cuisine is more popular in Etobicoke. While Caribbean cuisine is more popular in Scarborough._
# 
# ##### _Scarborough’s cuisine is influenced by Asian, Caribbean and American cuisines with very little European influence._
# 
# ##### _Etobicoke’s cuisine is influenced by Asian, American, European and Middle Eastern Cuisine.  Mediterranean cuisine has very little influence here._
# 

# ## 5. Discussion:

# ##### _Given the high migration rates of Asians to Canada, it is expected that a category of the Asian cuisine would be the most popular in the region.  Surprisingly, though the South Asians form a greater percentage of the population than the Chinese, (as per https://en.wikipedia.org/wiki/Demographics_of_Toronto), there are more Chinese restaurants than restaurants of all South Asian cuisines combined._
# 
# 
# ##### _From the Folium map of Scarborough, we see that, there are more restaurants towards the North, than there are towards the South. Most restaurants are located within a two block radius of the center of Scarborough. The Folium map of Etobicoke shows the exact opposite trend. Restaurants are located away from the center of the borough. Also, there are more restaurants in the South than there are in the North of Etobicoke. The layout of restaurants in the restaurant dense neighborhoods of both boroughs is roughly similar._
# 
# ##### _Another interesting fact about this data is that each borough has exactly 1 Dim Sum/ Dumpling,      Indian and Italian restaurant. The boroughs also have exactly 2 Korean restaurants._
# 

# ## 6. Conclusion:

# ##### _From this analysis we learnt that both the most popular cuisine in Etobicoke and Scarborough is Chinese. While Scarborough has mostly Asian, Caribbean, European and American gastronomic influences, Etobicoke has Far East Asian and Asian, American, European and Mediterranean  influences in its cuisine. Therefore, despite the fewer number of neighborhoods, the borough with the greatest gastronomic diversity is Etobicoke. So, for those who enjoy or wish to experience a variety of cuisines, Etobicoke is the place to be._
