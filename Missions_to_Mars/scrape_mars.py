# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager



def scrape():
    mars_data = {}

    # Nasa Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    news_soup = bs(html, 'html.parser')

    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_paragraph = news_soup.find_all('div', class_='article_teaser_body')[0].text


    # JPL Mars
    base_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(base_url)
    time.sleep(5)

    html = browser.html
    soup = bs(html,"html.parser")


    #image
    featured_image  = soup.find('article', class_="carousel_item")['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + featured_image


    # Mars Facts
    mars_dict = {}
    
    mars_facts_url = 'https://space-facts.com/mars/'
    mft = pd.read_html(mars_facts_url)
    mars_table = mft[0].set_index(0)[1].to_dict()
    
    mars_dict['mars_facts'] = mars_table

    # Mars Hemisphere
    base_url3= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(base_url3)
    time.sleep(5)

    html3 = browser.html
    soup = bs(html3, 'html.parser')

    info = soup.find('div', class_='collapsible results')
    print(info.prettify())
    hemispheres=info.find_all('a')
    hemisphere_imgs_urls = []

    for hemisphere in hemispheres:
        if hemisphere.h3:
            title=hemisphere.h3.text
            link=hemisphere["href"]
            main_url="https://astrogeology.usgs.gov/"
            next_url=main_url+link
            browser.visit(next_url)
            time.sleep(5)
            html = browser.html
            soup = bs(html, 'html.parser')
            hemisphere2=soup.find("div",class_= "downloads")
            img=hemisphere2.ul.a["href"]
            hemisphere_dict={}
            hemisphere_dict["Title"]=title
            hemisphere_dict["Image_URL"]=img
            hemisphere_imgs_urls.append(hemisphere_dict)
            browser.back()

    browser.quit()

    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "mars_facts": mars_table,
        "hemisphere_imgs_urls": hemisphere_imgs_urls,
        "hemisphere_dict": hemisphere_dict
    }

    return mars_data
