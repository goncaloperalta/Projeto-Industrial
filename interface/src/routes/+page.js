
export const load = async ({fetch}) => {
    let url = "http://localhost:8000/"
    if(typeof document != "undefined"){
        url = `http://${window.location.hostname}:8000/`
    }

    const fetchProfiles = async () => {
        const res = await fetch(url + "get-profiles");
        const data = await res.json();

        return data.profiles.profile;
    }    
    const profile = await fetchProfiles();

    const fetchLastTest = async () => {
        const res = await fetch(url + "get-last-test");
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
