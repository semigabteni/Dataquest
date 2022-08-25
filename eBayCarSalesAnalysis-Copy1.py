#!/usr/bin/env python
# coding: utf-8

# # Cleaning and analyzing eBay Car Sales Data
# 
# **objective**: analysis of eBay Car Sales
# **Dataset**: eBay Kleinanzeigen, a classifieds section of the German eBay website
# 
# ** Data dictionary**
# * dateCrawled - When this ad was first crawled. All field-values are taken from this date.
# * name - Name of the car.
# * seller - Whether the seller is private or a dealer.
# * offerType - The type of listing
# * price - The price on the ad to sell the car.
# * abtest - Whether the listing is included in an A/B test.
# * vehicleType - The vehicle Type.
# * yearOfRegistration - The year in which which year the car was first registered.
# * gearbox - The transmission type.
# * powerPS - The power of the car in PS.
# * model - The car model name.
# * kilometer - How many kilometers the car has driven.
# * monthOfRegistration - The month in which which year the car was * first registered.
# * fuelType - What type of fuel the car uses.
# * brand - The brand of the car.
# * notRepairedDamage - If the car has a damage which is not yet repaired.
# * dateCreated - The date on which the eBay listing was created.
# * nrOfPictures - The number of pictures in the ad.
# * postalCode - The postal code for the location of the vehicle.
# * lastSeenOnline - When the crawler saw this ad last online.
# 

# In[1]:


import pandas as pd


# In[2]:


autos = pd.read_csv("autos.csv", encoding='Latin-1')


# In[3]:


autos


# In[4]:


autos.info()


# ## Adjusting and rewording column names

# In[5]:


column_names = autos.columns
print(column_names)


# In[6]:


autos.rename({
    "yearOfRegistration" : "registration_year",
    "monthOfRegistration" : "registration_month",
    "notRepairedDamage" : "unrepaired_damage",
    "dateCreated" : "ad_created",
    'dateCrawled' : 'date_crawled',
    'offerType' : 'offer_type',
    'vehicleType' : 'vehicle_type',
    'fuelType' : 'fuel_type',
    'nrOfPictures' : 'nr_of_pictures',
    'postalCode' : 'postal_code',
    'lastSeen' : 'last_seen'},
    axis=1,
    inplace=True)


# In[7]:


print(autos.columns)


# ## Let's look for redundant or unnecessary columns

# In[8]:


autos.describe(include = 'all')


# **Observations**
# * 'seller' is systematically "privat" but for one entry
# * 'offer_type' is systematically "angebot" but for one entry
# * 'nf_of_pictures' is systematically 0
# 
# **Conclusion**
# * We'll drop all 3 columns

# In[9]:


autos.drop(labels=["offer_type", "nr_of_pictures", "seller"], axis=1, inplace=True)


# ## Let's convert to numeric values where relevant

# In[10]:


autos["price"] = (autos["price"]
                  .str.replace("$","")
                  .str.replace(",","")
                  .astype(int))

autos["price"].head()


# In[11]:


autos['odometer'] = (autos['odometer']
                     .str.replace("km","")
                     .str.replace(",","")
                     .astype(int))
autos.rename({'odometer' : 'odometer_km'}, axis=1, inplace=True)
autos['odometer_km'].head()


# ## Let's look for inconsistent data

# In[12]:


print(autos[['odometer_km', 'price']].describe())
print(autos['odometer_km'].value_counts())
print(autos['price'].value_counts())


# **Observations**
# * 1421 cars which price is zero.
# * A maximum car price of '$100,000,000'. 
# 
# **Questions**
# * How many cars have unrealistically low price?
# * How many cars have unrealistically high prices ?

# In[13]:


autos['price'].value_counts().head()


# In[14]:


autos['price'].value_counts().sort_index(ascending=False).head(20)


# **Conclusions**
# * Mileage information looks consistent. unsurprisingly, cars sold on eBay have a higher mileage in general
# * We'll consider the zero price cars as outliers, and remove them
# * As well as the cars with a price above '$500,000'

# In[15]:


autos = autos[(autos['price'] > 0) & (autos['price'] < 500000)]


# In[35]:





# In[16]:


autos['price'].describe()


# # Cleaning and analysis of date informations
# We focus on the date fields of the data set
# * date_crawled
# * last_seen
# * ad_created
# * registration_month
# * registration_year
# 
# **Objective**
# We want to analyze the date range covered by the data set

# In[17]:


autos[['date_crawled', 'last_seen', 'ad_created', 'registration_month', 'registration_year']].info()


# **Observations**
# * date_crawled, last_seen, ad_created are stored as string objects. We will need to convert them for data range analysis
# * registration_month and registration_year are stored as numerical values which allows analysis
# 
# Let's start preparing the first three columns for analysis

# In[18]:


autos[['date_crawled', 'last_seen', 'ad_created']].head()


# **Observations**
# * The date is stored in the first 10 characters of the string for each column
# * The remainder of the string indicates a time of day, which we don't need for the moment
# 
# **Conclusion**
# * Let's focus on the 10 first characters for each of the strings
# * We don't want to drop the rest of the information, so we start by duplicating the data of interest

# In[19]:


crawled_dates = autos['date_crawled'].str[:10]
created_dates =  autos['ad_created'].str[:10]
last_seen_dates =  autos['last_seen'].str[:10]


# *Analysis of date_crawled*

# In[20]:


crawled_dates.value_counts(normalize=True, dropna=False)


