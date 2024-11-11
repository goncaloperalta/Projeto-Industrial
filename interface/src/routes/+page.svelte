<script>

    import LinePlot from "./LinePlot.svelte";
    import TopBar from "./TopBar.svelte";
    let presets = {
        rb: { pressTime: 1, ntimes: 1, maxForce: 1, interval: 1 },
        fr: { pressTime: 2, ntimes: 2, maxForce: 2, interval: 2 },
        wps: { pressTime: 3, ntimes: 3, maxForce: 3, interval: 3 },
        inf: { pressTime: 4, ntimes: 4, maxForce: 4, interval: 4 }
    }
    let val = 'rb';
    let results = 0;
    function showResults(){
        results = 1;
    }
</script>

<!-- Title Container -->
<div class="fixed top-0 left-50 w-full text-#333 text-center p-4 z-10">
    <h1 class="text-3xl font-normal">Button testing web interface and platform</h1>
</div>

<TopBar tabName="Home" />

<!-- Centered Test Prompt -->
<div class="bg-[#ECDFCC] text-[#111827] min-h-screen flex items-center justify-center flex-col">
    <!-- Test Form Section -->
    <div class="text-center p-10 bg-white shadow-lg rounded-lg">
        <h2 class="text-2xl mb-5">Define the test</h2>
        
        <div class="mt-5 flex flex-col items-center">
            <label for="testType" class="mb-2 text-sm font-medium text-center">Default Configurations: </label>
            <select id="testType" bind:value={val} class="bg-gray-50 border border-gray-300 text-center rounded-lg p-2.5 text-center">
                <option selected value="rb">Select...</option>
                <option value="rb">Reset (Reboot)</option>
                <option value="fr">Factory Reset</option>
                <option value="wps">WPS</option>
                <option value="inf">Info</option>
            </select>
        </div>

        <!-- Input Fields for Test Parameters -->
        <div class="mt-2">
            <label for="pressTime" class="text-sm font-medium">Button press time (sec): </label>
            <input type="number" id="pressTime" value={presets[val].pressTime} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full">
        </div>
        <div class="mt-2">
            <label for="ntimes" class="text-sm font-medium">Number of times to be pressed: </label>
            <input type="number" id="ntimes" value={presets[val].ntimes} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full">
        </div>
        <div class="mt-2">
            <label for="maxForce" class="text-sm font-medium">Maximum force to apply (N): </label>
            <input type="number" id="maxForce" value={presets[val].maxForce} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full">
        </div>
        <div class="mt-2">
            <label for="interval" class="text-sm font-medium">Interval between actuations (sec): </label>
            <input type="number" id="interval" value={presets[val].interval} class="bg-gray-50 text-center border border-gray-300 text-sm rounded-lg p-2.5 w-full">
        </div>

        <!-- Start Button -->
        <div class="mt-10">
            <button on:click={showResults} class="bg-[#DA8359] text-gray-700 font-bold w-full h-10 rounded-lg hover:bg-[#b86d48] transition-all">Start</button>
        </div>
    </div>
</div>

<!-- Results Section -->
{#if results}
    <div class="bg-[#ECDFCC] text-[#111827] min-h-screen flex items-center justify-center flex-col transition-transform duration-500 ease-in-out transform translate-y-0">
        <div class="text-center p-10 bg-white shadow-lg rounded-lg w-3/4">
            <h2 class="text-2xl mb-5">Results</h2>
            <LinePlot />
        </div>
    </div>
{/if}