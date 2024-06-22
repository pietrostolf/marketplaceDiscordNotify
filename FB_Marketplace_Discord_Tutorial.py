#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import Dependencies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import numpy as np
import os

# In[3]:


# # Configure Chrome WebDriver options for headless mode
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")  # Necessary for headless mode on Windows

# # Initialize Chrome WebDriver
# browser = webdriver.Chrome(options=chrome_options)


# # In[4]:


# # Set up search parameters
# min_price = 200
# max_price = 500
# days_listed = 1
# query = "iPhone 13"
# city = "toronto"


# # In[5]:


# # Set up base url
# url = f'https://www.facebook.com/marketplace/{city}/search?query={query}&minPrice={min_price}&maxPrice={max_price}&daysSinceListed={days_listed}&exact=false'

# # Visit the website
# browser.get(url)


# # In[6]:


# #Close login popup
# try:
#     # Wait for up to 8 seconds for the close button to appear
#     close_button = WebDriverWait(browser, 8).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Close"]'))
#     )

#     # Click on the element once it's found
#     close_button.click()
# except:
#     pass


# # In[7]:


# #Scroll down to get all the available results
# try:
#     # Get the initial scroll position
#     last_height = browser.execute_script("return document.body.scrollHeight")

#     while True:
#         # Scroll down to the bottom of the page using JavaScript
#         browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # Adjust sleep time as needed

#         # Get the new scroll position
#         new_height = browser.execute_script("return document.body.scrollHeight")

#         # Check if we've reached the bottom
#         if new_height == last_height:
#             break

#         # Update the scroll position
#         last_height = new_height

# except Exception as e:
#     print(f"An error occurred: {e}")


# # In[8]:


# #Retrieve the HTML
# html = browser.page_source

# #Close the browser
# browser.close()

# # Parse the retrieved HTML content using BeautifulSoup
# soup = BeautifulSoup(html, 'html.parser')


# # In[ ]:


# # Create empty lists to store the desired information
# titles_list = []
# prices_list = []
# urls_list = []

# # Extract title information
# titles_div = soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
# titles_list.extend([title.text.strip() for title in titles_div])

# # Extract price information
# prices_div = soup.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
# prices_list.extend([price.text.strip() for price in prices_div])

# # Extract URL information
# urls_div = soup.find_all('a', href=lambda href: href and href.startswith('/marketplace/item/'))

# # Create a list of complete URLs
# urls_list = ['https://www.facebook.com' + url['href'] for url in urls_div]


# # In[10]:


# # Create empty lists to store the desired information
# titles_list = []
# prices_list = []
# urls_list = []

# # Find all <span> elements with the specified class that contain the titles
# titles_div = soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
# # Extract the text from each <span> element, strip any surrounding whitespace, and add to the titles_list
# titles_list.extend([title.text.strip() for title in titles_div])

# # Find all <span> elements with the specified class that contain the prices
# prices_div = soup.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
# # Extract the text from each <span> element, strip any surrounding whitespace, and add to the prices_list
# prices_list.extend([price.text.strip() for price in prices_div])

# # Find all <a> elements whose href attribute starts with '/marketplace/item/'
# urls_div = soup.find_all('a', href=lambda href: href and href.startswith('/marketplace/item/'))
# # For each <a> element, concatenate the base URL with the href attribute and add to the urls_list
# urls_list = ['https://www.facebook.com' + url['href'] for url in urls_div]


# # In[14]:


# # Create an empty list to store the item dictionaries
# items_list = []

# # Iterate over the titles, prices, and URLs simultaneously
# for title, price, url in zip(titles_list, prices_list, urls_list):
#     # Create an empty dictionary for the current item
#     item_dict = {}
#     # Add the title, price, and URL to the dictionary
#     item_dict["title"] = title
#     item_dict["price"] = price
#     item_dict["url"] = url
#     # Append the dictionary to the items_list
#     items_list.append(item_dict)


