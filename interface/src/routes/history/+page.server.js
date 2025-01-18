import os from 'os'

export const load = async ({fetch}) => {
    const fetchTests = async () => {
        const res = await fetch(`http://${os.hostname}:8000/get-tests-range`, {
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
        const res = await fetch(`http://${os.hostname}:8000/get-count`);
        const data = await res.json();

        return data.count;
    }
    const count = await fetchCount();

    return {
        tests,
        count
    };
}
