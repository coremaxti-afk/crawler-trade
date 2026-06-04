import requests
import re

url = "https://understat.com/league/EPL/2024"

html = requests.get(url).text

print("Tamanho HTML:", len(html))

matches = re.findall(r"JSON\.parse\('(.*?)'\)", html)

print("Blocos encontrados:", len(matches))

for i, item in enumerate(matches):
    print(f"\nBloco {i+1}")
    print(item[:300])
