import requests

url = "https://www.sofascore.com/api/v1/event/14023951/statistics"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36 Edg/148.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1"
}

response = requests.get(url, headers=headers, timeout=30)

print("Status:", response.status_code)
print(response.text[:1000])
