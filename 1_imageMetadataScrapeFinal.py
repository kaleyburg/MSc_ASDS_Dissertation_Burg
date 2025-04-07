# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 14:05:30 2024

@author: kburg
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re
import os

#pip install pyperclip
import pyperclip


#skip the rest of this until start of things

#ignore --- 
new_directory = 'C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation'


os.chdir(new_directory)

download_directory = os.getcwd()

driver = webdriver.Chrome()

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)


#ignore --^



#this works below to find the list of constituencies


constituencytest = driver.find_elements(By.XPATH, "//span[contains(@class,'text-sm')]")
print(len(constituencytest))
constituencytest



#SAVE THIS
#getting vector of constituency names and parties and elections

# Find all constituency elements
constituency_elements = driver.find_elements(By.XPATH, '//span[@class="text-sm"]')
constituency_elements
# Extract text from these elements
constituency_names = [element.get_attribute("textContent") for element in constituency_elements]
constituency_names
# Print the constituency names
for name in constituency_names:
    print(name)

len(constituency_names)
# Print the constituency names

import numpy as np

vector = np.array(constituency_names)
len(vector)


# Remove the first 20 elements
vector_without_first_20 = vector[20:]

# Print the vector without the first 20 elements
print(vector_without_first_20)


# Remove the first 20 elements
vector2 = vector[20:-15]

# Print the vector without the first 20 elements
print(vector2)


constituencyNames = vector2
constituencyNames[0]


electionNames = vector[:12]

partyNames = vector[12:20]







#ignore for now dont need to run with this version of the code ---
def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
        print("Folder created successfully!")
    except FileExistsError:
        print("Folder already exists!")

folder_name = "my_folder"
create_folder(folder_name)

#ignore for now --- 

















###########################
############  green party 2010        ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2010green"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0


