from selenium import webdriver
import time
import os
import pyautogui
from selenium.webdriver.common.keys import Keys
pyautogui.FAILSAFE = False
from fake_useragent import UserAgent
import random
import re
import pickle
# These are some global sleep variables, for each of the expected sleep times
# May need to be changed depending how fast or slow a persons computer is
# For now we will pick some conservative times, so things should work out of the box

# For tabbing, arrow keys, and interacting with a single webpage
shortSleep = 0.5

# For all other loading, including file uploads, page refreshes or reloads, etc.
longSleep = 5

# Other hardcoded variables
postalCode = " Brampton, ON, Canada"
phone = "416 805 6144"
address="Mississauga, ON"



# This will get the username and password from a text file
# Supports multiple logins, line separated
# Returns list of username,password
def getCredentials():

    # Open/read the file
    file = open("login.txt")
    file = file.read().splitlines()

    # Create list of usernames/passwords
    creds = []
    for credentials in file:
        credentials = credentials.split(", ")
        creds.append([credentials[0], credentials[1]])
    return creds


# This will retrieve the relevant info for the ad posting directory
# Returns title, price, description
def getAdInformation(directory):

    title, category,key, description = open("ads\\"+directory+"\\Ad.txt").read().split("\n", 3)
    return title, category,key, description


# This will return the absolute path to all images based on the directory
# Returns a list of absolute paths to images
def getAdImagePaths(directory):
    ads = os.getcwd() + "\\ads\\" + directory
    files = os.listdir(ads)

    # We will go through this list and remove the hidden files as well as Ad.txt
    # This will assume all remaining files are images so make sure they are!
    # Otherwise bad things might happen
    images = []
    for file in files:
        if file[0] != "." and file != "Ad.txt":
            images.append(ads + "\\" + file)
    return images


# This retrieves the directory name of each ad
# Returns list of ad folder names
def getAds():
    ads = os.getcwd() + "\\ads\\"
    ads = os.listdir(ads)
    return ads

# Initialize the browser, logging in with the given user/pass
# Returns browser object
def login(creds):

    # Init the browser, in this case firefox
    ua=["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78) Gecko/20100101 Firefox/78","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79) Gecko/20100101 Firefox/79","Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77) Gecko/20100101 Firefox/77","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75) Gecko/20100101 Firefox/75"]
    
    
    profile = webdriver.FirefoxProfile()
    
 
    
    profile.set_preference("general.useragent.override",ua[random.randint(0,3)] )
    profile.set_preference("dom.webdriver.enabled", False)
    browser = webdriver.Firefox(profile, executable_path='geckodriver')  # (executable_path='geckodriver')

    # Install adblocking extension
    #browser.install_addon(os.getcwd()+"\\uBlock0@raymondhill.net.xpi", temporary=True)

    # Take us to kijiji and maximize the window
    # So, maybe only halfscreening the window is better for testing, then we can see the terminal output in real time
    browser.maximize_window()
    time.sleep(longSleep)
    browser.get('https://www.kijiji.ca')
    
    
    cookies = pickle.load(open("cookies1.pkl", "rb"))
    for cookie in cookies:
      browser.add_cookie(cookie)
    '''
    time.sleep(random.randint(3,4))
    #browser.find_element_by_class_name('link-2454463992').click()
    
    try: 
       browser.find_element_by_link_text("Sign In").click()
       time.sleep(random.randint(3,5))
    except:  
        browser.get('https://www.kijiji.ca/t-login.html')
        time.sleep(random.randint(4,6))
    # Login by finding the correct fields by ID
    
    try:
       browser.find_element_by_xpath("//input[@type='email']").send_keys(creds[0])    
    except Exception as e:
        f=open("log.txt","a")
        f.write(str(e))
        f.close()
        try:
           browser.find_element_by_id("emailOrNickname").send_keys(creds[0])
        except Exception as e:
            f=open("log.txt","a")
            f.write(str(e))
            f.close()
            browser.find_element_by_xpath("//*[@id='emailOrNickname']").send_keys(creds[0])
            
        
    time.sleep(random.randint(4,6))
    browser.find_element_by_id("password").send_keys(creds[1])
    time.sleep(random.randint(2,3))
    try:   
      #browser.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div/div/form/button").click()
      #browser.find_element_by_tag_name('button')
      
      pyautogui.press('enter')
      time.sleep(random.randint(4,5))
      pickle.dump( browser.get_cookies() , open("cookies1.pkl","wb"))
      x = re.search('https://www.kijiji.ca/t-login.html',browser.current_url ) 
      if x:
         pyautogui.press('enter')
    #browser.find_element_by_class_name('signInButton-3250695435').click()
    except Exception as e :
        pyautogui.press('enter')
        time.sleep(random.randint(1,2))
        pyautogui.press('enter')
        
        f=open("log.txt","a")
        f.write(str(e))
        f.close()
    
    # Wait for page load
    

   # browser.find_element_by_xpath('//*[@id="SearchLocationPicker"]').click()
    #time.sleep(shortSleep)
    #browser.find_element_by_xpath('//*[@placeholder="Address, postal code, city or province"]').send_keys(address)
   # time.sleep(10)
   # pyautogui.press('space')
    #time.sleep(2)
    
    #pyautogui.press('enter')
    #time.sleep(5)
    #browser.find_element_by_xpath('//*[@class="submitButton-2124651659 button-1997310527 button__primary-1681489609 button__medium-1066667140"]').click()
    '''
    time.sleep(random.randint(4,5))
    return browser

