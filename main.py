from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pyforest import *

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get('https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U')
time.sleep(3)
driver.execute_script("document.body.style.zoom = '0.04'")
#scroll = driver.find_element(By.XPATH, "//div[@class='os-scrollbar-handle']")
#print(scroll.value_of_css_property("transform"))
#driver.execute_script("arguments[0].style.transform = 'translate(0px, 100.0000px)';", scroll)
#print(scroll.value_of_css_property("transform"))
time.sleep(3)
search = driver.find_elements(By.XPATH, "//div[@class='JUa6JJNj7R_Y3i4P8YUX']")
for song in search:
    content = song.text
output = content.split("\n")
output = list(filter(lambda x: x != 'E', output)) #removing "E" from list (explicit content)
splits = np.array_split(output, len(output)/6)
for array in splits:
    link_song = driver.find_element(By.XPATH, "//div[@class='iCQtmPqY0QvkumAOuCjr']/a").get_attribute('href')
    array = np.append(array, link_song)
    array[2] = array[2].split(", ")[0]
    print(list(array))
driver.close()