
export const load = async ({fetch}) => {
    const fetchTests = async () => {
        const res = await fetch('/api/get-tests');
        const data = await res.json();
        
        return data.tests;
    }
    
    const tests = await fetchTests();
    return {
        tests
    };
}