import requests
import json

url = "http://127.0.0.1:5000/projectpost"

payload = json.dumps({
  "name": "nname",
  "countrycode": "CC8",
  "district": "disn",
  "population": 800000
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
