
export const GET = async () => {
    const res = await fetch("http://localhost:8000/start")
    const data = await res.json()

    print(data)

    return new Response(JSON.stringify({message: "device added"}), {status: 201})
}