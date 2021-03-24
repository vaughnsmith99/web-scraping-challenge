import pandas as pd
import time
from splinter import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Visit the url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Mars Latest News

    container = soup.find('div', {'class':'list_text'})
    title = container.find('a', {'target':'_self'}).text
    body = container.find('div', {'class':'article_teaser_body'}).text

    # Visit the url
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Mars image 
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars2.jpg'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    mars_img= soup.find_all('img')['src']

    browser.quit()

    #Read tables with pandas

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = pd.DataFrame(tables[0])
    df.columns = ['Measure','Value']
    df_html = df.to_html()

    valles = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif'
    cerberus = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif'
    schiaparelli = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif'
    syrtis = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif'

    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": f"{valles}"},
    {"title": "Cerberus Hemisphere", "img_url": f"{cerberus}"},
    {"title": "Schiaparelli Hemisphere", "img_url": f"{schiaparelli}"},
    {"title": "Syrtis Major Hemisphere", "img_url": f"{syrtis}"}
                            ]

    dict = {
        'title': f'{title}',
        'body' : f'{body}',
        'mars_img' : f'{mars_img}',
        'table' : f'{df_html}',
        'hemisphere_image_urls' : f'{hemisphere_image_urls}'
        }

    return dict