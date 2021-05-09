#Importing Libraries
import scrapy
from bs4 import BeautifulSoup
import csv

class WorldometerSpider(scrapy.Spider): #Making main class of scrapy
    name = "worldometer" #Defining name for scrapy bot

    start_urls = ["https://www.worldometers.info/coronavirus/"] #Giving our website url, which we are going to scrape

    def parse(self, response):

        # Getting Heading of our data
        head = response.xpath("//table[@id='main_table_countries_today']//th") #We are getting th of table by using response.xpath method of scrapy and saving them to head variable.
        heading = [] #Making blank list for heading, We will save our head in this list
        for i in range(len(head)):
            # We are trying to get only text of th
            i = head[i].get().split('">') #Spliting th element by >
            i = i[1].replace("</th>","") # Removing </th>
            i = i.replace("<br>"," ") # Removing <br>
            heading.append(i) #Now we have only text of th, so we are appending our required in our already made heading list

        # Getting Data
        table_rows = response.xpath("//table[@id='main_table_countries_today']//tr").getall() # Getting tr's of table
        res = [] #Making empty, will append here all our rows data
        for i in table_rows:
            # to get text of td, we have to use some beautifulsoup
            td_txt = BeautifulSoup(i, "html.parser") # Giving our tr elements to beautifulsoup as string
            td_txt = td_txt.find_all("td") # Finding all the td available in tr's
            row = [] # Making empty list, will append here our single row data
            for i in td_txt:
                row.append(i.text) # appending single row data in our already made list

            res.append(row) #Appending all single rows data to our all data list

        res = res[9:-8] # Slicing for getting only countries data



        # Saving Data in csv
        with open("data.csv", 'a' , newline='') as csvfile: #Opening csv file
            writer = csv.writer(csvfile, dialect="excel") # Writing csv file
            writer.writerow(heading) # Giving header to our csv file
            for i in res:
                writer.writerow(i) # writer is appending data row by row

            #It will save the file as data.csv in same directory of this code file.



