import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import openpyxl


#link pattern to distinguish if row value is a link
link_pattern = re.compile(r'https?://\S+')

#read excell file
df = pd.read_excel('input.xlsx')
name_column = df['Location']


#Create worksheet and name the frist column
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet["A1"] = "Location"

#read every row in excell file
for i in range(len(name_column)):
    row_value = name_column.iloc[i]
    worksheetrow = 'A'+str(i+2)
    try:
        if link_pattern.match(row_value):
            parts = row_value.split('/')
            last_part = parts[-1]
            number = last_part.split('+')
            latitude = number[0]
            longitude = number[1]
            url = 'https://www.google.com/maps/search/?api=1&query='+latitude+','+longitude
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            street_name = soup.find('span', class_='GLOBAL__gm2-headline-5').text
            worksheet[worksheetrow] = street_name
    except:
        continue

workbook.save("output.xlsx")