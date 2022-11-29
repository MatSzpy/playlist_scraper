from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pyforest import *
import pandas

def logging_in():
    print("E-mail: ")
    my_login = input()
    print("Password: ")
    my_password = input()
    login_start = driver.find_element(By.CSS_SELECTOR, "div.LKFFk88SIRC9QKKUWR5u > button.Button-sc-qlcn5g-0.jsmWVV")
    login_start.click()
    time.sleep(3)
    login = driver.find_element(By.CSS_SELECTOR, '#login-username')
    login.send_keys(my_login)
    time.sleep(2)
    login = driver.find_element(By.CSS_SELECTOR, '#login-password')
    login.send_keys(my_password)
    time.sleep(2)
    logging_in = driver.find_element(By.CSS_SELECTOR,'#login-button > div.ButtonInner-sc-14ud5tc-0.lbsIMA.encore-bright-accent-set')
    logging_in.click()

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get('https://open.spotify.com/')
time.sleep(3)
logging_in() #logowanie do Spotify
time.sleep(3)
driver.get('https://open.spotify.com/playlist/1SQsULHYDVHhG5mHSROZ0z')
time.sleep(4)
cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
cookies.click()
time.sleep(3)
driver.execute_script("document.body.style.zoom = '0.04'")
time.sleep(10)
search = driver.find_elements(By.CSS_SELECTOR, "div.ShMHCGsT93epRGdxJp2w.Ss6hr6HYpN4wjHJ9GHmi > div.JUa6JJNj7R_Y3i4P8YUX")
dataframe = []
artists = []
for song in search:
    content = song.text
output = content.split("\n")
print(output)
output = list(filter(lambda x: x != 'E', output)) #removing "E" from list (explicit content)
splits = np.array_split(output, len(output)/6)
print(splits)
for array in splits:
    link_song = driver.find_elements(By.XPATH, "//div[@class='iCQtmPqY0QvkumAOuCjr']/a")
    array = np.append(array, link_song[int(list(array)[0])-1].get_attribute('href')) #adding link to the song
    array[2] = array[2].split(", ")[0]
    dataframe.append(list(array)) #creating dataframe from lists
    artists.append(list(array)[2])
print(len(dataframe))
#years = list(dict.fromkeys(artists))
#for i in years:
#    driver.get('https://www.last.fm/music/' + i)
#    time.sleep(3)
#    try:
#        reject = driver.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]')
#        reject.click()
#    except:
#        pass
#    activity = driver.find_element(By.CSS_SELECTOR, 'div.metadata-column > dl')
#    activity = (activity.text)[:4]
#    years[i] = activity
#print(years)
dataframe = pandas.DataFrame(dataframe, columns = ["Position", "Name", "Author", "Album", "Date", "Duration", "Link"])
writer = pandas.ExcelWriter("playlist.xlsx")
dataframe.to_excel(writer)
writer.save() #saving dataframe in Excel file
print('Do you want to create a new playlist? (y/n)')
if input() == "y":
    driver.execute_script("document.body.style.zoom = '1'")
    time.sleep(2)
    new_playlist = driver.find_element(By.CSS_SELECTOR, 'div.GlueDropTarget.GlueDropTarget--albums.GlueDropTarget--tracks.GlueDropTarget--local-tracks.GlueDropTarget--episodes > button > span')
    new_playlist.click()
    time.sleep(2)
    playlist_name = driver.find_element(By.CSS_SELECTOR, 'div.RP2rRchy4i8TIp1CTmb7 > span > button > span > h1')
    playlist_name.click()
    time.sleep(2)
    new_playlist_name = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Add a name']")
    print("What do you want to name the new playlist?")
    new_playlist_name.send_keys(input())
    save_playlist_name = driver.find_element(By.CSS_SELECTOR, 'div.Up_Ke_BKTraatSMY_Po_ > button > span')
    save_playlist_name.click()
    time.sleep(2)
    add_excel_song = driver.find_element(By.CSS_SELECTOR, 'div.rezqw3Q4OEPB1m4rmwfw > div.contentSpacing > section > div > div > input')
    #testy = []
    i = 0
    reader = pandas.read_excel("playlist.xlsx", usecols=['Name'])
    for data in reader.values:
        add_excel_song.send_keys(reader.values[i][0])
        time.sleep(2)
        choose_song = driver.find_element(By.CSS_SELECTOR, "button[data-testid*='add-to-playlist-button']")
        choose_song.click()
        clear_search = driver.find_element(By.CSS_SELECTOR, 'div.contentSpacing > section > div > div > div > button > svg > path')
        clear_search.click()
        time.sleep(2)
        #testy.append(reader.values[i][0])
        i += 1
    #print(testy)
    time.sleep(2)
    driver.close()
else:
    driver.close()