# This will delete all the currently active ads
def deleteAds(browser):

    browser.get("https://www.kijiji.ca/m-my-ads/active/1")
    time.sleep(longSleep)
    
    x = re.search('https://www.kijiji.ca/t-login.html',browser.current_url ) 
    if x:
        browser.quit()
        #time.sleep(random.randint(120,240))
        #os.system('start cmd.exe /c kijiji.py') 
        quit()
    # Assume there are at most 10 ads
    # Click each element from the xpaths here
    # Scrolling to each element might be a good idea too
    # Basically click, wait, repeat

    for i in range(1, 3):

        # Try to click each one
        try:
            # You can see that each delete button is differentiated by a different line index
            #xpath = "/html/body/div[3]/div[4]/div/div/div/div[4]/ul/li[%s]/div[2]/div/ul/li[2]/button/span" % str(i)
            #browser.find_element_by_xpath(xpath).click()
            browser.find_element_by_xpath("//button[@data-qa-id='adDeleteButton']").click()
            time.sleep(2)
            pyautogui.moveTo(567,424,2)
            time.sleep(3)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div[9]/div/div/div/div/div/div[2]/div[2]/button').click()
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div[9]/div/div/div/div/div/div[1]/button[1]').click()
            time.sleep(longSleep)
        except:
            
            # No more ads to delete
            time.sleep(longSleep)
            break
    browser.get("https://www.kijiji.ca/m-my-ads/inactive/1")
    time.sleep(longSleep)

    # Assume there are at most 10 ads
    # Click each element from the xpaths here
    # Scrolling to each element might be a good idea too
    # Basically click, wait, repeat

    for i in range(1, 5):

        # Try to click each one
        try:
            # You can see that each delete button is differentiated by a different line index
            #xpath = "/html/body/div[3]/div[4]/div/div/div/div[4]/ul/li[%s]/div[2]/div/ul/li[2]/button/span" % str(i)
            #browser.find_element_by_xpath(xpath).click()
            browser.find_element_by_xpath("//button[@data-qa-id='adDeleteButton']").click()
            time.sleep(2)
            pyautogui.moveTo(567,424,2)
            time.sleep(3)   
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div[10]/div/div/div/div/div/div[2]/div[2]/button').click()
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div[10]/div/div/div/div/div/div[1]/button[1]').click()
            time.sleep(longSleep)
        except:
            # No more ads to delete
            time.sleep(longSleep)
            break
    # exit()
    # /html/body/div[3]/div[4]/div/div/div/div[4]/ul/li[4]/div[2]/div/ul/li[2]/button/span
    # /html/body/div[3]/div[4]/div/div/div/div[4]/ul/li[3]/div[2]/div/ul/li[2]/button/span
    # /html/body/div[3]/div[4]/div/div/div/div[4]/ul/li[2]/div[2]/div/ul/li[2]/button/span
    # /html/body/div[3]/div[4]/div/div/div/div[4]/ul/li[1]/div[2]/div/ul/li[2]/button/span


