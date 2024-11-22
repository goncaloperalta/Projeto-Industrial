<script>
    import LinePlot from "./LinePlot.svelte";
    import PieChart2 from "./statistics/PieChart2.svelte";

    let presets = {
        rb: { pressTime: 1, ntimes: 10, maxForce: 1, interval: 5 },
        fr: { pressTime: 2, ntimes: 5, maxForce: 1, interval: 6 },
        wps_info: { pressTime: 3, ntimes: 15, maxForce: 4, interval: 3 },
        on: { pressTime: 1, ntimes: 15, maxForce: 5, interval: 3 }
    };
    let profiles = [];
    let profilesCounter = 0;

    let val = ''; // Set to empty so "Select..." appears initially
    let results = 0;
    let readings = {};

    // Computed values based on selection - in Select... shows an empty string ' '
    $: presetValues = val === 'rb' || val === 'fr' || val === 'wps_info' || val === 'on' 
        ? { ...presets[val] }
        : val.includes('profile') ? {...profiles[Number(val.charAt(val.length-1))-1]}
        : { pressTime: '', ntimes: '', maxForce: '', interval: '' };

    function saveProfile(){
        if(!val.includes('profile')){
            profiles.push(presetValues)
            profilesCounter += 1;
        }
    }

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
    let successRate = 90;
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
            <select id="testType" bind:value={val} class="bg-gray-50 border border-gray-300 dark:bg-slate-600 dark:border-slate-600 rounded-lg p-2.5 text-center">
                <option value="">Select...</option>
                <option value="rb">Reset (Reboot)</option>
                <option value="fr">Factory Reset</option>
                <option value="wps_info">WPS/Info</option>
                <option value="on">On</option>
                {#key profilesCounter}
                    {#each profiles as profile, index}
                        <option value="profile{index+1}">Profile {index+1}</option>
                    {/each}
                {/key}
            </select>
        </div>

        <!-- Input Fields for Test Parameters -->
        <div class="mt-2">
            <label for="pressTime" class="text-sm font-medium">Button press time (sec): </label>
            <input type="number" id="pressTime" bind:value={presetValues.pressTime} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-600 dark:border-slate-600 dark:outline-none">
        </div>
        <div class="mt-2">
            <label for="ntimes" class="text-sm font-medium">Number of times to be pressed: </label>
            <input type="number" id="ntimes" bind:value={presetValues.ntimes} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-600 dark:border-slate-600 dark:outline-none">
        </div>
        <div class="mt-2">
            <label for="maxForce" class="text-sm font-medium">Maximum force to apply (N): </label>
            <input type="number" id="maxForce" bind:value={presetValues.maxForce} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-600 dark:border-slate-600 dark:outline-none">
        </div>
        <div class="mt-2">
            <label for="interval" class="text-sm font-medium">Interval between actuations (sec): </label>
            <input type="number" id="interval" bind:value={presetValues.interval} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full dark:bg-slate-600 dark:border-slate-600 dark:outline-none">
        </div>

        <!-- Start Button -->
        <div class="flex justify-center">
            <div class="mt-10">
                <button on:click={showResults} class="bg-[#DA8359] px-10 py-2 text-gray-700 font-bold rounded-lg hover:bg-[#b86d48] transition-all dark:bg-slate-500 dark:hover:bg-slate-400 dark:text-white">Start</button>
            </div>
            <div class="mt-10 ml-auto">
                <button on:click={saveProfile} class="bg-[#DA8359] px-10 py-2 text-gray-700 font-bold rounded-lg hover:bg-[#b86d48] transition-all dark:bg-slate-500 dark:hover:bg-slate-400 dark:text-white">Save </button>
            </div>        
        </div>
        
    </div>
</div>

<!-- Results Section -->
{#if results}
    <div id="results-section" class="bg-[#ECDFCC] text-[#111827] min-h-screen flex items-center justify-center flex-col dark:bg-slate-800 dark:text-white">
        <div class="text-center p-10 bg-white shadow-lg rounded-lg w-3/4 dark:bg-slate-700">
            <h2 class="text-2xl mb-5">Results</h2>
            <div class="flex justify-around">
                {#await readings}
                    <p class="m-auto text-2xl">Pressing the button...</p>
                {:then readings}
                    <div>
                        <LinePlot X={readings.sensor.time} Y={readings.sensor.val} />
                    </div>
                    <div class="w-1/2 block">
                        {readings.but_feedback}
                    </div>
                {/await}
            </div>
        </div>
    </div>
{/if}