# In[21]:


(crawled_dates
 .value_counts(normalize=True, dropna=False)
 .sort_index())


# **Observations**
# * Ads were crawled daily and uniformally over the perios, but for 6 dates with lower frequency
# * date_crawled ranges from March 5th trough April 7th

# *Analysis of ad_created*

# In[22]:


created_dates.value_counts(normalize=True, dropna=False)


# In[23]:


(created_dates
 .value_counts(dropna=False)
 .sort_index()
 .head(20))


# In[24]:


(created_dates
 .value_counts(dropna=False)
 .sort_index()
 .tail(40))


# **Observations**
# * Ads were created from June 11th, 2015 through April 7th, 2016
# * While older ads are very few as the items are not on sale anymore, but exceptionally, the latest ads are less. Possible explanation: it may take a few days for an author to complete the information for an ad.
# * The bulk of the creation dates start from March 5th, 2016

# *Analysis of last_seen dates*

# In[25]:


last_seen_dates.value_counts(normalize=True, dropna=False)


# In[26]:


(last_seen_dates
 .value_counts(dropna=False)
 .sort_index())


# **Observations**
# * last seen date of an ad can be assumed to be the date the ad was removed
# * Almost half the ads were last seen by the crawler in the last 3 days of the period. The crawler may not crawl through all ads every day, which explains why a bigger amount of ads were last seen on the past 3 days
# * As one goes back in time, there are, overall, less ads that were last seen on a given date
# 
# **Recap on date ranges observations**
# * Ads were created from June 11th, 2015 through April 7th, 2016
# * The bulk of the creation dates start from March 5th, 2016
# * Ads were crawled from March 5th trough April 7th, 2016
# * Ads were last seen from March 5th, 2016, with half of them in the latest 3 days of April 2016

# **Registration year analysis**

# In[27]:


autos['registration_year'].describe()


# **Observations**
# * Registration years concentrate in a period of 10 years around 2004
# * We observe unrealistic registration years whether in the past or in the future, which requires cleaning
# 

# ## Cleaning for unrealistic registration dates

# In[28]:


(autos['registration_year']
 .value_counts(dropna=False)
 .sort_index()
 .head(20))


# In[29]:


(autos['registration_year']
 .value_counts(dropna=False)
 .sort_index()
 .tail(20))


# **Observations**
# * We confirm the presence of inconsistent -too old or future- registrations. There are less than 2000 such records, which is less than 4% of our records. Thus we shouldn't be losing significant data
# 
# **Required corrections**
# * Obviously, we should discard ads with registration years before 1900
# * We should also discard registrations which are after the ads date range, that is 2017 registrations and beyond

# In[32]:


autos = autos[autos['registration_year'].between(1900,2016)]

(autos['registration_year']
 .value_counts(normalize=True)
 .head(20))


# In[34]:


(autos['registration_year']
 .value_counts(normalize=True)
 .tail(20))


# **Observations**
# * The bulk of cars were registered in the late 1990s, with a concentration in the 1999 - 2005 period
# * More recent cars, registered in 2010 and after, are less, as we are dealing with second hand car market
# * There is a long tail of older registrations which goes back to the 1930s

# ## Analysis by brand, aggregation ##

# *Which brands should we focus on?*

# In[46]:


brand_count = (autos["brand"]
 .value_counts(normalize=True, dropna=False)
 .sort_values(ascending=False)
)


# In[70]:


top_brands = brand_count[brand_count > 0.05].index
print(top_brands)


# **Observations**
# * 6 brands have a market share of 5% or more, we'lll focus on those

# In[73]:


mean_price_dict = {}
for brand in top_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_price = brand_only["price"].mean()
    mean_price_dict[brand] = int(mean_price)


# In[74]:


print(mean_price_dict)


# **Observations**
# * Audi is the most expensive brand, while Opel is the cheapest, among the most sold cars in the german second hand market represented by eBay
# * The Ausi mean price is 3 times the Opel mean price
# * Mercedes and BMW are the 2 other expensive brands, Ford is the second cheapest brand, Volkswagen is the mid range brand

# ## Cross-analysis of price and mileage 
# 
# *We first build the relevant mileage data
# 
# *We first build the relevant pandas data structure

# In[75]:


mean_mileage_dict = {}
for brand in top_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_mileage = brand_only["odometer_km"].mean()
    mean_mileage_dict[brand] = int(mean_mileage)


# In[76]:


print(mean_mileage_dict)


# *Create series objects out of the 2 data dictionnaries*

# In[77]:


mean_price_series = pd.Series(mean_price_dict)


# In[78]:


mean_mileage_series = pd.Series(mean_mileage_dict)


# *Create a dataframe with the first series (mean price)*

# In[82]:


cross_analysis_df = pd.DataFrame(mean_price_series, columns=['mean_price'])


# *Add the second series (mean mileage) to the dataframe*

# In[84]:


cross_analysis_df['mean_mileage'] = mean_mileage_series


# In[87]:


(cross_analysis_df
 .sort_values('mean_price')
 .head(6))


# **Observations**
# * Mean mileages are close across the 6 most sold brands in the second hand eBay market
# * They differ by 8000km at most, that is 6% or less
# * Mean prices differ much more with up to x3 differences 
# * The lost mean mileage brand is actually the second cheapest, and the most expensive brand has average mean mileage
# 
# **Conclusion**
# * Mileage has no significant impact on brand mean price, though a small correlation may be observed

# In[ ]:




