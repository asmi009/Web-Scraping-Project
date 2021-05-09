import timeit
start = timeit.default_timer()

from bs4 import BeautifulSoup #to scrape webpage
import requests #to get send request on website and get response
import pandas as pd #to make dataframe
import numpy as np

#Getting Website Response
get_website = requests.get("https://www.worldometers.info/coronavirus/")

#Getting Website's Html code as a string
web_html = get_website.text

# Send String Html code in BS4 to parse html
soup = BeautifulSoup(web_html, "html.parser")

# Retreiving table which id is "main_table_countries_today"
table = soup.find("table", {"id": "main_table_countries_today"})


# Getting Heading of table

# Make empty list to append all my heading later
heading = []

# Find all the th tags from our table
head = table.find_all("th")
for i in head:
    heading.append(i.text)

# Find all the tr tags from our table
table_rows = table.find_all('tr')

# Make empty list to append all the data from tr.
res = []

# We are going in every tr by help of loop
for i in table_rows:
    try:
        # Giving every tr tag to bs4
        soup = BeautifulSoup(str(i), "html.parser")

        # We are finding all the td tags in tr with bs4
        td = soup.find_all("td")

        # We make new empty list to append single row of data
        row = []
        for i in td:
            # appending single row data in row list
            row.append(i.text)

        # appending all the rows in our main list where all the rows exists.
        res.append(row)

    except:
        pass

#getting only Countries Data by slicing the list
res = res[9:-9]
#print(res)

# Making dataframe
df = pd.DataFrame(res, columns=heading)

#Set the option to display all the rows
pd.set_option('display.max_rows', None)

print(df)

# uncomment below print to see the data types before conversion
#print(df.dtypes)

#as all our features/variables are stored as objects in the dataframe 
#to apply descriptive analysis we need to convert them to numerics, integers and float 
df['TotalCases'] = df['TotalCases'].str.replace(',', '').astype(int)

df['TotalDeaths'] = df['TotalDeaths'].replace(r'^\s+$', '0', regex=True)
df['TotalDeaths'] = df['TotalDeaths'].str.replace(',', '').astype(int)
df['Active Cases/1M pop'] = df['Active Cases/1M pop'].str.replace(',', '').replace('', '0').astype(float)
df['NewCases'] = df['NewCases'].str.replace(',', '').replace('', '0').astype(int)
df['NewDeaths'] = df['NewDeaths'].str.replace(',', '').replace('', '0').astype(int)
df['TotalRecovered'] = df['TotalRecovered'].str.replace(',', '').replace('', '0').astype(int)
df['NewRecovered'] = df['NewRecovered'].str.replace(',', '').replace('', '0').astype(int)
df['ActiveCases'] = df['ActiveCases'].str.replace(',', '').replace('', '0').astype(int)
df['Serious,Critical'] = df['Serious,Critical'].str.replace(',', '').replace('', '0').astype(int)
df['1 Deathevery X ppl'] = df['1 Deathevery X ppl'].str.replace(',', '').replace('', '0').astype(int)
df['New Cases/1M pop'] = df['New Cases/1M pop'].str.replace(',', '').replace('', '0').astype(float)
df['1 Testevery X ppl'] = df['1 Testevery X ppl'].str.replace(',', '').replace('', '0').astype(int)
df['New Deaths/1M pop'] = df['New Deaths/1M pop'].str.replace(',', '').replace('', '0').astype(float)
df['TotalTests'] = df['TotalTests'].str.replace(',', '').replace('', '0').astype(int)
df['Tot Cases/1M pop'] = df['Tot Cases/1M pop'].str.replace(',', '').replace('', '0').astype(float)
df['Deaths/1M pop'] = df['Deaths/1M pop'].str.replace(',', '').replace('', '0').astype(float)
df['Tests/\n1M pop\n'] = df['Tests/\n1M pop\n'].str.replace(',', '').replace('', '0').astype(float)
df['1 Caseevery X ppl'] = df['1 Caseevery X ppl'].str.replace(',', '').replace('', '0').astype(int)
df['Population'] = df['Population'].replace(r'^\s+$', '0', regex=True)
df['Population'] = df['Population'].str.replace(',', '').astype(int)

df.describe()
from matplotlib import pyplot as plt
ax = plt.gca()
df.plot(kind='line',x='TotalCases',y='TotalDeaths',ax=ax) #This allows us to plot Total Cases agianst Total Deaths and we 
#can see that both have an increasing trend 
plt.show()

# create dummy variable them group by that
# set the legend to false because we'll fix it later
df.assign(dummy = 1).groupby(
  ['dummy','Continent']).size().to_frame().unstack().plot(kind='bar',stacked=True,legend=False)

plt.title('Distribution of cases by Continent')

# other it'll show up as 'dummy' 
plt.xlabel('Country')

# disable ticks in the x axis
plt.xticks([])

# fix the legend
current_handles, _ = plt.gca().get_legend_handles_labels()
reversed_handles = reversed(current_handles)

labels = reversed(df['Continent'].unique())

plt.legend(reversed_handles,labels,loc='lower right')
plt.show()

#As we can see Asian Continent is the most representative mainly due to recent surge in covid cases in India.

# uncomment below print to see data types after conversion
#print(df.dtypes)

# uncomment below to see full dataframe
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #print(df)
    
print(df)


df.describe(include='all')
# This above describe() function is used to generate descriptive statistics that summarizes 
#the central tendency, dispersion and shape of a dataset’s distribution, excluding NaN values.


stop = timeit.default_timer()

print('Time: ', stop - start)
