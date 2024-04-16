import time
from tqdm import tqdm
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

XPATH = {"firstXPATH": "//img[@alt='Website for automation practice']", 
         "secondXPATH": "//img[@alt='demo website for practice']",
         "thirdXPATH": "//input[@id='susbscribe_email']",
         "fourthXPATH": "//a[contains(text(),'Signup / Login')]"}
TITLE = "Automation Exercise - Signup / Login"
URLS = {"pageURL": "https://automationexercise.com/"}
CASE = "\n--- Caso 1 ---\n"
XPATHSUCCESSCASE = {"firstXPATHMessage": "El logo de la página es visible",
                    "secondXPATHMessage": "La imagen del slider es visible",
                    "thirdXPATHMessage": "La caja de búsqueda es visible",}
XPATHFAILURECASE = {"firstXPATHMessage": "El logo de la página no es visible",
                    "secondXPATHMessage": "La imagen del slider no es visible",
                    "thirdXPATHMessage": "La caja de búsqueda no es visible",}

#Function to wait for the page to load
def waitPageLoad(message, timeout):
    seconds = range(timeout)
    for second in tqdm(seconds, desc=message, bar_format="{l_bar}{bar}|"):
        time.sleep(0.1)

#Wait for the AdBlock extension to be activated
def waitAdblockActivation():
    waitPageLoad("Esperando que cargue la extensión de AdBlock...", 80)
    print("Se cargó la extensión de AdBlock\n")
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()

#Function to check if an element is visible
def checkIfElementIsVisible(element, XPATHMessage):
    if(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))):
        print(XPATHSUCCESSCASE[XPATHMessage])
    else:
        print(XPATHFAILURECASE[XPATHMessage])
        raise NoSuchElementException

#Set the options for the browser
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument(f"--load-extension={os.path.abspath("./AdBlock")}")

#Open the browser
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

#Open the URL
print(CASE)
driver.get(URLS["pageURL"])
waitAdblockActivation()

try:
    #Wait for the page to load and check the logo of the page is visible
    waitPageLoad("Esperando a que la página cargue...", 50)
    checkIfElementIsVisible(XPATH["firstXPATH"], "firstXPATHMessage")
    checkIfElementIsVisible(XPATH["secondXPATH"], "secondXPATHMessage")
    checkIfElementIsVisible(XPATH["thirdXPATH"], "thirdXPATHMessage")

    #Click on the Signup/Login button
    productButton = driver.find_element(By.XPATH, XPATH["fourthXPATH"])
    productButton.click()
    print("Se hizo click en el botón de Signup/Login\n")

    #Wait for the page to load and check the title of the current page
    waitPageLoad("Esperando a que la página cargue...", 50)
    signupLoginTitle = driver.title
    assert TITLE == signupLoginTitle
    print("El título de la página es correcto")

    #Success message if all the test cases pass
    print("\nTodos los casos de prueba han sido ejecutados correctamente.",
          "\nCerrando el navegador...\n")
except TimeoutException as e:
    print("Ocurrio un error al intentar esperar a que un elemento se cargue")
except NoSuchElementException as e:
    print("Ocurrio un error al intentar encontrar un elemento en el DOM")
except AssertionError as e:
    print("Ocurrio un error al intentar hacer una validación")
except Exception as e:
    print("Ocurrio un error de tipo: ", repr(e))
except NoSuchWindowException as e:
    print("Ocurrio un error en la página objetivo")
finally:
    driver.quit()