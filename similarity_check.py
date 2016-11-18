from pyvirtualdisplay import Display
from selenium import webdriver
import selenium
import time
from selenium.webdriver.common.keys import Keys

def filter(l) :
    res = []
    while (len(res) < 3) :
        if ('wiki' in l[i]) :
            continue
        res.append(l[i])
    return res


def get_links(title1 , title2) :
    search_query = title1 + "," + title2
    url = 'https://www.google.com/search?q='+search_query
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Chrome()
    driver.get(url)
    results = driver.find_elements_by_css_selector('h3')
    links = []
    for i in range(10) :
        link = results[i].find_element_by_tag_name("a")
        href = link.get_attribute("href")
        links.append(href)
    return filter(links)









