import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from Beer import Beer

chrome_path = "C:/.libraries/chromedriver.exe"
url = "https://www.flaschenpost.de/bier/pils"

driver = webdriver.Chrome(executable_path=chrome_path)
driver.get(url)

# enter zip code in popup
zipField = driver.find_element_by_id("validZipcode")
zipField.send_keys("30167")

# find and press "LOS" button
inputField = driver.find_element_by_class_name("fp-modal_input")
button = inputField.find_element_by_tag_name("button")
button.click()

max_delay = 10
try:
    WebDriverWait(driver, max_delay).until(expected_conditions.presence_of_element_located((By.ID, "fp-productList")))
except:
    print("max timeout of {}s reached".format(max_delay))
    driver.quit()
    quit()
driver.get(url)
try:
    WebDriverWait(driver, max_delay).until(expected_conditions.presence_of_element_located((By.ID, "fp-sub-category-id")))
except:
    print("max timeout of {}s reached".format(max_delay))
    driver.quit()
    quit()

# sleep for cookie
# time.sleep(3)
# driver.get(url)
# time.sleep(1)

beer_list = []

productContainer = driver.find_element_by_id("fp-productList")
productList = productContainer.find_elements_by_class_name("fp-productList")
# each beer has its own <div class>
for beerDivClass in productList:
    brand = beerDivClass.get_attribute("data-brandname")
    name = beerDivClass.get_attribute("data-product")
    hasOffer = beerDivClass.get_attribute("data-has-offer")

    # each beerDivClass has 2 child divs: "fp-productList_image" and "fp-productList_content"
    # we are only interested in the content
    beerContentDiv = beerDivClass.find_element_by_class_name("fp-productList_content")
    # the beerContent contains 1 div for metadata (%alc) and 1 div for each variant of the beer
    metaDiv = beerContentDiv.find_element_by_class_name("fp-productList_info")
    alcPercent = metaDiv.find_element_by_class_name("fp-productList_alcohol").text

    # loop over divs containing variants of beer
    variantDivs = beerDivClass.find_elements_by_class_name("fp-productList_detail")
    for variantDiv in variantDivs:
        # each variantDiv has 4 child divs: "fp-productList_bottleDetails",
        # "fp-productList_price fp-productList_price--hasOld"/"fp-productList_price fp-price_info"
        # (depending on data-has-offer = true/false)
        # "fp-productList_count", "fp-productList_action"
        bottleDetailsDiv = variantDiv.find_element_by_class_name("fp-productList_bottleDetails")
        bottleInfoDiv = bottleDetailsDiv.find_element_by_class_name("fp-productList_bottleInfo")
        # "b" tag contains price
        divPrice = variantDiv.find_element_by_tag_name("b")
        # "small" tag contains price per litre
        divPPL = variantDiv.find_element_by_tag_name("small")
        # print(brand, name, hasOffer, alcPercent, bottleInfoDiv.text, div2.text)
        beer = Beer(brand, name, hasOffer, alcPercent, bottleInfoDiv.text, divPrice.text, divPPL.text)
        beer_list.append(beer)

driver.close()
print("beers found: " + str(len(beer_list)))

for beer in beer_list:
    beer.print()

print("\nsorting...\n")

beer_list.sort(key=lambda x: x.ppl, reverse=True)

for beer in beer_list:
    beer.print_fancy()
    print("")

