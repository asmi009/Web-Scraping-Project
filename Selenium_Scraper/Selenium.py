# Importing Libraries
import timeit

start = timeit.default_timer()
from selenium import webdriver #importing webdriver from selenium
import pandas as pd #importing pandas for dataframe
driver = webdriver.Chrome(executable_path="C:\\Users\\muhammad usman\\Downloads\\chromedriver.exe") #Getting chrome from webdriver, you have to give path of your chromedriver here
driver.get("https://www.worldometers.info/coronavirus/") #We are using get method of webdriver for opening the website

driver.implicitly_wait(10) #We are giving wait to webdriver for 10 seconds to find elements in giving time

heading = [] #Making empty list, will append here our th
table = driver.find_element_by_id("main_table_countries_today") #Finding table element by id 
head = table.find_elements_by_xpath("//table[@id='main_table_countries_today']//th") #Finding th tags by xpath from table

for i in head:
    heading.append(i.text) #Appending head elements to our already made heading list
    
table_rows = table.find_elements_by_tag_name("tr") #Finding rows by tag name from our table 

res = [] # Making empty list, will append here our all rows data

for tr in table_rows:
    td = tr.find_elements_by_tag_name("td") #Finding elements td by tag name from our rows
    
    row = [] # Making empty list, will append here our single row
    for i in td:
        row.append(i.text) 
        
    res.append(row) #Appending single rows to our rows data
heading_final = [] #Making final list for heading
for i in heading:
    i = i.replace("/", " ") # removing / from our heading elements
    i = i.replace("\n", " ") # removing \n from our heading elements
    heading_final.append(i) # appending ((/,\n) removed from head) in our final heading list
    
#Now we are removing blank list from our all rows list
for i in res: 
    if i == ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']: # We are removing row, if row equals to completely blank
        res.remove(i)
        
res = res[1:-8] # Getting only countries data by slicing the all rows data list
df = pd.DataFrame(res, columns=heading_final) # Making dataframe
pd.set_option('display.max_rows', None) #Set the option to display all the rows
df# Printing dataframe

stop = timeit.default_timer()

print('Time: ', stop - start)
