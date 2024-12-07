import Database from "better-sqlite3"

const db = new Database('app.db');
db.pragma('journal_mode = WAL');

export const GET = () => {
    const query = "SELECT * FROM tests";
    const tests = db.prepare(query).all();  
    
    return new Response(JSON.stringify({tests: tests}), {status: 200});
}