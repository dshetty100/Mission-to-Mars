
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

# Setting up the executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

#search for elements with a specific combination of tag (div) and attribute (list_text).
# Optional - telling our browser to wait one second before searching for components.
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Set up the html parser & look for the <div /> tag and its 
# descendent (the other tags within the <div /> element) with the class 
# of list_text. This is our parent element.
# when using select_one, the first matching element returned will be 
# a <li /> element with a class of slide and all nested elements within it.
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# Begin scraping. We’re looking for a <div /> with a class of “content_title.”
# The output should be the HTML containing the content title and anything else nested inside 
# of that <div />.
slide_elem.find('div', class_='content_title')

# Search within the parent element (<div /> tag) to find the first `a` tag and save it as `news_title`
# .get_text() will return only the text of the element. The code will 
# return only the title of the news article and not any of the HTML tags 
# or elements as in above output.
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title 

# Use the parent element to find the paragraph text
# scraping (searching) for the article summary instead of the title, so 
# we’ll need to use the unique class associated with the article summary.
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Now scrapping image from a different website, "https://spaceimages-mars.com/""

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1] # find an element by a tage named 'button'
full_image_elem.click()  # Splinter will "click" the image to view its full size


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
# tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Scraping a table (Mars data) from website 'https://galaxyfacts-mars.com/''

# scrape the entire table with Pandas' .read_html() function.
df = pd.read_html('https://galaxyfacts-mars.com')[0]  # creating a new DataFrame from the HTML table. specifying an index of 0, tells Pandas to pull only the first table it encounters
df.columns=['description', 'Mars', 'Earth'] # assign columns to the new DataFrame
df.set_index('description', inplace=True)  # turning the Description column into the DataFrame's index
df


# convert our DataFrame back into HTML-ready code
df.to_html()


# Now we have gathered everything. End the automated browsing session
browser.quit()




