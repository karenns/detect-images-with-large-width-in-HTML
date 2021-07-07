# Library
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import cssutils

# Functions
def isWideImage(soup):
    wideScreen = False
    for att in soup.find_all('div', id=re.compile('^attachment_') ):
        if ('alignleft' in att['class']) or ('alignright' in att['class']):
            # div example: <div id="attachment_215850" ...>
            div_style = cssutils.parseStyle(att["style"])
            width_arr = div_style.width.split("px")
            width = int(width_arr[0])
            if width > 850:
                wideScreen = True
    return wideScreen

def doRequest(row):
    wideScreen = False
    headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    
    url = row['url']
    try:
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        wideScreen = isWideImage(soup)
        if wideScreen:
            print(url)
            file = open('output.txt', 'a')
            output = [ url,'\n']
            file.writelines(output)
            file.close()
    except Exception as e: 
        print(e)
    return wideScreen
    

# Open CSV
df = pd.read_csv('input.csv', header=None)
df.columns = ['url']

# Make it smaller just for TESTING purposes
#df = df.loc[1:10]

# Open and clean the output file
file = open('output.txt', 'w+')
file.truncate(0) 

# Run the function
df.apply(doRequest, axis =1)

# The maximum width in characters of a column in the repr of a pandas data structure
# pd.set_option('display.max_colwidth', None)
# print(df)

