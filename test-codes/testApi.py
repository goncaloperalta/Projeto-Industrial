import requests
url = 'http://localhost:8000/delete-profile'
headers = {
    "Content-type": "application/json"
}
body = {
    "pName": "Example"
}

res = requests.post(url, headers=headers, json=body)
print(res.text)