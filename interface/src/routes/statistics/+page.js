
export const load = async ({fetch}) => {
    const fetchTests = async () => {
        const res = await fetch('http://localhost:8000/get-success')
        const data = await res.json()
        
        return data
    }
    
    const tests = await fetchTests();
    return {
        tests
    }
}