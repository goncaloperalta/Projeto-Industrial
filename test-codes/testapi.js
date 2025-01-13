
fetch("http://192.168.43.97:8000:8000/add-profile", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
        "pName": "INFO",
        "pressTime": 2,
        "nTimes": 4,
        "interval": 1
    })
}).then((res) => {
    res.json()
}).then((data) => {
    console.log(data)
})