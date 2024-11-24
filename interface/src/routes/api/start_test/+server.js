
export const GET = async () => {
    const res = await fetch("http://localhost:8000/start", { signal: AbortSignal.timeout(10000) })
    const data = await res.json()
   
    return new Response(JSON.stringify({data: data}), {status: 201})
}