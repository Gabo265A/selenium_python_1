from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from tqdm import tqdm

#Function to wait for the page to load
def waitPageLoad(message, timeout):
    seconds = range(timeout)
    for second in tqdm(seconds, desc=message, bar_format="{l_bar}{bar}|"):
        time.sleep(0.1)

#Wait for the AdBlock extension to be activated
def waitAdblockActivation(driver):
    waitPageLoad("Esperando que cargue la extensión de AdBlock...", 80)
    print("Se cargó la extensión de AdBlock\n")
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()

#Check the product details and extract only the necessary information
def checkProductDetails(element, index, PRODUCTDETAILSLABELS, PRODUCTDETAILS, PRODUCTDETAILSSUCCESSCASE, PRODUCTDETAILSFAILURECASE):
    labelTitle = PRODUCTDETAILSLABELS[index]
    newElement = ""
    lenLabelWords = len(PRODUCTDETAILS[labelTitle].split(" "))
    countWords = 1
    for productDetailsWord in PRODUCTDETAILS[labelTitle].split(" "):
        for elementWord in element.split(" "):
            if(elementWord == productDetailsWord):
                if(countWords == lenLabelWords):
                    newElement += elementWord
                else:
                    newElement += elementWord + " "
                countWords += 1
                break
    if(PRODUCTDETAILS[labelTitle] == newElement):
        print(PRODUCTDETAILSSUCCESSCASE[labelTitle])
    else:
        print(PRODUCTDETAILSFAILURECASE[labelTitle], newElement)
        raise AssertionError
    
#Function to check if an element is visible
def checkIfElementIsVisible(element, XPATHMessage, driver, XPATHSUCCESSCASE, XPATHFAILURECASE, time):
    if(WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, element)))):
        print(XPATHSUCCESSCASE[XPATHMessage])
    else:
        print(XPATHFAILURECASE[XPATHMessage])
        raise TimeoutException
    
def checkText(element, text, driver, XPATHSUCCESSCASE, XPATHFAILURECASE, XPATHMessage):
    if(driver.find_element(By.XPATH, element).text == text):
        print(XPATHSUCCESSCASE[XPATHMessage])
    else:
        print(XPATHFAILURECASE[XPATHMessage])
        raise AssertionError

def checkContainsText(element, text, driver, XPATHSUCCESSCASE, XPATHFAILURECASE, XPATHMessage):
    containText = False
    for text in text:
        if(text in driver.find_element(By.XPATH, element).text):
            print(XPATHSUCCESSCASE[XPATHMessage])
            containText = True
            return
    if(not containText):
        print(XPATHFAILURECASE[XPATHMessage])
        raise AssertionError