#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#0+1 represents 2010 election
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({0+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 2 for green party (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({2+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(3)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(0.5)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(1)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end



#GREEN DONE








###########################
############  labour party 2010     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2010labour"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0


#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#0+1 represents 2010 election
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({0+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 3 for labour party (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({3+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(3)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(0.5)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(1)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end






####LABOUR DONE


























###########################
############  liberal democrats party 2010     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2010libdems"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0


#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#0+1 represents 2010 election
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({0+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 4+1 for libdems (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({4+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(2)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(1)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end


















###########################
############  UK independence party 2010     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2010UKind"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0


#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#0+1 represents 2010 election
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({0+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 4+1 for libdems (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({7+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(3)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(0.5)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(1)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end






###########################
############  Conservative 2015     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2015conserv"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0


#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#3+1 represents 2015 (3)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({3+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 1+1 for conservs (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({1+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end














###########################
############  Labour 2015     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2015labour"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()





#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0





#selecting election



print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#3+1 represents 2015 (3)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({3+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 3+1 for labour (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({3+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end




####2015 LABOUR DONE














###########################
############  Lib Dems 2015     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2015libdems"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0




#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#3+1 represents 2015 (3)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({3+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        


#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 4+1 for libdems (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({4+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end











###########################
############  UK independence 2015     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2015UKind"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0




#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#3+1 represents 2015 (3)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({3+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        


#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 7+1 for uk indpendence (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({7+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end




















###########################
############  Conservative 2017     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2017conserv"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0




#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#6+1 represents 2017 (6)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({6+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 1+1 for conserv (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({1+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(295, len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end





###done







###########################
############  Green 2017     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2017green"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0


#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#6+1 represents 2017 (6)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({6+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 2+1 for green (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({2+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end














###########################
############  Labour 2017    ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2017labour"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()





#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0





#selecting election



print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#6+1 represents 2017 (6)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({6+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 3+1 for labour (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({3+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end











###########################
############  Lib Dems 2017     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2017libdems"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0




#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#6+1 represents 2017 (6)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({6+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        


#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 4+1 for libdems (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({4+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end











###########################
############  UK independence 2017     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2017UKind"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0




#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#6+1 represents 2017 (6)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({6+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        


#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 7+1 for uk indpendence (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({7+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end



















###########################
############  Conservative 2019     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2019conserv"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0




#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#7+1 represents 2019 (7)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({7+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 1+1 for conserv (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({1+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end











###########################
############  Green 2019     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2019green"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0


#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#7+1 represents 2019 (7)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({7+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 2+1 for green (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({2+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end














###########################
############  Labour 2019    ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2019labour"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()





#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0





#selecting election



print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#7+1 represents 2019 (7)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({7+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        
#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 3+1 for labour (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({3+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end











###########################
############  Lib Dems 2019     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2019libdems"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0




#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#7+1 represents 2019 (7)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({7+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        


#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 4+1 for libdems (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({4+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end











###########################
############  UK independence 2019     ###############
###########################






#start of things
#adjust this at the start


#directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/all_downloads"
directory = "C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation/2019UKind"

# Change the working directory
os.chdir(directory)

current_directory = os.getcwd()
print("Current working directory:", directory)



#works - before you start adjust the cwd above


#start of actual things running

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
    
    
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.openelections.co.uk/")
driver.set_window_size(1296, 688)

#country selection - keep the same
driver.execute_script("window.scrollTo(0, 0)")
#country selections
driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()
driver.find_element(By.NAME, "country").click()



#ignore for now
constituencyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='constituency']")
#print(len(constituencyResults))

electionResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='election']")
#print(len(electionResults))

partyResults = driver.find_elements(By.XPATH, "//input[contains(@class,'oe-checkbox') and contains(@type, 'checkbox') and @name='party']")
#print(len(partyResults))

electionList = (0, 3, 6, 7, 10, 11)
electionList

partyList = (1, 2, 3, 4, 7)
partyList


#ignore but scared to delete
totalImages = 0




#selecting election

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#7+1 represents 2019 (7)
checkbox_selector = f".js-leaflets-election > .mb-4:nth-child({7+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector).click()
time.sleep(1.5)
        

time.sleep(1.5)
        


#selecting party
       
print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
print('waiting')
time.sleep(1.5)

print('finding accordion to click')
driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .oe-accordion-title").click()
time.sleep(1.5)

print('scrolling to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

#changed the nth child to 7+1 for uk indpendence (adjust as necessary)
checkbox_selector2 = f".js-leaflets-party > .mb-4:nth-child({7+1}) .oe-checkbox"
print('back to top')
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(1.5)

print('finding checkbox')
driver.find_element(By.CSS_SELECTOR, checkbox_selector2).click()
time.sleep(1.5)
            
        
##
           
#loading all images
    
while True:
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for a short period to allow new content to load
        time.sleep(5)

        # Find the "Load More" button
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".js-leaflets-load-more")

        # If the button is visible and enabled, click it
        if load_more_button.is_displayed() and load_more_button.is_enabled():
            load_more_button.click()
            print("Clicked 'Load More'")
        else:
            print("No more content to load.")
            break  # Exit the loop if the button is not found or not clickable

    except NoSuchElementException:
        print("No 'Load More' button found. Exiting loop.")
        break  # Exit the loop if the button is not found

    except Exception as e:
        print("Error while scrolling and loading content:", e)
        break
    

print('loaded all')





##starting downlaods
           

print("Starting loop to click 'Download'")

driver.execute_script("window.scrollTo(0, 0)")
 

    # Initial click before looping
  #  self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > .oe-accordion-title").click()

    # Wait for the "country" element to be present
    #country_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "country")))
    #country_element.click()

time.sleep(1)

#check how many images to know how many to iterate over
    
imgResults = driver.find_elements(By.XPATH,"//li[contains(@class,'w-1/2 lg:w-1/3 px-3 mb-6')]")


#print how many there are
totalImages = totalImages + len(imgResults)
print(totalImages)

print(len(imgResults))
print(range(len(imgResults)))

#ignore this i think but too scared to delete
downloaded_files = set()


#loop to download
if len(imgResults) == 0:
    print('nothing to download')
else:
    #change the cwd before the code runs!
    download_directory = os.getcwd()
    prefs = {'download.default_directory': download_directory}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': download_directory})
    print(os.getcwd())
    for d in range(len(imgResults)):
        print(f"iteration {d}")
        # Scroll to the i-th image result

        
        element = driver.find_element(By.CSS_SELECTOR, f".w-1\\/2:nth-child({d+1}) .absolute")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
            
        # Click on the i-th image result
        imgResults[d].click()  
            
        time.sleep(2)
        
        # Wait for the "Download" link to be clickable and then click it
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link.click()
        
        time.sleep(1)
        
        text_filename = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
                # Sanitize the URL to make it a valid filename
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', download_link.get_attribute("href"))
        
        # Use the sanitized URL as the filename for the text file
        text_filename = sanitized_url + ".txt"
        print(text_filename)
        
        time.sleep(2)
        
        
        
        # Execute JavaScript to trigger Ctrl+A and Ctrl+C
        driver.execute_script("document.body.focus();document.execCommand('selectAll');")
        driver.execute_script("document.execCommand('copy');")
        
        # Get the copied text from the clipboard
        copied_text = driver.execute_script("return window.getSelection().toString();")
        
        # Save the copied text into a file named after the downloaded file
        with open(text_filename, "w") as file:
            file.write(copied_text)
        
        print(f"Text copied from the webpage has been saved into '{text_filename}.txt'")
               
        
        
        # Wait for the element with class "mt-6" to be clickable and then click it
        another_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mt-6")))
        another_element.click()
        
        # Adjust sleep duration or replace with proper waits as needed
        time.sleep(2)

 # Iterate over each image result
         # Iterate over each image result
            
#end












