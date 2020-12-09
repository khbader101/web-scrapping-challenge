# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)



def scrape():
    browser = init_browser
    mars_data = {}
    # Nasa Mars News
        # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    news_soup = bs(html, 'html.parser')

    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text
    print(news_title)
    print(news_p)


    # JPL Mars
    base_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(base_url)
    time.sleep(5)

    html = browser.html
    soup = bs(html,"html.parser")
    print(soup.prettify())
    #image
    featured_image  = soup.find('article', class_="carousel_item")['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + featured_image
    print(f"featured_image_url: {featured_image_url}")


    # Mars Facts
    base_url2 = "https://space-facts.com/mars/"
    browser.visit(base_url2)
    time.sleep(5)

    facts = pd.read_html(base_url2)
    facts_df = facts[0]
    print("Mars Planet Facts")
    facts_df

    mars_facts = facts_df.rename(columns={0 : "Features", 1 : "Value"}).set_index(["Features"])
    mars_facts
    mars_table = mars_facts.to_html()


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

    hemisphere_imgs_urls

    mars_data = {
        "ne"
    }

    browser.quit()
