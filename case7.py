import time
from tqdm import tqdm
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

XPATH = {"firstPageXPATH": "//a[contains(@href, '/products')]", 
         "secondPageXPATH": "//a[contains(@href, '/product_details/1')]",
         "thirdPageXPATH": "//div[2]/div[2]/div[2]/div"}
TITLE = "Automation Exercise - All Products"
URLS = {"pageURL": "https://automationexercise.com/",
        "firstURL": "https://automationexercise.com/product_details/1"}
CASE = "\n--- Caso 7 ---\n"
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
PRODUCTDETAILSSUCCESSCASE = {
                            "name": "El nombre del producto es correcto",
                            "category": "La categoría del producto es correcta",
                            "price": "El precio del producto es correcto",
                            "availability": "La disponibilidad del producto es correcta",
                            "condition": "La condición del producto es correcta",
                            "brand": "La marca del producto es correcta"
                            }
PRODUCTDETAILSFAILURECASE = {
                            "name": f"El nombre del producto es incorrecto, se esperaba {PRODUCTDETAILS['name']} y se obtuvo",
                            "category": f"La categoría del producto es incorrecta, se esperaba {PRODUCTDETAILS['category']} y se obtuvo",
                            "price": f"El precio del producto es incorrecto, se esperaba {PRODUCTDETAILS['price']} y se obtuvo",
                            "availability": f"La disponibilidad del producto es incorrecta, se esperaba {PRODUCTDETAILS['availability']} y se obtuvo",
                            "condition": f"La condición del producto es incorrecta, se esperaba {PRODUCTDETAILS['condition']} y se obtuvo",
                            "brand": f"La marca del producto es incorrecta, se esperaba {PRODUCTDETAILS['brand']} y se obtuvo"
                            }

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

#Check the product details and extract only the necessary information
def checkProductDetails(element, index):
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
    #Wait for the page to load and click on the products button
    waitPageLoad("Esperando a que la página cargue...", 50)
    productButton = driver.find_element(By.XPATH, XPATH["firstPageXPATH"])
    productButton.click()
    print("Se hizo click en el botón de productos\n")

    #Wait for the page to load and check the title of the current page
    waitPageLoad("Esperando a que la página cargue...", 50)
    productsPageTitle = driver.title
    assert TITLE == productsPageTitle
    print("El título de la página es correcto")
    #Wait for the page to load and click on the first view product
    viewProduct = driver.find_element(By.XPATH, XPATH["secondPageXPATH"])
    viewProduct.click()
    print("Se hizo click en el primer producto\n")

    #Wait for the page to load and check the URL
    waitPageLoad("Esperando a que la página cargue...", 50)
    currentUrl = driver.current_url
    assert URLS["firstURL"] == currentUrl
    print("La URL de la página es correcta")
    #Check if the product information is displayed
    if(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATH["thirdPageXPATH"])))):
        print("La información del producto es visible")
    productDetails = driver.find_element(By.XPATH, XPATH["thirdPageXPATH"]).text.split("\n")
    productDetails.pop(3)
    for element in productDetails:
        checkProductDetails(element, productDetails.index(element))
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