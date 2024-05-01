import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options
from functions import waitPageLoad, waitAdblockActivation, checkIfElementIsVisible

XPATH = {"XPATHCartText": "//*[@id='nav-cart-text-container']/span[2]",
         "XPATHLogo": "//*[@id='nav-logo-sprites']",
         "XPATHCustomerService": "//*[@id='nav-xshop']/a[2]",
         "XPATHInputSearch": "//*[@id='twotabsearchtextbox']",
         "XPATHChangeLanguage": "//*[@id='nav-flyout-icp']/div[2]/a[2]/span/span[1]",
         "XPATHSearchHelp": "//*[@id='twotabsearchtextbox']"}
TITLE = "Amazon.com en espanol. Gasta menos. Sonríe más."
URLS = {"amazonURL": "https://www.amazon.com/-/es/",}
CASE = "\n--- Caso 8 ---\n"
XPATHSUCCESSCASE = {"XPATHLogo": "El logo de la página es visible",
                    "XPATHCustomerService": "Elemento del menú 'Servicio al cliente' es visible",}
XPATHFAILURECASE = {"XPATHLogo": "El logo de la página no es visible",
                    "XPATHCustomerService": "Elemento del menú 'Servicio al cliente' no es visible",}
SUCCESSCASE = {"message": "Caso de prueba ejecutado correctamente hasta el momento."}

#Set the options for the browser
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument(f"--load-extension={os.path.abspath("./AdBlock")}")

#Open the browser
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

#Open the URL
print(CASE)
driver.get(URLS["amazonURL"])
waitAdblockActivation(driver)

try:
    #Wait for the page to load and resolve the captcha
    waitPageLoad("Esperando a que se resuelva el captcha manualmente...", 80)
    print("")

    #Wait for the page to load
    waitPageLoad("Esperando a que la página cargue...", 50)

    #Save and print the title page
    title_page = driver.title
    print(f"El título de la página es: {title_page}")

    #Save cart element and print the text
    element = driver.find_element(By.XPATH, XPATH["XPATHCartText"])
    print(f"Texto del carrito: {element.text}")

    #Print success message
    print(SUCCESSCASE["message"])

    #Verify the title of the page
    assert TITLE == title_page
    print("El título de la página es correcto")

    #Verify logo is visible
    checkIfElementIsVisible(XPATH["XPATHLogo"], "XPATHLogo", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)

    #Verify customer service is visible
    checkIfElementIsVisible(XPATH["XPATHCustomerService"], "XPATHCustomerService", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)

    #Type the text to search and print it
    element = driver.find_element(By.XPATH, XPATH["XPATHSearchHelp"])
    element.send_keys(input(f"Escriba el texto a buscar: "))
    print(f"El texto ingresado es {element.get_attribute("value")}")

    #Success message
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