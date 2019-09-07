from flask import Flask, render_template
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd
import numpy as np




executable_path = {'executable_path': 'C:/Users/jamie/Documents/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)



def new_news():
    url ='https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    articles = soup.find_all('div', class_='image_and_description_container')
    time.sleep(5)
    
    news_title=[]
    news_p=[]
    
    try:
        for article in articles:
            h3 = article.find('h3').text
            teaser = article.find('div',class_="article_teaser_body").text
            news_title.append(h3)
            news_p.append(teaser)

    except:
        print("\nScraping Complete")

    latest_news = [news_title[0],news_p[0]]
    return(latest_news)
    


def fetured_img():
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    big_picture = soup.find("article", class_="carousel_item")['style']
    big_picture = big_picture.replace('background-image: url(', '').replace(');', '')
    big_picture = big_picture.replace("'","").replace("'","")
    featured_url = "https://jpl.nasa.gov" + big_picture
    return(featured_url)



def weather_tweet():
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find_all("p", class_="tweet-text")[1].get_text("InSight sol")

    return(mars_weather)



def mars_table():
    res = requests.get("https://space-facts.com/mars/")
    soup = bs(res.content,'lxml')
    table = soup.find_all('table')[1] 
    mars_facts = pd.read_html(str(table))
    mars_facts_df = pd.DataFrame(mars_facts[0])
    mars_html = mars_facts_df.to_html()
    return(mars_html)




def mars_dictio():
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    products = soup.find_all('div',class_='collapsible')
    time.sleep(5)

    for link in products:
        name = link.find_all('h3')

    title = []
    x = 0
    for value in name:
        title.append(name[x].text)
        x+=1


    image_url = []
    x = 0
    for value in titles:
        browser.click_link_by_partial_text(f'{titles[x]}')
        html = browser.html
        soup = bs(html, 'html.parser')
        time.sleep(3)
        ur_addr = soup.find("a",target="_blank")["href"]
        image_url.append(ur_addr)
        browser.visit(url)
        time.sleep(5)
        x+=1

    hemisphere_image_urls = [ {'title': title[i], 'image_url': image_url[i] } for i in range(len(title)) ]
    return(hemisphere_image_urls)