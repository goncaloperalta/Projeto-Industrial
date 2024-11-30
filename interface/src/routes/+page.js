
export const load = async ({fetch}) => {
    const fetchProfiles = async () => {
        const res = await fetch('/api/get-profiles')
        const data = await res.json()
        
        return data.profiles
    }
    
    const profiles = await fetchProfiles();
    return {
        profiles
    }
}