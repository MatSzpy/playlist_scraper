from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pyforest import *

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get('https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U')
time.sleep(3)
search = driver.find_elements(By.XPATH, "//div[@class='JUa6JJNj7R_Y3i4P8YUX']")
for piece in search:
    content = piece.text
output = content.split("\n")
output = list(filter(lambda x: x != 'E', output)) #removing "E" from list (explicit content)
splits = np.array_split(output, len(output)/6)
for array in splits:
    print(list(array))
driver.close()