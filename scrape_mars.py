import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriver, ChromeDriverManager


def scrape():
    # Scrape News Article
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    mars_news_url = "https://redplanetscience.com/"
    browser.visit(mars_news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    news = soup.find('div', id='news')
    news_title = news.find('div', class_='content_title').text
    news_p = news.find('div', class_='article_teaser_body').text

    # Scrape Image of the day
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    html = browser.html
    soup = bs(html, "html.parser")
    img_url = jpl_url + soup.find('a', class_="showimg")["href"]

    # Scrape Mars Facts table
    mars_facts_url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(mars_facts_url)
    mars_facts_df = tables[0]
    mars_facts_df.columns=["Description", "Mars", "Earth"]
    mars_facts_df.set_index("Description", inplace=True)
    mars_facts_html = mars_facts_df.to_html(classes="table table-striped")

    # Scrape hemisphere picture URLS and Titles
    mars_hemisphere_url = "https://marshemispheres.com/"
    browser.visit(mars_hemisphere_url)
    html = browser.html
    soup = bs(html, "html.parser")
    hemispheres = soup.find_all('div', class_='item')
    hemisphere_url_list = []
    for hemisphere in hemispheres:
        hemisphere_url = hemisphere.find('a')['href']
        hemisphere_url_list.append(mars_hemisphere_url+hemisphere_url)
    hemisphere_img_urls = []
    for hemisphere in hemisphere_url_list:
        browser.visit(hemisphere)
        html = browser.html
        soup = bs(html, "html.parser")
        title = soup.find('h2').text.strip()
        url = browser.links.find_by_text('Sample')['href']
        hemisphere_img_urls.append({"title": title, "img_url": url})

    scrape_dict = {"news_title":news_title, "news_p":news_p, "img_url":img_url, "hemisphere_img_urls":hemisphere_img_urls, "mars_facts_html":mars_facts_html}
    browser.quit

    return(scrape_dict)