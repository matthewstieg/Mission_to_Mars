    #!/usr/bin/env python
    # coding: utf-8

    # In[105]:


import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests as req
import re

from splinter import browser
from selenium import webdriver


    # In[ ]:

def init_browser():
    executable_path = {'executable_path' : 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)
    init_browser.quit()




    # In[109]:
def scrape_all():
    browser=init_browser()

    url= "https://mars.nasa.gov/news/" 
    response = req.get(url)
    soup = bs(response.text, 'html5lib')


    # In[126]:


    news_url = "https://mars.nasa.gov/news/"
    news_browser = webdriver.Chrome()
    news_browser.get(news_url)
    time.sleep(1)
    news_titles = news_browser.find_elements_by_tag_name('a')
    news_bodies = news_browser.find_elements_by_class_name('article_teaser_body')
    all_titles = []
    all_bodies = []
    for title in news_titles:
        all_titles.append(title.text)
    for body in news_bodies:
        all_bodies.append(body.text)



    news_browser.quit()


    # In[131]:


    news_title = all_titles[35]
    news_desc = all_bodies[0]

    print(news_title)
    print(news_desc)


    # In[92]:


    # MARS IMAGE CAPTURE
    # -----------------------------------------------------------------------------------------------------

    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    pre_featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(pre_featured_image_url)


    # In[93]:


    html = browser.html
    soup = bs(html, "html.parser")


    # In[94]:


    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(2)


    # In[95]:


    browser.click_link_by_partial_text('more info')


    # In[96]:


    fi_html = browser.html
    fi_soup = bs(fi_html, 'html.parser')
    fi_url = fi_soup.find('img', class_='main_image')
    url_part2 = fi_url.get('src')

    featured_image_link = "https://www.jpl.nasa.gov" + url_part2

    print(featured_image_link)
    browser.quit()


    # In[132]:


    # TWITTER
    # -----------------------------------------------------------------------------------------------------

    twitter_url = "https://twitter.com/marswxreport?lang=en"
    twitter_browser = webdriver.Chrome()


    # In[133]:


    twitter_browser.get(twitter_url)
    time.sleep(1)


    # In[134]:


    twitter_body = twitter_browser.find_element_by_tag_name('body')


    # In[135]:


    # Get list of all weather reports

    tweets = twitter_browser.find_elements_by_class_name('tweet-text')
    mars_weathers = []
    for tweet in tweets:
        mars_weathers.append(tweet.text)
        print(tweet.text)
    twitter_browser.quit()


    # In[136]:


    # Select first/most recent weather report

    current_mars_weather = mars_weathers[0]
    current_mars_weather


    # In[97]:


    # MARS FACTS
    # -----------------------------------------------------------------------------------------------------

    # Pull mars facts table into a DF

    mars_table_url = "https://space-facts.com/mars/"
    mars_tables = pd.read_html(mars_table_url)

    mars_df = mars_tables[0]
    mars_df.columns = ['0', '1']
    mars_df = mars_df.iloc[0:]

    print(mars_df)


    # In[98]:


    # Convert DF to html code
    table_object = mars_df.to_html(classes="table table-striped")
    table_object = table_object.replace('\n', '')
    table_object


    # In[53]:


    # MARS IMAGES LIST FROM USGS
    # -----------------------------------------------------------------------------------------------------



    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_request = req.get(usgs_url)


    # In[54]:


    usgs_soup = bs(usgs_request.text, "html.parser")
    hemisphere_list = usgs_soup.find_all('a', class_='itemLink product-item')


    # In[67]:


    # Link Setup

    hemi_link_1 = hemisphere_list[0]['href']
    hemi_link_2 = hemisphere_list[1]['href']
    hemi_link_3 = hemisphere_list[2]['href']
    hemi_link_4 = hemisphere_list[3]['href']

    print(hemi_link_1)
    print(hemi_link_2)
    print(hemi_link_3)
    print(hemi_link_4)


    # In[73]:



    hemi_base_url = 'https://astrogeology.usgs.gov'
    cerberus_url = hemi_base_url + hemi_link_1
    schiaparelli_url = hemi_base_url + hemi_link_2
    syrtis_url = hemi_base_url + hemi_link_3
    valles_url = hemi_base_url + hemi_link_4
    urls = [cerberus_url, schiaparelli_url, syrtis_url, valles_url]

    print(urls[3])


    # In[102]:


    images = []
    headers = []
    for url in urls:
        img_req = req.get(url)
        img_soup = bs(img_req.text, "html.parser")
        img_item = img_soup.find('img', class_='wide-image')
        images.append(hemi_base_url+img_item['src'])
        title = img_soup.find('h2', class_='title')
        headers.append(title.text)

    print(images)



    # In[104]:


    hemisphere_image_urls = [{'title':headers[0], 'img_url': images[0]},
                        {'title':headers[1], 'img_url': images[1]},
                        {'title':headers[2], 'img_url': images[2]},
                        {'title':headers[3], 'img_url': images[3]},
                       ]
    print(hemisphere_image_urls)


    # In[ ]:


    mars_data_dict = {"News_Title": news_title,
                     "News_Description": news_desc,
                     "Featured_Image": featured_image_link,
                     "Mars_Weather": current_mars_weather,
                     "Mars_Facts": table_object,
                      "Hemispheres" : hemisphere_image_urls
                     }


    return mars_data_dict



    # In[ ]:





    # In[ ]:





    # In[ ]:




