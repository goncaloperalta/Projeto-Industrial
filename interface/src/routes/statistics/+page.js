
export const load = async ({fetch}) => {
    let url = "http://localhost:8000/"
    if(typeof document != "undefined"){
        url = `http://${window.location.hostname}:8000/`
    }

    const fetchTests = async () => {
        const res = await fetch(url + "get-success")
        const data = await res.json()
        
        return data
    }
    
    const tests = await fetchTests();
    for(let i = 0; i < tests.length; i++){
        tests[i] = JSON.parse(tests[i]);
    }
    
    return {
        tests
    }
}
