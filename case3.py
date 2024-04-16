import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from functions import waitPageLoad, waitAdblockActivation, checkContainsText, checkIfElementIsVisible

XPATH = {"username": "//input[@id='username']",
         "password": "//input[@id='password']",
         "submitButtom": "//button[@id='submit']",
         "successMessage": "//strong[contains(.,'Congratulations student. You successfully logged in!')]",
         "logoutButtom": "//a[contains(text(),'Log out')]",}
USERDATA = {"username": "student", "password": "Password123"}
URLS = {"pageURL": "https://practicetestautomation.com/practice-test-login/",
        "successURL": "practicetestautomation.com/logged-in-successfully/"}
TITLE = "Logged In Successfully | Practice Test Automation"
CASE = "\n--- Caso 3 ---\n"
XPATHSUCCESSCASE = {"successMessage": "El mensaje de éxito contiene el texto 'Congratulations' o 'successfully logged in'",
                    "logoutButtom": "El botón de logout es visible"}
XPATHFAILURECASE = {"successMessage": "El mensaje de éxito no contiene el texto 'Congratulations' o 'successfully logged in'",
                    "logoutButtom": "El botón de logout no es visible"}

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
    print("Se hizo click en el botón de submit\n")

    #Wait for the page to load
    waitPageLoad("Esperando a que la página cargue...", 50)
    #Check if the URL is correct
    assert URLS["successURL"] in driver.current_url
    print("La url actual de la página es correcta")
    #Check if the success message contains 'Congratulations' or 'successfully logged in'
    checkContainsText(XPATH["successMessage"], ["Congratulations", "successfully logged in"], driver, XPATHSUCCESSCASE, XPATHFAILURECASE, "successMessage")
    #Check if the logout button is visible
    checkIfElementIsVisible(XPATH["logoutButtom"], "logoutButtom", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)
    #Check if the title is correct
    assert TITLE in driver.title
    print("El título de la página es correcto\n")
    
    #Success message if all the test cases pass
    print("Todos los casos de prueba han sido ejecutados correctamente.")
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