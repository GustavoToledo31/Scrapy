# Scrapy Projects
1. OLX
2. PalmeirasTitles

## OLX 

### The project consists in a web scraping on OLX page that returns a database containing properties informations.

How to run the code:

1- First pull all the "OLX" fold
2- Install scrapy and numpy packages
3- Open your CMD, go to the fold "OLX" and run the command: scrapy crawl olx -o Extracted_Data.csv

After doing this, you'll see that a new file has been created. The file name will be "Extracted_Data.csv" and it'll contain aproximately 5000 rows of informations about properties scraped from OLX website.

Obs: When you run the code in CMD the code takes a while to execute and a lot of information will appear, don't be afraid of that.

## PalmeirasTitles

### The project consists in a web scraping of Palmeiras Futebol Team Titles.

This project was just a test and extract a few information.

How to run the code:

1- First pull all the "PalmeirasTitles" fold
2- Install scrapy package
3- Open your CMD, go to the fold "PalmeirasTitles" and run the command: scrapy crawl Palmeiras -o Palmeiras_Titles_Data.csv

After doing this, you'll see that a new file has been created. The file name will be "PalmeirasTitles.csv" and contain a few informations about Palmeiras titles.