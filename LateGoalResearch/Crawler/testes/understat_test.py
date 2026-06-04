import requests

url = "https://understat.com/league/EPL/2024"

response = requests.get(url)

print(response.status_code)
print(response.text[:500])
