
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

   # scaape Mars news 
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
   
   # Add try/except for error handling
   try:
      slide_elem = news_soup.select_one('div.list_text')

      # Begin scraping. We’re looking for a <div /> with a class of “content_title.”
      # Use the parent element to find the first <a> tag and save it as `news_title`
      news_title = slide_elem.find('div', class_='content_title').get_text()

      # Use the parent element to find the paragraph text
      # scraping (searching) for the article summary instead of the title, so 
      # we’ll need to use the unique class associated with the article summary.
      news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
  
   except AttributeError:
       return None, None

   return news_title, news_p


# ### Now scrapping image from a different website, "https://spaceimages-mars.com/""

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1] # find an element by a tage named 'button'
    full_image_elem.click()  # Splinter will "click" the image to view its full size


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
       # Find the relative image url
       # tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image
       img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ### Scraping a table (Mars data) from website 'https://galaxyfacts-mars.com/''

def mars_facts():
    # Add try/except for error handling
    try:
       # scrape the entire table with Pandas' .read_html() function.
       df = pd.read_html('https://galaxyfacts-mars.com')[0]  # creating a new DataFrame from the HTML table. specifying an index of 0, tells Pandas to pull only the first table it encounters
    
    except BaseException:
        return None


    df.columns=['Description', 'Mars', 'Earth'] # assign columns to the new DataFrame
    df.set_index('Description', inplace=True)  # turning the Description column into the DataFrame's index

    # convert our DataFrame back into HTML-ready code. add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())




