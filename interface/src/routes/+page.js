
export const load = async ({fetch}) => {
    const fetchProfiles = async () => {
        const res = await fetch('http://localhost:8000/get-profiles');
        const data = await res.json();

        return data.profiles.profile;
    }
    
    const profile = await fetchProfiles();
    return {
        profile
    };
}