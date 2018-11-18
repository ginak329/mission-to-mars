from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import os
import pandas as pd
import time
import requests
import pymongo
import tweepy


def scrape():
    mars_dict={}

    url1="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    html=requests.get(url1)
    soup=BeautifulSoup(html.text,'html.parser')

    news_title=soup.find('div','content_title','a').text
    news_p=soup.find('div','rollover_description_inner').text




    print("News Title:", news_title)
    print("News Paragraph Text:",'\n', news_p)

    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p



    url2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    executable_path={'executable_path':'chromedriver.exe'}
    browser=Browser('chrome')
    browser.visit(url2)




    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    image=soup.find("img",class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url=img_url
    print("Featured Image URL:", featured_image_url)

    mars_dict['featured_image']=featured_image_url


    url3="https://twitter.com/marswxreport?lang=en"
    from key_vault import (consumer_key, consumer_secret, access_token, access_token_secret)



    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth,parser=tweepy.parsers.JSONParser())

    target_user="marswxreport"
    tweet=api.user_timeline(target_user,count=1)[0]
    mars_weather=tweet['text']
    print("The latest tweet:", mars_weather)

    mars_dict['mars_weather']=mars_weather


    url4="https://space-facts.com/mars/"
    mars_facts = pd.read_html(url4)
    mars_df = mars_facts[-1]
    mars_df=mars_df.rename(columns={0:"Description",1:"Value"})
    mars_html=mars_df.to_html()
    mars_dict['mars_html']=mars_html



    url5="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    executable_path={'executable_path':'chromedriver.exe'}
    browser=Browser('chrome')
    browser.visit(url5)

    html_hemispheres=browser.html
    soup=BeautifulSoup(html_hemispheres,'html.parser')
    links=soup.find_all('div',class_="item")
    mars_hemisphere = []
    for link in links:
    
        title=link.find('h3').text
        title=title.replace("Enhanced","")
        endlink=link.find("a")
        imagelink="https://astrogeology.usgs.gov"+ str(endlink.attrs['href'])
    
        browser.visit(imagelink)
        soup=BeautifulSoup(browser.html,"html.parser")
        downloads=soup.find("div",class_="downloads")
        
        imageurl=downloads.find("a").attrs["href"]
        mars_hemisphere.append({"title":title, "img_url":imageurl})
        

    mars_dict['mars_hemisphere']=mars_hemisphere
    return mars_dict