import requests

device = {
    "model": "1111",
    "success": 0,
    "button1": 33,
    "button2": 12,
    "date": "2024-11-22",
    "time": "15:33:00"
};

requests.post('http://localhost:3000/add-device', json=device)
