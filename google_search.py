from pyvirtualdisplay import Display
from selenium import webdriver
import selenium
import time
from selenium.webdriver.common.keys import Keys

display = Display(visible=0, size=(800, 600))
display.start()

driver = webdriver.Chrome()

#driver.get('http://www.google.com')

driver.get("https://www.google.com/search?q=New York")

results = driver.find_elements_by_css_selector('h3')
link = results[1].find_element_by_tag_name("a")
href = link.get_attribute("href")
driver.get(href)
page = driver.find_element_by_tag_name("body").text
print page

display.stop()