import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options
from functions import waitPageLoad, waitAdblockActivation, checkIfElementIsVisible

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
waitAdblockActivation(driver)

try:
    #Wait for the page to load and check the logo of the page is visible
    waitPageLoad("Esperando a que la página cargue...", 50)
    checkIfElementIsVisible(XPATH["firstXPATH"], "firstXPATHMessage", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)
    checkIfElementIsVisible(XPATH["secondXPATH"], "secondXPATHMessage", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)
    checkIfElementIsVisible(XPATH["thirdXPATH"], "thirdXPATHMessage", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)

    #Click on the Signup/Login button
    driver.find_element(By.XPATH, XPATH["fourthXPATH"]).click()
    print("Se hizo click en el botón de Signup/Login\n")

    #Wait for the page to load and check the title of the current page
    waitPageLoad("Esperando a que la página cargue...", 50)
    assert TITLE == driver.title
    print("El título de la página es correcto")

    #Success message if all the test cases pass
    print("\nTodos los casos de prueba han sido ejecutados correctamente.")
    waitPageLoad("Cerrando el navegador...", 30)
except TimeoutException as e:
    print("Ocurrio un error al intentar esperar a que un elemento se cargue")
except NoSuchElementException as e:
    print("Ocurrio un error al intentar encontrar un elemento en el DOM")
except AssertionError as e:
    print("Ocurrio un error al intentar hacer una validación")
except NoSuchWindowException as e:
    print("Ocurrio un error en la página objetivo")
except Exception as e:
    print("Ocurrio un error de tipo: ", repr(e))
finally:
    driver.quit()