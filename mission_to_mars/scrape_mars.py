#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time

def scrape():


    #Create path for chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#   Create browser variable to open headless browser for chromedriver
    browser = Browser('chrome', **executable_path, headless=False)

    #Create news_url variable of page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    #Visit url via browser
    browser.visit(news_url)
    time.sleep(3)
    #Create html variable via browser
    html = browser.html
    #Create news_soup vairable via bs
    news_soup = BeautifulSoup(html, 'html.parser')

    #Get the latest news title and paragraph. Index 0 for first.
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text


    #Create variables for jpl basic url and jpl Mars image to be scraped
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(images_url)
    time.sleep(3)

    html = browser.html

    images_soup = BeautifulSoup(html, 'html.parser')

    #Create variable to hold path to image
    relative_image_path = images_soup.find_all('img')[3]["src"]
    #Create variable for path to featured image
    featured_image_url = jpl_nasa_url + relative_image_path


    #Create variable for Mars facts to be scraped
    facts_url = 'https://space-facts.com/mars/'

    #Read in pandas
    facts_list = pd.read_html(facts_url)

    facts_df = facts_list[0]

    #Rename columns
    facts_df.columns = ["Description", "Value"]


    #Convert the pandas  python to html for use later in flask
    mars_html_table = facts_df.to_html()


    #Ditch /n from pandas and make legible in html string as per the instructions
    clean_mars_html_table = mars_html_table.replace('\n', '')

    #Create variable for Mars hemisphere name and image to be scraped
    usgs_url = 'https://astrogeology.usgs.gov'

    #Create variable for Mars hemisphere name and image to be scraped
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # browser.visit(hemispheres_url)
    time.sleep(3)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')

    # #Create variables for Mars hemispheres products data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    # #Create empty list for loop to create list of dictionaries
    hemisphere_image_urls = []

    # #Loop through each hemisphere data
    for x in mars_hemispheres:
         #Scrape title
        hemisphere = x.find('div', class_="description")
        title = hemisphere.h3.text
        
    #     #Scrape image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)
        time.sleep(3)
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

    #     #Create dictionary for title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        
    #     #Append dictionary to list
        hemisphere_image_urls.append(image_dict)

    my_dict = {}
    my_dict["news_title"] = news_title
    my_dict["news_p"] = news_p
    my_dict["featured_image_url"] = featured_image_url
    my_dict["clean_mars_html_table"] = clean_mars_html_table
    my_dict["hemisphere_image_urls"] = hemisphere_image_urls

    return my_dict


