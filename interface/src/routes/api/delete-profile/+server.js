import Database from "better-sqlite3"

const db = new Database('app.db')
db.pragma('journal_mode = WAL')

export const DELETE = async ({request}) => {
    const body = await request.json();
    const deleteData = db.prepare("DELETE FROM profiles WHERE pName = ?");
    deleteData.run(body.pName);

    return new Response(JSON.stringify({message: "profile removed"}), {status: 200})
}