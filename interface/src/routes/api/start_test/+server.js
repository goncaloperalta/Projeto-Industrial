import Database from "better-sqlite3"

const db = new Database('app.db');
// db.pragma('journal_mode = WAL');

export const POST = async ({request}) => {
    const body = await request.json();
    const res = await fetch("http://192.168.43.97:8000/start", {
        headers: {
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({pressTime: body.pressTime})
    });
    const data = await res.json();
    
    // console.log(data)
    const insertData = db.prepare("INSERT INTO tests (button, success, force_val, time_val, date, time) VALUES (?, ?, ?, ?, ?, ?)");
    insertData.run(data.feedback.button, data.feedback.success, JSON.stringify(data.force_val), JSON.stringify(data.time_val), data.date, data.time);

    return new Response(JSON.stringify({data: data}), {status: 201});
}
