import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser

def scrape():
    mars_info={}
    url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_="slide")
    for result in results:
        try:
            news_title = result.find(class_="content_title").text
            news_p = result.find(class_="rollover_description_inner").text

            if (news_title and news_p):
                print('-------------')
                print(news_title)
                print(news_p)
        except AttributeError as e:
            print(e)
        mars_info['news_title']=news_title
        mars_info['news_p']=news_p

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html = browser.html
    soup2 = bs(html, 'html.parser')
    images = soup2.find_all('a', class_="fancybox")
    image_url=[]
    for image in images:
        link=image['data-fancybox-href']
        image_url.append(link)
    complete_link='https://www.jpl.nasa.gov' + link
    browser.quit()
    mars_info['Space_Image_Link']=complete_link

    url3='https://twitter.com/marswxreport?lang=en'
    response3 = requests.get(url3)
    soup3 = bs(response3.text, 'html.parser')
    results3 = soup3.find("div", class_="js-tweet-text-container")
    mars_weather=results3.find("p", class_="tweet-text").text
    mars_info['Weather_Info']=mars_weather


    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    df=tables[0]
    df.columns = ['Name', 'Value']
    df.set_index('Name', inplace=True)
    df_new=df.to_html()
    df_new.replace('\n', '')
    mars_info['Mars_Fact']=df_new

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    html = browser.html
    soup5 = bs(html, 'html.parser')
    results5 = soup5.find_all('h3')
    hemisphere_image_urls=[]
    dict={}
    for result in results5:
        browser.click_link_by_partial_text(result.text)
        html51 = browser.html
        soup51 = bs(html51, 'html.parser')
        results51 = soup51.find_all('div', class_='downloads')
        link=results51[0].find('a')['href']
        dict['title']=result.text
        dict['img_url']=link
        hemisphere_image_urls.append(dict)
        dict={}
        browser.back()
    browser.quit()
    mars_info['Hemisphere_Info']=hemisphere_image_urls

    return mars_info