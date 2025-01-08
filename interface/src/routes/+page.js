
export const load = async ({fetch}) => {
    const fetchProfiles = async () => {
        const res = await fetch('http://192.168.43.97:8000/get-profiles');
        const data = await res.json();

        return data.profiles.profile;
    }
    
    const profile = await fetchProfiles();
    return {
        profile
    };
}