# # In[16]:


# items_df = pd.DataFrame(items_list)


# # In[18]:


# # # Extract numbers from the "Price" column using regular expressions
# # items_df['price'] = items_df['price'].apply(lambda x: re.sub(r'\D', '', x))

# # # Replace empty strings with NaN
# # items_df['price'].replace('', np.nan, inplace=True)

# # # Convert the "Price" column from object to float
# # items_df['price'] = items_df['price'].astype(float)


# # In[20]:


# # List of terms that must be present in the titles
# must_have_terms = [
#     "13",
#     "iPhone"
# ]

# # List of terms that must not be present in the titles
# forbidden_terms = [
#     "mini",
#     "iphone 7",
#     "iphone 8",
#     "iphone x",
#     "iphone xs",
#     "iphone 11",
#     "iphone 12",
#     "iphone 14",
#     "iphone 15",
#     "locked",
#     "blacklisted",
#     "screen"
# ]

# # Initialize the condition with True so that it can be combined using &= later
# condition = True

# # Generate the conditions dynamically based on must_have_terms and forbidden_terms
# # Check that each title contains all the must-have terms
# for term in must_have_terms:
#     condition &= items_df['title'].str.contains(term, case=False, regex=True)

# # Check that each title does not contain any of the forbidden terms
# for term in forbidden_terms:
#     condition &= ~items_df['title'].str.contains(term, case=False, regex=True)

# # Filter the DataFrame based on the generated condition
# filtered_df = items_df[condition]

# # Reset the index of the filtered DataFrame for a clean DataFrame
# filtered_df = filtered_df.reset_index(drop=True)


# # In[22]:


# # # Sort the DataFrame by the "price" column in ascending order
# # sorted_df = filtered_df.sort_values(by='price')

# # # Get the 10 cheapest entries
# # cheapest_10 = sorted_df.head(10)


# # In[23]:


# cheapest_10


# In[24]:


# Prepare the message with the price, title, and URL of the 10 cheapest items
# message = ""
# Iterate over each row in the DataFrame containing the 10 cheapest items
# for index, row in cheapest_10.iterrows():
    # Append the title, price, and URL of each item to the message string
    # message += f"Title: {row['title']}\nPrice: ${row['price']}\nURL: {row['url']}\n\n"

# message = "hi"

# # URL of the Discord channel where the message will be posted
# discord_url = 'https://discord.com/api/v9/channels/1222322624890146856/messages'

# # Payload containing the message to be sent
# payload = {"content": message}

# # Get the Discord API authorization token from the environment variable
# # discord_token = os.getenv('DISCORD_API_TOKEN')
# headers = {"Authorization": "TIyMjMyMDMxNzYwNzg0MTkyNA.G0PtCx.zElU2UN8BI69zrGMxbuWs8diAOqejzFDa3tZV4"}

# # Send a POST request to the Discord API with the payload and headers
# response = requests.post(discord_url, payload, headers=headers)

# Retrieve the Discord API token from the environment variable
discord_token = os.getenv('DISCORD_API_TOKEN')

if not discord_token:
    raise ValueError("DISCORD_API_TOKEN environment variable is not set")

# Prepare the message with the price, title, and URL of the 10 cheapest items
message = "hi"
print(message)
# # Iterate over each row in the DataFrame containing the 10 cheapest items
# for index, row in cheapest_10.iterrows():
#     # Append the title, price, and URL of each item to the message string
#     message += f"Title: {row['title']}\nPrice: ${row['price']}\nURL: {row['url']}\n\n"

# URL of the Discord channel where the message will be posted
discord_url = 'https://discord.com/api/v9/channels/1222322624890146856/messages'

# Payload containing the message to be sent
payload = {"content": message}

# Headers including the authorization token for the Discord API
headers = {"Authorization" : discord_token}

# Send a POST request to the Discord API with the payload and headers
response = requests.post(discord_url, payload, headers=headers)

