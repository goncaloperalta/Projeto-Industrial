import requests

device = {
    "model": "1111",
    "success": 0,
    "button1": 33,
    "button2": 12,
    "date": "2023-9-21",
    "time": "15:33:00"
};

requests.post('http://localhost:3000/add-device', json=device)
