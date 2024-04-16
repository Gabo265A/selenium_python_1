import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options
from functions import waitPageLoad, checkProductDetails, waitAdblockActivation, checkIfElementIsVisible

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
XPATHSUCCESSCASE = {"thirdPageXPATH": "La información del producto es visible",
                    "secondXPATHMessage": "La imagen del slider es visible",
                    "thirdXPATHMessage": "La caja de búsqueda es visible",}
XPATHFAILURECASE = {"thirdPageXPATH": "La información del producto no es visible",
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
    #Wait for the page to load and click on the products button
    waitPageLoad("Esperando a que la página cargue...", 50)
    driver.find_element(By.XPATH, XPATH["firstPageXPATH"]).click()
    print("Se hizo click en el botón de productos\n")

    #Wait for the page to load and check the title of the current page
    waitPageLoad("Esperando a que la página cargue...", 50)
    assert TITLE == driver.title
    print("El título de la página es correcto")
    #Wait for the page to load and click on the first view product
    driver.find_element(By.XPATH, XPATH["secondPageXPATH"]).click()
    print("Se hizo click en el primer producto\n")

    #Wait for the page to load and check the URL
    waitPageLoad("Esperando a que la página cargue...", 50)
    assert URLS["firstURL"] == driver.current_url
    print("La URL de la página es correcta")
    #Check if the product information is displayed
    checkIfElementIsVisible(XPATH["thirdPageXPATH"], "thirdPageXPATH", driver, XPATHSUCCESSCASE, XPATHFAILURECASE, 10)
    #Check the product details and extract only the necessary information
    productDetails = driver.find_element(By.XPATH, XPATH["thirdPageXPATH"]).text.split("\n")
    productDetails.pop(3)
    for element in productDetails:
        checkProductDetails(element, productDetails.index(element), PRODUCTDETAILSLABELS, PRODUCTDETAILS, PRODUCTDETAILSSUCCESSCASE, PRODUCTDETAILSFAILURECASE)

    print("\nTodos los casos de prueba han sido ejecutados correctamente.\n")
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