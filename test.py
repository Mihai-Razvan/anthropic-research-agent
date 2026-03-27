from bs4 import BeautifulSoup
import requests as req

url = 'https://www.reddit.com/r/learnpython/comments/1cs0u0t/beautiful_soup/'

response = req.get(url)
parser = BeautifulSoup(response.text, 'html.parser')
movies = parser.select('td.titleColumn a')
for m in movies:
    print(m.text)
