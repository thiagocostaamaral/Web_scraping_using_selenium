
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import numpy as np
from datetime import datetime
from datetime import timedelta
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://www.windy.com/-5.189/-37.075?-5.244,-36.911,11')
time.sleep(2) #giving time to json get in the data
print('Clicking to extend table...')
element =  driver.find_element_by_xpath('//div[@class="fg-red size-xs inlined clickable"]').click()
time.sleep(2)

#Getting HTML
html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
soup = BeautifulSoup(html, 'html.parser')
table = soup.find(id="detail-data-table")
rows_wind = soup.find_all("tr", {"class": "td-wind height-wind d-display-table"})[0]
rows_gust = soup.find_all("tr", {"class": "td-gust height-gust d-display-table"})[0]
rows_direction = soup.find_all("tr", {"class": "td-windDir height-windDir d-display-table"})[0]
rows_temp= soup.find_all("tr", {"class": "td-temp height-temp d-display-table"})[0]
rows_hour= soup.find_all("tr", {"class": "td-hour height-hour d-display-table"})[0]
time.sleep(2)

#driver.close()

#%%
#Each row contain one data source


data_wind = str(rows_wind).split('</td>')
data_gust = str(rows_gust).split('</td>')
data_temp = str(rows_temp).split('°</td>')
data_hour = str(rows_hour).split('</td>')
data_direction = str(rows_direction).split('deg);"')
results = []
for j in range(len(data_wind)-1):
    wind = data_wind[j].split(')">')[1]
    gust = data_gust[j].split(')">')[1]
    temp = data_temp[j][-2:]
    direction = data_direction[j].split('transform:rotate(')[1]
    hour = data_hour[j].split('ts="')[1].split('"')[0]
    #print(wind,gust,direction,temp,hour)
    results.append([wind,gust,direction,temp,hour])

results_df = pd.DataFrame(results, columns = ['Wind','gust','Direction','Temperature','Time_milliseconds'])
results_df['Time_UTC'] = results_df['Time_milliseconds'].apply(lambda x: pd.to_datetime(x, unit='ms'))
results_df = results_df.set_index('Time_UTC')
display(results_df)
# %%
