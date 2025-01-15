
export const load = async ({fetch}) => {
    const fetchProfiles = async () => {
        const res = await fetch('http://10.42.0.1:8000/get-profiles');
        const data = await res.json();

        return data.profiles.profile;
    }    
    const profile = await fetchProfiles();

    const fetchLastTest = async () => {
        const res = await fetch('http://10.42.0.1:8000/get-last-test');
        const data = await res.json();

        return data;
    }
    const lastTest = await fetchLastTest();
    lastTest.success = JSON.parse(lastTest.success);
    lastTest.parameters = JSON.parse(lastTest.parameters);
    lastTest.force_val = JSON.parse(lastTest.force_val);
    lastTest.time_val = JSON.parse(lastTest.time_val);

    return {
        profile,
        lastTest
    };
}
