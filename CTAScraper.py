from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": r"C:\Users\JohnLook\CTA_data",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=options)
driver.get("http://www.iasg.com")
# Login
driver.find_element_by_id("dnn_dnnLogin_enhancedLoginLink").click()
driver.find_element_by_id("username").send_keys("lmf20653@eoopy.com")
driver.find_element_by_id("password").send_keys("daveylmf")
driver.find_element_by_xpath("//button[@type='submit' and @ng-click='submitLoginForm(login, $event)']").click()
# Go to performance table
driver.get("https://www.iasg.com/en-us/managed-futures/performance?sdmax=2006")
table = driver.find_element_by_id("report.table")
table_html = table.get_attribute("outerHTML")
# Pass html to beautiful soup
bsObj = BeautifulSoup(table_html)
base_url = 'https://www.iasg.com/'
urls = []
# Collect all urls
for tr in bsObj.tbody.findAll("tr"):
    name_values = tr.findAll("th")[1].findAll("a")
    cta_dict = {
        "program": name_values[0].getText(),
        "fund": name_values[1].getText(),
        "url": name_values[1].get_attribute_list("href")[0]
    }
    urls.append(cta_dict)
# Visit fund page and download data
for url_dict in urls:
    driver.get(base_url+url_dict.get("url"))
    driver.maximize_window()
    time.sleep(2)
    # export_btn = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.ID, "lbExport")))
    # export_btn.click()
    driver.find_element_by_id("lbExport").click()

# Exit
driver.close()

