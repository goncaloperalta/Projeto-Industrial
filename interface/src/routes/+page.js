
export const load = ({fetch}) => {
    const fetchPosts = async () => {
        const res = await fetch('/api')
        const data = await res.json()
        return data.devices
    }

    return {
        devices: fetchPosts()
    }
}