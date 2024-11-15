import Database from "better-sqlite3"

const db = new Database('app.db')
db.pragma('journal_mode = WAL')

export const POST = async ({request}) => {
    const body = await request.json();
    const insertData = db.prepare("INSERT INTO devices (model, success, button1, button2, date, time) VALUES (?, ?, ?, ?, ?, ?)");
    insertData.run(body.model, body.success, body.button1, body.button2, body.date, body.time);

    return new Response(JSON.stringify({message: "device added"}), {status: 201})
}