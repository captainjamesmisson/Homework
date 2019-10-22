from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import requests
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# Initiate browser driver

mars_results={}

def init_browser():
    return webdriver.Chrome("C:\\Users\\brand\\Downloads\\chromedriver_win32\\chromedriver")

# Define Nasa news scrape function

def scrape_nasa_news():
    browser = init_browser()

    nasa_news_url = "https://mars.nasa.gov/news/"
    browser.get(nasa_news_url)
    time.sleep(1)
    html = browser.page_source
    soup = bs(html, "lxml")

    news_title = soup.find('div',class_='content_title').text.strip()
    news_p = soup.find('div', class_='article_teaser_body').text.strip()

    print(news_title)
    print(news_p)

    # nasa_news_data = {'title':news_title,'teaser':news_title}
    
    mars_results['news_title']=news_title
    mars_results['news_p']=news_p


    browser.close()

    return mars_results

# Define Nasa image scrape function
def scrape_nasa_image():

    browser = init_browser()

    nasa_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.get(nasa_image_url)
    browser.find_element_by_css_selector("#full_image").click()
    time.sleep(1)
    html = browser.page_source
    soup = bs(html, "lxml")

    image = soup.find_all('a',class_="fancybox")[1]
    image_url = image['data-fancybox-href']
    image_url

    home_url = 'https://www.jpl.nasa.gov'
    featured_image_url = home_url + image_url
    featured_image_url

    # nasa_image_data = {'image':image_url}

    mars_results['featured_image_url']=featured_image_url

    browser.close()

    return mars_results

# Define Mars Twitter page scrape function

def scrape_mars_twitter():

    browser = init_browser()

    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.get(mars_twitter_url)
    time.sleep(1)
    html = browser.page_source
    soup = bs(html, "lxml")

    mars_weather = soup.find('div',class_="js-tweet-text-container").find('p').text.strip()
    mars_weather

    # mars_weather_data = {'weather':mars_weather}

    mars_results['mars_weather']=mars_weather

    browser.close()
    
    return mars_results

# Define Mars facts scrape function:

def scrape_mars_facts():

    browser = init_browser()

    mars_facts_url = "https://space-facts.com/mars/"
    browser.get(mars_facts_url)
    time.sleep(1)
    html = browser.page_source
    # soup = bs(html, "lxml")

    table = pd.read_html(html)
    mars_earth_df = table[0]
    mars_df = mars_earth_df.drop(columns=['Earth'])
    mars_df.columns=['Item','Value']
    mars_df.set_index('Item',inplace=True)
    mars_table = mars_df.to_html()

    mars_results['mars_table']=mars_table
    
    browser.close()

    return mars_results

# Define Mars hemisphere scrape function

def scrape_mars_hemisphere():

    browser = init_browser()

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.get(hemisphere_url)

    html = browser.page_source
    soup = bs(html, "lxml")

    hemispheres = soup.find_all('div',class_="description")

    url_list=[]

    for hemisphere in hemispheres:
        one_of_four = hemisphere.find('a')['href']
        url_list.append(one_of_four)

    hemisphere_url_list = ['http://astrogeology.usgs.gov' + url for url in url_list]
    hemisphere_url_list

    image_title_list = []
    image_src_list = []

    for hemisphere_url in hemisphere_url_list:
        browser.get(hemisphere_url)
        time.sleep(2)
        html = browser.page_source
        soup = bs(html, "lxml")
        image_title = soup.find('h2',class_="title").text.strip('Enhanced')
        image_title_list.append(image_title)
        image_src = soup.find('img',class_="wide-image")['src']
        image_src_list.append(image_src)
    
    image_url_list = ['http://astrogeology.usgs.gov' + src for src in image_src_list]

    hemisphere_zip = zip(image_title_list, image_url_list)
    hemisphere_list = list(hemisphere_zip)

    hemisphere_dict =[]

    for i in range(len(hemisphere_list)):               
        print(f'iteration {i} contains {hemisphere_list[i]}')
        hemisphere_dict.append({'title': hemisphere_list[i][0], 'image_url':hemisphere_list[i][1]})

    hemisphere_data = hemisphere_dict

    mars_results['hemisphere_dict']=hemisphere_data

    browser.close()

    return mars_results
