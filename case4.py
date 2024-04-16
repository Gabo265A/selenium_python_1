import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from functions import waitPageLoad, waitAdblockActivation, checkIfElementIsVisible, checkText

XPATH = {"username": "//input[@id='username']",
         "password": "//input[@id='password']",
         "submitButtom": "//button[@id='submit']",
         "errorMessage": "//div[@id='error']"}
USERDATA = {"username": "incorrectUser", "password": "Password123"}
URLS = {"pageURL": "https://practicetestautomation.com/practice-test-login/"}
CASE = "\n--- Caso 4 ---\n"
XPATHSUCCESSCASE = {"errorMessage": "El mensaje de error es visible",
                    "textError": "El mensaje de error es correcto"}
XPATHFAILURECASE = {"errorMessage": "El mensaje de error no es visible",
                    "textError": "El mensaje de error no es correcto"}
CHECKTEXT = ["Your username is invalid!"]

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

    #Type the username and password
    driver.find_element(By.XPATH, XPATH["username"]).send_keys(USERDATA["username"])
    print("Se ingresó el nombre de usuario")
    driver.find_element(By.XPATH, XPATH["password"]).send_keys(USERDATA["password"])
    print("Se ingresó la contraseña")
    #Click on the submit button
    driver.find_element(By.XPATH, XPATH["submitButtom"]).click()
    print("Se hizo click en el botón de submit")
    #Check if the error message is visible
    checkIfElementIsVisible(XPATH["errorMessage"], "errorMessage", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)
    #Check if error message is correct
    checkText(XPATH["errorMessage"], CHECKTEXT[0], driver, XPATHSUCCESSCASE, XPATHFAILURECASE, "textError")
    
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