import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options
from functions import waitPageLoad, checkProductDetails, waitAdblockActivation, checkIfElementIsVisible
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

XPATH = {"XPATHFreeTrial": "//a[contains(.,'Comienza tu periodo de prueba gratis*')]", 
         "XPATHInputEmail": "//input[@id='ap_email']",
         "XPATHContinueButton": "//input[@id='continue']",
         "XPATHErrorMessage": "//div[@id='auth-error-message-box']/div",
         "XPATHUseAndPrivacy": "//a[contains(text(),'Condiciones de uso y el Aviso de privacidad')]",
         "XPATHCSSProperty": "//h1[contains(.,'INFORMACIÓN SOBRE EL PROVEEDOR DE SERVICIOS AMAZON PRIME VIDEO Y CONDICIONES Y POLÍTICAS APLICABLES')]",
         "XPATHUsser": "//*[@id='pv-nav-container']/div/div[2]/div[2]/div/ol/li[3]",
         "XPATHBurgerMenu": "//*[@id='pv-nav-container']/div/div[2]/div[2]/div/ol/li[3]/div",
         "XPATHSearchHelp": "//input[@name='search']",}
TITLE = "Bienvenido a Prime Video"
URLS = {"primeVideoURL": "https://www.primevideo.com/",
        "primeVideoUseAndPrivacyURL": "https://www.primevideo.com/help/ref=av_auth_te?nodeId=202064890"}
CASE = "\n--- Amazon Prime Video ---\n"
PRODUCTDETAILSLABELS = [
                        "name",
                        "category",
                        "price",
                        "availability",
                        "condition",
                        "brand"
                        ]
PRODUCTDETAILS = {
                "name": "Blue Top",
                "category": "Women",
                "price": "Rs. 500",
                "availability": "In Stock",
                "condition": "New",
                "brand": "Polo"
                }
XPATHSUCCESSCASE = {"XPATHFreeTrial": "Botón de prueba gratuita visible",
                    "XPATHErrorMessage": "El mensaje de error es visible",
                    "XPATHBurgerMenu": "El menú desplegable es visible"}
XPATHFAILURECASE = {"XPATHFreeTrial": "Botón de prueba gratuita no visible",
                    "XPATHErrorMessage": "El mensaje de error no es visible",
                    "XPATHBurgerMenu": "El menú desplegable no es visible"}
EXPECTEDTEXT = {"CssProperty": "21px"}
#Set the options for the browser
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument(f"--load-extension={os.path.abspath("./AdBlock")}")

#Open the browser
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

#Set the actions for the browser
actions = ActionChains(driver)

#Open the URL
print(CASE)
driver.get(URLS["primeVideoURL"])
waitAdblockActivation(driver)

try:
    #Wait for the page to load and check the title of the current page
    waitPageLoad("Esperando a que la página cargue...", 50)
    assert TITLE == driver.title
    print("El título de la página es correcto")
    
    #Check if the free trial button is visible
    checkIfElementIsVisible(XPATH["XPATHFreeTrial"], "XPATHFreeTrial", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)

    #Click on the button to start the free trial
    driver.find_element(By.XPATH, XPATH["XPATHFreeTrial"]).click()
    print("Se hizo click en el botón de prueba gratuita\n")

    #Wait for the page to load and run the test cases
    waitPageLoad("Esperando a que la página cargue...", 50)
    driver.find_element(By.XPATH, XPATH["XPATHInputEmail"]).send_keys("gabriel.loaiza@correo.tdea.eddu.co")
    print("Se ingresó el correo electrónico")
    driver.find_element(By.XPATH, XPATH["XPATHContinueButton"]).click()
    print("Se hizo click en el botón continuar")
    checkIfElementIsVisible(XPATH["XPATHErrorMessage"], "XPATHErrorMessage", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)
    driver.find_element(By.XPATH, XPATH["XPATHUseAndPrivacy"]).click()
    print("Se hizo click en el enlace de condiciones de uso y privacidad\n")

    #Wait for the page to load and check the URL
    waitPageLoad("Esperando a que la página cargue...", 50)
    if(driver.current_url == URLS["primeVideoUseAndPrivacyURL"]):
        print("La URL de la página es correcta")
    else:
        print("La URL de la página no es correcta")
    css_property = driver.find_element(By.XPATH, XPATH["XPATHCSSProperty"]).value_of_css_property('font-size')
    if(css_property == EXPECTEDTEXT["CssProperty"]):
        print("El tamaño de la fuente es correcto")
    else:
        print("El tamaño de la fuente no es correcto")
    element = driver.find_element(By.XPATH, XPATH["XPATHUsser"])
    actions.move_to_element(element).perform()
    checkIfElementIsVisible(XPATH["XPATHBurgerMenu"], "XPATHBurgerMenu", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)

    #Success message if all the test cases pass
    print("\nTodos los casos de prueba han sido ejecutados correctamente.")
    waitPageLoad("Cerrando el navegador...", 50)
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