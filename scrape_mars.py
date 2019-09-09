from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd
import numpy as np
import pymongo

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.items

executable_path = {'executable_path': 'C:/Users/jamie/Documents/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)



def new_news():
    url ='https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    articles = soup.find_all('div', class_='image_and_description_container')
    time.sleep(10)
    
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

    latest_news = {'title': news_title[0], 'news_teaser': news_p[0] }
    db.latest_news.insert_one(latest_news)
    
    return()
    


def featured_img():
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    big_picture = soup.find("article", class_="carousel_item")['style']
    big_picture = big_picture.replace('background-image: url(', '').replace(');', '')
    big_picture = big_picture.replace("'","").replace("'","")
    img_url = "https://jpl.nasa.gov" + big_picture
    featured_url = {'featured_img': img_url}
    db.latest_news.insert_one(featured_url)
    
    return()



def weather_tweet():
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find_all("p", class_="tweet-text")[3].get_text("InSight sol")
    mars_tweet = {'latest_weather': mars_weather}
    db.latest_news.insert_one(mars_tweet)
    
    return()



def mars_table():
    res = requests.get("https://space-facts.com/mars/")
    soup = bs(res.content,'lxml')
    table = soup.find_all('table')[1] 
    mars_facts = pd.read_html(str(table))
    mars_facts_df = pd.DataFrame(mars_facts[0])
    mars_html = mars_facts_df.to_html()
    mars_fact_table = {'facts_table':mars_html}
    db.latest_news.insert_one(mars_fact_table)
    
    return()



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
    for value in title:
        browser.click_link_by_partial_text(f'{title[x]}')
        html = browser.html
        soup = bs(html, 'html.parser')
        time.sleep(3)
        ur_addr = soup.find("a",target="_blank")["href"]
        image_url.append(ur_addr)
        browser.visit(url)
        time.sleep(5)
        x+=1
    
    x = 0
    for  i in title:
        hemisphere_image_urls = {'title': title[x], 'image_url': image_url[x]}
        db.hemisphere_img.insert_one(hemisphere_image_urls)
        x+=1

    return()



def scrape:
    new_news()
    featured_img()
    weather_tweet()
    mars_table()
    mars_dictio()
    return()




