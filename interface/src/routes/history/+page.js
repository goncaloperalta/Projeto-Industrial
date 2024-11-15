
export const load = async ({fetch}) => {
    const fetchDevices = async () => {
        const res = await fetch('/api')
        const data = await res.json()
        return data.devices
    }

    const devices = await fetchDevices();
    return {
        devices
    }
}