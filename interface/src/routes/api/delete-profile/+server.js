import Database from "better-sqlite3"

const db = new Database('app.db');
db.pragma('journal_mode = WAL');

export const DELETE = async ({request}) => {
    const body = await request.json();
    const deleteData = db.prepare("DELETE FROM profiles WHERE pName = ?");
    deleteData.run(body.pName);

    const query = "SELECT * FROM profiles";
    const profiles = db.prepare(query).all();

    return new Response(JSON.stringify({profiles: profiles}), {status: 200});
}