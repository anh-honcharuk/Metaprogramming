import requests
from  bs4 import BeautifulSoup as BS
'''
r = requests.get('https://multiplex.ua/cinema/kyiv/tsum')
html2 = BS(r.content, 'html.parser')

item = html2.find_all('a', class_='title')
print(item)
item = set(item)
links = []
for link in item:
    links.append(link.get('href'))
    print(link.get('href'))

for i in range(len(links)):
    rq = requests.get('https://multiplex.ua' + links[i])
    html1 = BS(rq.content, 'html.parser')
    #<h1 id="mvi_title">
    item2 = html1.find_all('h1', id='mvi_title')
    print(item2[0].get_text())
'''
print('-----------------')
req = requests.get('https://multiplex.ua/cinema/kyiv/tsum')
htmlka = BS(req.content, 'html.parser')

for l in htmlka.select(".cinema_inside"):
    title = l.find_all('div', class_ = 'title')
    print(title)







