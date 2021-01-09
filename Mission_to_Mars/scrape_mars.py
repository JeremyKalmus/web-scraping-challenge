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

    footer = soup.find('footer')
    for a  in footer.find_all('a'):
        featured_image = a['data-fancybox-href']
        featured_image_url = f'https://www.jpl.nasa.gov/{featured_image}'
    browser.quit()


    #scrape for facts
    url = 'https://space-facts.com/mars/'
    mars_data_table = pd.read_html(url, header=0)
    mars_data_table = mars_data_table[0]
    mars_data_html = mars_data_table.to_html()

    # scrape hemi-info
    hemi_list = ['Cerberus', 'Schiaparelli', 'Syrtis_Major', 'Valles_Marineris']
    hemi = 'Cerberus'
    hemisphere_image_urls = []

    for hemi in hemi_list:
        hemi_url = f'https://astrogeology.usgs.gov/search/map/Mars/Viking/{hemi}_enhanced'
        response = requests.get(hemi_url)
        soup = bs(response.text, 'html.parser')

        downloads = soup.find('div', class_="downloads" )
        images_list = downloads.find_all('li')[1]
        for a in images_list.find_all('a'):
            img_url = a['href']
            title = f'{hemi} Hemisphere'
            title = title.replace('_', ' ')
            image_dict = {'title': title, 'img_url':img_url}
        hemisphere_image_urls.append(image_dict)    


    #put all results in dict
    mars_dict = {
        {'Recent News':news_title, 'News Story':news_p }, 
        {'Featured Image':featured_image_url}, 
        {'Mars Data': mars_data_html}, 
        {'Mars Hemisphers': hemisphere_image_urls}
    }
    return mars_dict


# %%
