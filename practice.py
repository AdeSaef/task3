import requests

api_key ='2c20153b-293a-41ba-92c2-77ad2d0e4407'
word='potato'
url=f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}'

res = requests.get(url)

definitions = res.json()

for definition in definitions:
    print(definition)