# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-toolsai.jupyter added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '../../../../../../../var/folders/6c/12zttfmj58d_3_yqjbdtcn6h0000gn/T/2e692a61-87d4-447a-b9ac-c66588833d84'))
	print(os.getcwd())
except:
	pass
# %%

def scrape():
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import requests
    from splinter import Browser
    from webdriver_manager.chrome import ChromeDriverManager
    import pymongo
    #scrape news
    url = 'https://mars.nasa.gov/news'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')


    
    title_results = soup.find('div', class_="content_title")
    news_title = title_results.get_text(strip=True)

    para_results = soup.find('div', class_="rollover_description_inner")
    news_p = para_results.get_text(strip=True)


    #scrape for image

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    browser.find_by_css('div[class="NavDesktopDropdown -active"]')[0].click()
    browser.click_link_by_partial_text('Featured Image')

    html = browser.html
    soup = bs(html, 'html.parser')
    main = soup.find('main')
    img = main.find('img')
    featured_image_url = img['src']




    


    #scrape for facts
    url = 'https://space-facts.com/mars/'
    mars_data_table = pd.read_html(url, header=None)
    mars_data_table = mars_data_table[0]
    mars_data_table = mars_data_table.rename(columns={0:'Description',1: 'Mars'})
    mars_data_html = mars_data_table.to_html()

    # scrape hemi-info
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    url_list = []
    hemi_list = []

    items = soup.find_all('div', class_='description')

    for item in items:
        a = item.find('a', class_='itemLink')
        hemi = a.text.strip()
        hemi_list.append(hemi)
        url = item.find('a')['href']
        url_list.append(url)


    hemi_list = [i.split(' Enhanced',1)[0] for i in hemi_list]

    orignial_img_list = []

    for url in url_list:
        browser.visit(f"https://astrogeology.usgs.gov/{url}")
        html = browser.html
        soup = bs(html, 'html.parser')
        downloads = soup.find_all('li')
        temp_list = []
        for download in downloads:
            orignial_img = download.find('a')['href']
            temp_list.append(orignial_img)
        
        orignial_img_list.append(temp_list[1]) 

    hemisphere_image_urls = []

    browser.quit()

    for i in range(0,4,1):
        temp_dict = {'title': hemi_list[i], 'img_url': orignial_img_list[i]}
        hemisphere_image_urls.append(temp_dict)

    #put all results in list of dict
    mars_dict = [
        {'Recent_News':news_title, 'News_Story':news_p }, 
        {'Featured_Image':featured_image_url}, 
        {'Mars_Data': mars_data_html}, 
        {'Mars_Hemispheres': hemisphere_image_urls}
    ]
    
    
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    db = client.mars_db 
    mars_collection = db.mars_collection

    mars_collection.insert_many(
        mars_dict
    )

    print('Mars Data Uploaded')



# %%
