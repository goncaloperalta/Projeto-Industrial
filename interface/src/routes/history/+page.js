
export const load = async ({fetch}) => {
    let url = "http://localhost:8000/"
    if(typeof document != "undefined"){
        url = `http://${window.location.hostname}:8000/`
    }

    const fetchTests = async () => {
        const res = await fetch(url + "get-tests-range", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                size: 10,
                offset: 0
            })
        });
        const data = await res.json();
        
        return data.tests.test;
    }
    
    const tests = await fetchTests();
    for(let i = 0; i < tests.length; i++){
        let timeVal = JSON.parse(tests[i].time_val);
        let forceVal = JSON.parse(tests[i].force_val);
        
        for(let j = 0; j < timeVal.length; j++){
            tests[i].time_val = timeVal;
            tests[i].force_val = forceVal;
        }

        tests[i].success = JSON.parse(tests[i].success);
        tests[i].parameters = JSON.parse(tests[i].parameters);
    }

    const fetchCount = async () => {
        const res = await fetch(url + "get-count");
        const data = await res.json();

        return data.count;
    }
    const count = await fetchCount();

    return {
        tests,
        count
    };
}
