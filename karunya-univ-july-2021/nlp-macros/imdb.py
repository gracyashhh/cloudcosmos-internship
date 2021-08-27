import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/find?q=avatar'
page = requests.get(url)
print(page)
data = page.content

soup = BeautifulSoup(data,'html.parser')
print(soup)

#extracting link and text
result = soup.find('table',{'class':'findList'})
texts = result.find_all('td',{'class':'result_text'})

for r1 in texts:
    r2 = r1.find('a').text
    r3 = r1.find('a').get('href')
    link = url + r3
    print("Name:",r2)           #title of the link
    print("Link:",link)         #link