# This will post an ad to the kijiji marketplace, takes browser object and directory
def postAd(browser, directory):

    # Get ad info
    title, category, key,  description = getAdInformation(directory)

    browser.get("https://www.kijiji.ca/p-admarkt-post-ad.html?categoryId=%s&adTitle=" % (str(category)))
    time.sleep(longSleep)

    # Input title
    browser.find_element_by_xpath('//*[@id="postad-title"]').send_keys(title)
    time.sleep(shortSleep)

    # Input description
    browser.find_element_by_xpath('//*[@id="pstad-descrptn"]').send_keys(description)
    time.sleep(shortSleep)
    browser.find_element_by_xpath('//*[@id="pstad-tagsInput"]').send_keys(key)
    time.sleep(shortSleep)
    browser.find_element_by_xpath('//button[text()="Add"]').click()
    time.sleep(shortSleep)
    browser.find_element_by_xpath('//*[@id="pstad-map-address"]').send_keys(postalCode)
    time.sleep(shortSleep)
    pyautogui.press("pagedown")

    # Create the file string and enter it into the image selection window
    # Allow files to be uploaded
    # I think really slow internet could mess this part up, so we will give it some generous load time (5 seconds)
    # Need to replace \\ with / for some reason, mac vs windows inconsistencies are getting annoying
    images = getAdImagePaths(directory)
    files = ""
    for imagePath in images:
        files += '"' + imagePath.replace("//", "\\") + '" '
        # files += '' + imagePath.replace("//", "\\") + ' '


    # Select images
    browser.find_element_by_xpath('//*[@id="ImageUploadButton"]').click()
    time.sleep(longSleep)
    #browser.execute_script("document.getElementById('ImageUploadButton').setAttribute('value', '%s')" % files)
    #time.sleep(longSleep)
    pyautogui.typewrite(files)
    time.sleep(5)
    pyautogui.press(['enter','enter'])
  
    

    # Allow lots of time for pictures to upload, maybe like 10 seconds?
    time.sleep(60)
    pyautogui.press("pagedown")
    # Enter postal code (also hard coded)
    # This only needs to be done once (ever?) so we can just use a try/except
    try:
        browser.find_element_by_xpath('//*[@id="location"]').send_keys(location.replace("-", ""))
        
        
        time.sleep(longSleep)
        pyautogui.press("down")
        pyautogui.press("enter")
        pyautogui.press("pagedown")

    except:
        # Basically, skip this location part because it is already there
        pass
    time.sleep(shortSleep)

    # Enter price and phone number (hard coded)
    #browser.find_element_by_xpath('//*[@id="PriceAmount"]').send_keys(price.replace("$", "").replace(",", ""))
    #time.sleep(shortSleep)
    browser.find_element_by_xpath('//*[@id="PhoneNumber"]').send_keys(phone.replace("-", ""))
    time.sleep(shortSleep) 
    pyautogui.press("pagedown")
    time.sleep(6)
    try:
        
       browser.find_element_by_xpath('//*[@data-qa-id="package-0-bottom-select"]').click()
    except:
        pass
   # browser.find_element_by_xpath('//*[@data-qa-id="package-0-bottom-select"]').click()
    time.sleep(3)
    
    # Post Ad
    # Strange, it seems the full xpath only seems to work some of the time
    # It is *rarely* different when I get the path from the inspector
    # We will try this shortened path instead
    # browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[1]/form/div/div[9]/button[1]').click()
    # Right now we will just try to click on both xpaths that potentially lead to the Post Your Ad button
    # browser.find_element_by_xpath('//*[@id="MainForm"]/div[9]/button[1]').click()
    # browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/header/div[3]/div/div[2]/div/a[2]')
    try:
        
        # This should work
        browser.find_element_by_name('saveAndCheckout').click()
    except:
        pass
        # If it doesn't, use the error Rohan was getting on his surface laptop
        browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/header/div[3]/div/div[2]/div/a[2]').click()

    # This is some extra sleeping for loading, uploading, and to make it look like not a bot??
    time.sleep(longSleep)
    pyautogui.press("pagedown")
    time.sleep(longSleep)


def main():

    # So because kijiji limits free accounts to 10 ads each, we must cycle through properly
    # Do this later
    credentials = getCredentials()

    # Get the ads
    ads = getAds()
    print(ads)

    # We want to post 10 ads per account
    # Just increment and login to the new account every 10 ads
    counter = 0
    for creds in credentials:

        # Login to the new account and delete all the ads
        browser = login(creds)
        deleteAds(browser)
        time.sleep(random.randint(160,185))
        for i in range(2):
            try:
                ad = ads[counter]
            except:
                # No more ads to post
                # Program exits
                print("All ads posted")
                exit()

            postAd(browser, ad)
            print(ad, "posted")
            time.sleep(random.randint(150,170))
            counter += 1
        # Close the browser and start again with the new account
        # Could also just logout and login with the new account but not a big deal here
        browser.close()
        #time.sleep(random.randint(600,700))

main()
