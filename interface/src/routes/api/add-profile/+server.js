import Database from "better-sqlite3"

const db = new Database('app.db');
db.pragma('journal_mode = WAL');

export const POST = async ({request}) => {
    const body = await request.json();
    const insertData = db.prepare("INSERT INTO profiles (pName, pressTime, nTimes, interval) VALUES (?, ?, ?, ?)");
    insertData.run(body.pName, body.pressTime, body.nTimes, body.interval);
    
    const query = "SELECT * FROM profiles";
    const profiles = db.prepare(query).all();

    return new Response(JSON.stringify({profiles: profiles}), {status: 201});
}