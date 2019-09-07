#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars
# 
# A webscraping assignment.  We will be gathering data from differnet websites using Beautiful Soup, Splinter, and Pandas. 
# 
# ### Import Libraries

# In[1]:


from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd
import numpy as np





# ### First site:  https://mars.nasa.gov/news/
# 
# We're going to be gathering the headlines and teaser paragraph from the first page of the news page. <br>
# We are going to append the headlines and articles to a list so they can be used later on in the assignment. <br>
# We are also going to be printing out the list to display.  

# In[3]:


url ='https://mars.nasa.gov/news/'


# #### Spinter will open up Chrome and go to the site
# 

# In[4]:


browser.visit(url)


# #### Empty lists are created here

# In[5]:


news_title=[]
news_p=[]


# #### We parse through the site:
# 
# Look for the div tag with the class:  image_and_description_container<br>
# <br>    
# Then loop through the articles and print them while at the same time store the articles and headlines into the lists. <br>

# In[6]:


# HTML object
html = browser.html
# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')
# Retrieve all elements that contain book information
articles = soup.find_all('div', class_='image_and_description_container')
time.sleep(5)



try:
    for article in articles:
            
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        h3 = article.find('h3').text
        teaser = article.find('div',class_="article_teaser_body").text
        news_title.append(h3)
        news_p.append(teaser)
        print("\n")
        print('-----------')
        print(h3)
        print("\n")
        print(teaser)


        
except:
    print("\nScraping Complete")


# ### Second site:  https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
# 
# We want to get the URL for the current featured picture in the highest resolution. <br>
# We will look for the <article> tag and the class:  carousel_item  and also narrow it even futher with style. <br>
# This will return a partial address with extra bits of information. <br>
#     The truncate the results by stripping off:  "background-image: url('  and  ');    from the results<br>
# We then append the results to the address:  jpl.nasa.gov
# <br>

# In[7]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


# In[8]:


browser.visit(url)


# In[9]:


html = browser.html
# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')

big_picture = soup.find("article", class_="carousel_item")['style']
big_picture = big_picture.replace('background-image: url(', '').replace(');', '')
big_picture = big_picture.replace("'","").replace("'","")
featured_url = "https://jpl.nasa.gov" + big_picture
featured_url



# ### Third site: https://twitter.com/marswxreport?lang=en
# 
# We want to get the latest mars weather tweet from mars.  <br>
# We use the .get_text function to filter for the ones with "Insight sol" in it. <br>
# We use [1] to pick the second to the second newest twitter post because that is the latest weather report <br>

# In[10]:


url = 'https://twitter.com/marswxreport?lang=en'


# In[11]:


browser.visit(url)


# In[12]:


html = browser.html
# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')


# In[13]:


mars_weather = soup.find_all("p", class_="tweet-text")[1].get_text("InSight sol")


# In[14]:


mars_weather


# ### Fourth site: https://space-facts.com/mars/
# 
# We get extract the Mars facts from the page using Pandas <br>
# We then convert the table to a Pandas Datafram and then convert it to HTML format.  <br>

# In[15]:


res = requests.get("https://space-facts.com/mars/")
soup = bs(res.content,'lxml')
table = soup.find_all('table')[1] 
mars_facts = pd.read_html(str(table))
mars_facts_df = pd.DataFrame(mars_facts[0])
mars_facts_df 


# In[16]:


mars_facts_df.to_html()


# ### Fifth site: https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
# 
# We get it to click on the 4 hemispheres, grab the URL for the original high resolution and store them into a dictionary.  

# In[24]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# In[25]:


browser.visit(url)


# #### Scrape the Products page
# 
# We first scrape the div class collapsible.  This will put it into a list of 1 long string.  I chose to put into a list because it makes it easier to clean out the h3 tags afterwards.  

# In[70]:


html = browser.html
# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')



products = soup.find_all('div',class_='collapsible')
time.sleep(5)
print(products)
for link in products:
    name = link.find_all('h3')


# #### Clean out the h3 tags from the list. 
# 
# Now by running the .text on the list, it strips off the h3 tags.  Now the list can be iterated through while splinter clicks on the partial links and grab the picture URLs.  

# In[76]:


title = []
x = 0
for value in name:
    title.append(name[x].text)
    x+=1

print(title)


# #### Browse the site and get the URLs for the photos. 
# 
# I used the title list and used it to make spliter do a click partial text so that soup can retireve the address to the high res jpegs.  These URLs are then stored in image_url.  

# In[77]:



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


# In[78]:


print(image_url)


# #### Import into a list of dictionaries. 
# 
# Now we take the two lists and put them into the dictionary, "hemisphere_image_url"
# 
# The list comprehension reads, "For i in the range of the length of the title list, 'title': is title[i] and 'image_url' : is image_url[i]." 

# In[80]:


hemisphere_image_urls = [ {'title': title[i], 'image_url': image_url[i] } for i in range(len(title)) ]
hemisphere_image_urls


# In[ ]:





# In[ ]:




