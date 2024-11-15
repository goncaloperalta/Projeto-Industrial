import Database from "better-sqlite3"

const db = new Database('app.db')
db.pragma('journal_mode = WAL')

export const GET = () => {
    const query = "SELECT * FROM devices"
    const devices = db.prepare(query).all()  
    
    return new Response(JSON.stringify({devices: devices}), {status: 200})
}