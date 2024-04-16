import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from functions import waitPageLoad, waitAdblockActivation, checkIfElementIsVisible

XPATH = {"addButton": "//button[@id='add_btn']",
         "secondInputField": "//div[@id='row2']/input",
         "successMessage": "//div[@id='confirmation']",}
URLS = {"pageURL": "https://practicetestautomation.com/practice-test-exceptions/"}
CASE = "\n--- Caso 6 ---\n"
XPATHSUCCESSCASE = {"secondInputField": "El segundo campo de texto es visible",
                    "successMessage": "El mensaje de segunda línea agregada es visible"}
XPATHFAILURECASE = {"secondInputField": "El segundo campo de texto no es visible",
                    "successMessage": "El mensaje de segunda línea agregada no es visible"}
TIME = 5.2
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
    #Wait for the page to load
    waitPageLoad("Esperando a que la página cargue...", 50)

    #Click on the add button
    driver.find_element(By.XPATH, XPATH["addButton"]).click()
    print("Se hizo click en el botón de añadir")
    #Check if the second input field is visible
    checkIfElementIsVisible(XPATH["secondInputField"], "secondInputField", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, TIME)
    #Check if the success message is visible
    checkIfElementIsVisible(XPATH["successMessage"], "successMessage", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, TIME)
    
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
except ElementClickInterceptedException as e:
    print("Ocurrio un error al intentar hacer click en un elemento")
except Exception as e:
    print("Ocurrio un error de tipo: ", repr(e))
finally:
    driver.quit()