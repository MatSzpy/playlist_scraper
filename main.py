from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pyforest import *
import pandas

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get('https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U')
time.sleep(3)
driver.execute_script("document.body.style.zoom = '0.04'")
time.sleep(3)
search = driver.find_elements(By.XPATH, "//div[@class='JUa6JJNj7R_Y3i4P8YUX']")
dataframe = []
for song in search:
    content = song.text
output = content.split("\n")
output = list(filter(lambda x: x != 'E', output)) #removing "E" from list (explicit content)
splits = np.array_split(output, len(output)/6)
for array in splits:
    link_song = driver.find_elements(By.XPATH, "//div[@class='iCQtmPqY0QvkumAOuCjr']/a")
    array = np.append(array, link_song[int(list(array)[0])-1].get_attribute('href')) #adding link to the song
    array[2] = array[2].split(", ")[0]
    dataframe.append(list(array)) #creating dataframe from lists
    print(list(array))
dataframe = pandas.DataFrame(dataframe, columns = ["Position", "Name", "Author", "Album", "Date", "Duration", "Link"])
writer = pandas.ExcelWriter("playlist.xlsx")
dataframe.to_excel(writer)
writer.save() #saving dataframe in Excel file
print(dataframe)
driver.close()