const express = require("express");
const database = require("better-sqlite3");
const cors = require('cors');
const port = 3000;

const app = express();
app.use(express.json());
app.use(cors());
const db = new database("app.db");

app.get('/', (req, res) => {
    const query = "SELECT * FROM devices";
    const devices = db.prepare(query).all();
    res.json({devices: devices});
});

app.post('/add-device', (req, res) => {
    console.log(req.body);
    const data = req.body;
    const insertData = db.prepare("INSERT INTO devices (model, success, button1, button2, date, time) VALUES (?, ?, ?, ?, ?, ?)");
    insertData.run(data.model, data.success, data.button1, data.button2, data.date, data.time);

    res.send({
        mesage: "New device added to the database",
    });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

// `
//     CREATE TABLE devices (
//         model VARCHAR(255) PRIMARY KEY UNIQUE,
//         success INT,
//         button1 INT,
//         button2 INT,
//         date DATE,
//         time TIME
//     )
// `
// db.exec(query);
