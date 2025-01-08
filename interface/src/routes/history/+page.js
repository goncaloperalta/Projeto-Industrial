
export const load = async ({fetch}) => {
    const fetchTests = async () => {
        const res = await fetch('http://192.168.43.97:8000/get-tests');
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
    }

    return {
        tests
    };
}