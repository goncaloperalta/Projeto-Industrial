<script>
    import LinePlot from "./LinePlot.svelte";
    import PieChart from "./PieChart.svelte";
    import TopBar from "./TopBar.svelte";
    
    let presets = {
        rb: { pressTime: 1, ntimes: 10, maxForce: 1, interval: 5 },
        fr: { pressTime: 2, ntimes: 5, maxForce: 1, interval: 6 },
        wps: { pressTime: 3, ntimes: 15, maxForce: 4, interval: 3 },
        inf: { pressTime: 4, ntimes: 15, maxForce: 4, interval: 3 }
    };

    let val = ''; // Set to empty so "Select..." appears initially
    let results = 0;

    // Computed values based on selection - in Select... shows an empty string ' '
    $: presetValues = val === 'rb' || val === 'fr' || val === 'wps' || val === 'inf' 
        ? { ...presets[val] }
        : { pressTime: '', ntimes: '', maxForce: '', interval: '' };

    // Calculate totalPresses and successfulPresses based on the selected test preset
    $: totalPresses = presetValues.ntimes || 0;
    $: successfulPresses = Math.floor(totalPresses * 0.87);  // 87% success rate assumption

    function showResults() {
        results = 1;
        setTimeout(() => {
            document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
        }, 0);
    }
</script>

<!-- Title Container -->
<div class="fixed top-0 left-50 w-full text-#333 text-center p-4 z-10">
    <h1 class="text-3xl font-normal">Button testing web interface and platform</h1>
</div>

<TopBar tabName="Home" />

<!-- Centered Test Prompt -->
<div class="bg-[#ECDFCC] text-[#111827] min-h-screen flex items-center justify-center flex-col">
    <div class="text-center p-10 bg-white shadow-lg rounded-lg">
        <h2 class="text-2xl mb-5">Define the test</h2>
        
        <!-- Test Type Selection -->
        <div class="mt-5 flex flex-col items-center">
            <label for="testType" class="mb-2 text-sm font-medium text-center">Default Configurations: </label>
            <select id="testType" bind:value={val} class="bg-gray-50 border border-gray-300 rounded-lg p-2.5 text-center">
                <option value="">Select...</option>
                <option value="rb">Reset (Reboot)</option>
                <option value="fr">Factory Reset</option>
                <option value="wps">WPS</option>
                <option value="inf">Info</option>
            </select>
        </div>

        <!-- Input Fields for Test Parameters -->
        <div class="mt-2">
            <label for="pressTime" class="text-sm font-medium">Button press time (sec): </label>
            <input type="number" id="pressTime" bind:value={presetValues.pressTime} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full">
        </div>
        <div class="mt-2">
            <label for="ntimes" class="text-sm font-medium">Number of times to be pressed: </label>
            <input type="number" id="ntimes" bind:value={presetValues.ntimes} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full">
        </div>
        <div class="mt-2">
            <label for="maxForce" class="text-sm font-medium">Maximum force to apply (N): </label>
            <input type="number" id="maxForce" bind:value={presetValues.maxForce} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full">
        </div>
        <div class="mt-2">
            <label for="interval" class="text-sm font-medium">Interval between actuations (sec): </label>
            <input type="number" id="interval" bind:value={presetValues.interval} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full">
        </div>

        <!-- Start Button -->
        <div class="mt-10">
            <button on:click={showResults} class="bg-[#DA8359] px-10 py-2 text-gray-700 font-bold rounded-lg hover:bg-[#b86d48] transition-all">Start</button>
        </div>
    </div>
</div>

<!-- Results Section -->
{#if results}
    <div id="results-section" class="bg-[#ECDFCC] text-[#111827] min-h-screen flex items-center justify-center flex-col">
        <div class="text-center p-10 bg-white shadow-lg rounded-lg w-3/4">
            <h2 class="text-2xl mb-5">Results</h2>
            <div class="flex justify-around">
                <div class="w-1/2 p-4">
                    <LinePlot />
                </div>
                <div class="w-1/2 p-4">
                    <PieChart {totalPresses} {successfulPresses}/>
                </div>
            </div>
        </div>
    </div>
{/if}