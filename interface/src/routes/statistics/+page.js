
export const load = async ({fetch}) => {
    const fetchTests = async () => {
        const res = await fetch('http://10.42.0.1:8000/get-success')
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
