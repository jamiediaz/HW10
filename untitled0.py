# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 21:10:19 2019

@author: jamie
"""


def newNews():
    url ='https://mars.nasa.gov/news/'
    browser.visit(url)
    latest_title = []
    html = browser.html
    soup = bs(html, 'html.parser')
    articles = soup.find_all('div', class_='image_and_description_container')
    time.sleep(5)
    try:
        for article in articles:
                
            # Use Beautiful Soup's find() method to navigate and retrieve attributes
            h3 = article.find('h3').text
            teaser = article.find('div',class_="article_teaser_body").text
            latest_title = [h3,teaser]
            
    except:
        print("\nScraping Complete")

    return(latest_title)


newNews