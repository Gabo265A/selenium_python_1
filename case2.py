import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from functions import waitPageLoad, waitAdblockActivation, checkProductDetails, checkIfElementIsVisible, checkText

XPATH = {"productsButtom": "//a[contains(@href, '/products')]", 
         "brand": "//a[contains(@href, '/brand_products/H&M')]",
         "productCard": "//div[2]/div/div[2]/div",
         "productName": "//p[contains(.,'Men Tshirt')]",
         "ViewProduct": "//a[contains(@href, '/product_details/2')]",
         "productIMG": "//img[@alt='ecommerce website products']",
         "productInformation": "//div[2]/div[2]/div[2]/div",
         "addToCart": "//span/button",
         "addedToCart": "//div[@id='cartModal']/div/div/div[2]/p",
         "procedToCheckout": "//u[contains(.,'View Cart')]",}
URLS = {"pageURL": "https://automationexercise.com/"}
CASE = "\n--- Caso 2 ---\n"
PRODUCTDETAILSLABELS = ["price",
                        "availability",
                        "condition",
                        "brand"]
PRODUCTDETAILS = {"price": "Rs. 400",
                "availability": "In Stock",
                "condition": "New",
                "brand": "H&M"}
PRODUCTDETAILSSUCCESSCASE = {"price": "El precio del producto es correcto",
                            "availability": "La disponibilidad del producto es correcta",
                            "condition": "La condición del producto es correcta",
                            "brand": "La marca del producto es correcta"}
PRODUCTDETAILSFAILURECASE = {"price": f"El precio del producto es incorrecto, se esperaba {PRODUCTDETAILS['price']} y se obtuvo",
                            "availability": f"La disponibilidad del producto es incorrecta, se esperaba {PRODUCTDETAILS['availability']} y se obtuvo",
                            "condition": f"La condición del producto es incorrecta, se esperaba {PRODUCTDETAILS['condition']} y se obtuvo",
                            "brand": f"La marca del producto es incorrecta, se esperaba {PRODUCTDETAILS['brand']} y se obtuvo"}
XPATHSUCCESSCASE = {"productCard": "La tarjeta del producto es visible",
                    "productIMG": "La imagen del producto es visible",
                    "productName": "El nombre del producto es correcto",
                    "addedToCart": "El texto de confirmación es correcto"
                    }
XPATHFAILURECASE = {"productCard": "La tarjeta del producto no es visible",
                    "productIMG": "La imagen del producto no es visible",
                    "productName": "El nombre del producto no es correcto",
                    "addedToCart": "El texto de confirmación no es correcto"}
CHECKTEXT = ["Men Tshirt", "Your product has been added to cart."]

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

    #Click on the products button
    driver.find_element(By.XPATH, XPATH["productsButtom"]).click()
    print("Se hizo click en el botón de productos\n")

    #Click on the brand button
    waitPageLoad("Esperando a que la página cargue...", 50)
    driver.find_element(By.XPATH, XPATH["brand"]).click()
    print("Se hizo click en el botón de la marca\n")

    #Check if the product card is visible
    waitPageLoad("Esperando a que la página cargue...", 50)
    checkIfElementIsVisible(XPATH["productCard"], "productCard", driver, XPATHSUCCESSCASE, XPATHFAILURECASE)
    checkText(XPATH["productName"], CHECKTEXT[0], driver, XPATHSUCCESSCASE, XPATHFAILURECASE, "productName")
    driver.find_element(By.XPATH, XPATH["ViewProduct"]).click()
    print("Se hizo click en el botón de la marca\n")

    #Check the product details
    waitPageLoad("Esperando a que la página cargue...", 50)
    checkIfElementIsVisible(XPATH["productIMG"], "productIMG", driver, XPATHSUCCESSCASE, XPATHFAILURECASE)
    productDetails = driver.find_element(By.XPATH, XPATH["productInformation"]).text.split("\n")
    productDetails = productDetails[2:3] + productDetails[4:]
    for element in productDetails:
        checkProductDetails(element, productDetails.index(element), PRODUCTDETAILSLABELS, PRODUCTDETAILS, PRODUCTDETAILSSUCCESSCASE, PRODUCTDETAILSFAILURECASE)

    #Click on the add to cart button
    driver.find_element(By.XPATH, XPATH["addToCart"]).click()
    print("Se hizo click en el botón de añadir al carrito\n")

    #Wait message to confirm the product was added to the cart
    waitPageLoad("Esperando a que se añada el producto al carrito...", 30)
    checkText(XPATH["addedToCart"], CHECKTEXT[1], driver, XPATHSUCCESSCASE, XPATHFAILURECASE, "addedToCart")
    print("")

    #Click on the view cart
    waitPageLoad("Esperando a que se cargue el modal...", 30)
    driver.find_element(By.XPATH, XPATH["procedToCheckout"]).click()
    print("Se hizo click en el botón de proceder al checkout\n")

    #Success message if all the test cases pass
    print("Todos los casos de prueba han sido ejecutados correctamente.\n")
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