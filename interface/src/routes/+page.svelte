<script>
    import LinePlot from "./LinePlot.svelte";

    let {data} = $props();

    let profiles = $state(data.profiles);
    let selected = $state(0);
    let currentProfile = $state(profiles[0]);
    let showProfileInputName = $state(0);
    let profileName = $state('');
    function changeToCustom(){
        if(selected != 0){
            selected = 0;
        }
    }
    function selectChanges(){
        currentProfile = profiles[selected];
    }
    async function saveProfile(){
        if(selected == 0){
            showProfileInputName = !showProfileInputName;
            
            if(profileName && showProfileInputName == 0){
                await fetch("api/add-profile", {
                    method: "POST",
                    body: JSON.stringify({
                        pName: profileName,
                        pressTime: currentProfile.pressTime,
                        nTimes: currentProfile.nTimes,
                        interval: currentProfile.interval
                    })
                });

                const response = await fetch("api/get-profiles");
                const json = await response.json();
                profiles = json.profiles;
            }
        }
    }
    async function deleteProfile(){
        if(selected != 0){
            await fetch("api/delete-profile", {
                method: "DELETE",
                body: JSON.stringify({
                    pName: currentProfile.pName
                })
            });

            const response = await fetch("api/get-profiles");
            const json = await response.json();
            profiles = json.profiles;
        }
    }

    let results = $state(0);
    let readings = $state(0);
    function showResults(){
        results = 1;
        readings = getReadings();
        setTimeout(() => {
            document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
        }, 0);
    }

    async function getReadings(){
        const res = await fetch('api/start_test', { signal: AbortSignal.timeout(10000) });
        const data = await res.json()

        return data.data
    }
</script>

<!-- Title Container -->
<div class="fixed top-0 left-50 w-full text-#333 text-center p-4 z-10 dark:text-white">
    <h1 class="text-3xl font-normal">Button testing web interface and platform</h1>
</div>

<!-- Centered Test Prompt -->
<div class="bg-[#ECDFCC] text-[#111827] min-h-screen flex items-center justify-center flex-col dark:bg-slate-800 dark:text-white">
    <div class="text-center p-10 bg-white dark:bg-slate-700 shadow-lg rounded-lg">
        <h2 class="text-2xl mb-5">Define the test</h2>
        
        <!-- Test Type Selection -->
        <div class="mt-5 flex flex-col items-center">
            <label for="testType" class="mb-2 text-sm font-medium text-center">Default Configurations: </label>
            <select id="testType" bind:value={selected} onchange={selectChanges} class="bg-gray-50 border border-gray-300 dark:bg-slate-600 dark:border-slate-600 rounded-lg p-2.5 text-center">
                {#key profiles}
                    {#each profiles as profile, index}
                        <option value="{index}">{profile.pName}</option>
                    {/each}
                {/key}
            </select>
        </div>

        <!-- Input Fields for Test Parameters -->
        <div class="mt-2">
            <label for="pressTime" class="text-sm font-medium">Button press time (sec): </label>
            <!-- svelte-ignore binding_property_non_reactive -->
            <input type="number" id="pressTime" onchange={changeToCustom} bind:value={currentProfile.pressTime} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-600 dark:border-slate-600 dark:outline-none">
        </div>
        <div class="mt-2">
            <label for="ntimes" class="text-sm font-medium">Number of times to be pressed: </label>
            <!-- svelte-ignore binding_property_non_reactive -->
            <input type="number" id="ntimes" onchange={changeToCustom} bind:value={currentProfile.nTimes} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-600 dark:border-slate-600 dark:outline-none">
        </div>
        <div class="mt-2">
            <label for="interval" class="text-sm font-medium">Interval between actuations (sec): </label>
            <!-- svelte-ignore binding_property_non_reactive -->
            <input type="number" id="interval" onchange={changeToCustom} bind:value={currentProfile.interval} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-600 dark:border-slate-600 dark:outline-none">
        </div>

        <!-- Start Button -->
        <div class="mt-5 text-center">
            <span>
                <button onclick={showResults} class="bg-[#DA8359] w-32 py-2 text-gray-700 font-bold rounded-lg hover:bg-[#b86d48] transition-all dark:bg-slate-500 dark:hover:bg-slate-400 dark:text-white">Start</button>
            </span>
            <span>
                <button onclick={saveProfile} class="bg-[#DA8359] w-32 py-2 text-gray-700 font-bold rounded-lg hover:bg-[#b86d48] transition-all dark:bg-slate-500 dark:hover:bg-slate-400 dark:text-white">Save</button>
            </span>
            <span>
                <button onclick={deleteProfile} class="bg-[#DA8359] w-32 py-2 text-gray-700 font-bold rounded-lg hover:bg-[#b86d48] transition-all dark:bg-slate-500 dark:hover:bg-slate-400 dark:text-white">Delete</button>
            </span>
        </div>

        {#if showProfileInputName}
            <div class="mt-10">
                <div>Enter a Name for the profile and press save again:</div>
                <input bind:value={profileName} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-600 dark:border-slate-600 dark:outline-none">
            </div>
        {/if}
    </div>
</div>

<!-- Results Section -->
{#if results}
    <div id="results-section" class="bg-[#ECDFCC] text-[#111827] min-h-screen flex items-center justify-center flex-col dark:bg-slate-800 dark:text-white">
        <div class="text-center p-10 bg-white shadow-lg rounded-lg w-3/4 dark:bg-slate-700">
            <h2 class="text-3xl mb-5">Results</h2>
            <div class="flex justify-around">
                {#await readings}
                    <p class="m-auto text-2xl">Pressing the button...</p>
                {:then readings}
                    <div class="w-1/2 align-middle text-xl m-auto ml-10">
                        <ul class="text-left">
                            <li><b><i>Button name:</i></b> {readings.feedback.button}</li>
                            <li><b><i>Success:</i></b> {readings.feedback.success}</li>
                        </ul>
                    </div>
                    <div>
                        <LinePlot X={readings.time_val} Y={readings.force_val} />
                    </div>
                {/await}
            </div>
        </div>
    </div>
{/if}