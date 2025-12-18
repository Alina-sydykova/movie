import requests
import json

url = "https://openl-translate.p.rapidapi.com/translate"
headers = {
    'x-rapidapi-key': "21d339758emsh9a614fe90158b2cp136f6djsnbc8fdc6a54d3",
    'x-rapidapi-host': "openl-translate.p.rapidapi.com",
    'Content-Type': "application/json"
}
payload = {"target_lang": "ky", "text": "Hello world, how are you?"}

response = requests.post(url, headers=headers, json=payload)
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.json()}")