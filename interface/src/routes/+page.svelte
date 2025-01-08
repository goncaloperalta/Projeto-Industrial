<script>
    import { onMount } from "svelte";
    import LinePlot from "./LinePlot.svelte";

    let {data} = $props();

    onMount(() => {
        setInterval(refreshLastTest, 10000);
    })

    let profiles = $state(data.profile);
    let ind = $state(0);
    let lastTest = $state(data.lastTest);
    let len = $derived(lastTest.time_val.length);
    let selected = $state(0);
    let currentProfile = $state(data.profile[0]);
    let showProfileInputName = $state(0);
    let profileName = $state('');
    function changeToCustom(){
        if(selected != 0){
            selected = 0;
        }
    }
    function selectChanges(){
        currentProfile = data.profile[selected];
    }
    async function saveProfile(){
        if(selected == 0){
            showProfileInputName = !showProfileInputName;
            if(profileName && showProfileInputName == 0){
                await fetch("http://192.168.43.97:8000/add-profile", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        pName: profileName,
                        pressTime: Number(currentProfile.pressTime),
                        nTimes: Number(currentProfile.nTimes),
                        interval: Number(currentProfile.interval)
                    })
                });
                
                const res = await fetch("http://192.168.43.97:8000/get-profiles");
                const json = await res.json();
                profiles = json.profiles.profile;
                data = json.profiles;
            }
        }
    }
    async function deleteProfile(){
        if(selected != 0){
            await fetch("http://192.168.43.97:8000/delete-profile", {
                method: "DELETE",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    pName: currentProfile.pName
                })
            });

            const res = await fetch("http://192.168.43.97:8000/get-profiles");
            const json = await res.json();
            profiles = json.profiles.profile;
            data = json.profiles;
            selected = 0;
        }
    }

    let results = $state(0);
    let readings = $state(0);
    async function showResults(){
        if(!isNumber(currentProfile.pressTime) || currentProfile.pressTime < 0){
            alert("Button press time must be a positive number");
            return;
        }
        if(!isNumber(currentProfile.nTimes) || currentProfile.nTimes < 1){
            alert("Number of times to be pressed must be a number greater than one");
            return;
        }
        if(!isNumber(currentProfile.interval) || currentProfile.interval < 0){
            alert("Interval between actions must be a positive number");
            return;
        }

        let params = currentProfile;
        readings = startTest(params);
        
        setTimeout(() => {
            document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
        }, 0);
    }

    async function startTest(params){
        await fetch('http://192.168.43.97:8000/start', {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                pressTime: Number(params.pressTime),
                nTimes: Number(params.nTimes),
                interval: Number(params.interval)
            }),
            signal: AbortSignal.timeout(10000)
        });

        const response = await fetch('http://192.168.43.97:8000/get-last-test');
        const json = response.json();

        return json;
    }

    function isNumber(n){
        if(typeof n == 'number'){
            return true;
        }
        return false;
    }

    async function refreshLastTest(){
        const res = await fetch('http://192.168.43.97:8000/get-last-test');
        const data = await res.json();

        lastTest = data;
        lastTest.success = JSON.parse(lastTest.success);
        lastTest.force_val = JSON.parse(lastTest.force_val);
        lastTest.time_val = JSON.parse(lastTest.time_val);
    }    
</script>

<!-- Title Container -->
<div class="fixed top-0 left-50 w-full text-#333 text-center p-4 z-10 dark:text-white">
    <h1 class="text-3xl font-normal">Button testing web interface and platform</h1>
</div>

<!-- Centered Test Prompt -->
<div class="bg-[#ECDFCC] text-[#111827] min-h-screen flex items-center justify-center dark:bg-slate-800 dark:text-white">
    <div class="flex items-center bg-slate-600 rounded-lg shadow-lg">
        <div class="text-center p-10 bg-white dark:bg-slate-600 rounded-lg">
            <h2 class="text-2xl mb-5">Define the test</h2>
            
            <!-- Test Type Selection -->
            <div class="mt-5 flex flex-col items-center ">
                <label for="testType" class="text-gray-300">Profiles </label>
                <select id="testType" bind:value={selected} onchange={selectChanges} class="bg-gray-50 border border-gray-300 dark:bg-slate-500 dark:border-slate-500 rounded-lg p-2.5 text-center">
                    {#key profiles}
                        {#each profiles as profile, index}
                            <option value="{index}">{profile.pName}</option>
                        {/each}
                    {/key}
                </select>
            </div>

            <!-- Input Fields for Test Parameters -->
            <div class="mt-2">
                <label for="pressTime" class="text-gray-300">Button press time (sec) </label>
                <input type="number" id="pressTime" onchange={changeToCustom} bind:value={currentProfile.pressTime} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-500 dark:border-slate-500 dark:outline-none">
            </div>
            <div class="mt-2">
                <label for="ntimes" class="text-gray-300">Number of times to be pressed </label>
                <input type="number" id="ntimes" onchange={changeToCustom} bind:value={currentProfile.nTimes} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-500 dark:border-slate-500 dark:outline-none">
            </div>
            <div class="mt-2">
                <label for="interval" class="text-gray-300">Interval between actuations (sec) </label>
                <input type="number" id="interval" onchange={changeToCustom} bind:value={currentProfile.interval} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-500 dark:border-slate-500 dark:outline-none">
            </div>
            
            <div class="w-full my-3">
                <hr class="bg-gray-900">
            </div>

            <!-- Start Button -->
            <div class="text-center">
                <span>
                    <button onclick={showResults} class="bg-[#DA8359] w-[8.5rem] py-2 text-gray-700 font-bold rounded-lg hover:bg-[#b86d48] transition-all dark:bg-slate-500  dark:hover:bg-slate-400 dark:text-white">Start</button>
                </span>
                <span>
                    <button onclick={saveProfile} class="bg-[#DA8359] w-[8.5rem] py-2 text-gray-700 font-bold rounded-lg hover:bg-[#b86d48] transition-all dark:bg-slate-500  dark:hover:bg-slate-400 dark:text-white">Save</button>
                </span>
                <span>
                    <button onclick={deleteProfile} class="bg-[#DA8359] w-[8.5rem] py-2 text-gray-700 font-bold rounded-lg hover:bg-[#b86d48] transition-all dark:bg-slate-500  dark:hover:bg-slate-400 dark:text-white">Delete</button>
                </span>
            </div>

            {#if showProfileInputName}
                <div class="mt-10">
                    <div>Enter a Name for the profile and press save again:</div>
                    <input bind:value={profileName} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-600 dark:border-slate-600 dark:outline-none">
                </div>
            {/if}
        </div>
        <div class=" border border-slate-800 h-96 rounded-lg"></div>
        <div class=" bg-slate-600 ml-10 text-center rounded-lg">
            <div class="mt-10">
                <span class="text-2xl m-auto">Last Test  <button onclick={refreshLastTest} class="hover:bg-slate-900 transition-all rounded-lg">&#8634;</button></span>
                <select name="graph-number" bind:value={ind} class="bg-gray-50 border border-gray-300 dark:bg-slate-500 dark:border-slate-500 rounded-lg p-2.5 text-center">
                    {#each lastTest.time_val as e, index}
                        <option value="{index}">{index+1}</option>
                    {/each}
                </select>
            </div>
            <div>
                Button: {lastTest.button}; Success: [{lastTest.success}] <br>
                Date: {lastTest.date}; Time: {lastTest.time}
            </div>
            {#key ind}
                <div>
                    <LinePlot X={lastTest.time_val[ind]} Y={lastTest.force_val[ind]}/>
                </div>
            {/key}
        </div>
    </div>
</div>
