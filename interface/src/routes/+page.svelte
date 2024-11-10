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

<TopBar tabName="Home" />

<div class="bg-slate-800 grid grid-cols-2 gap-4 content-start h-screen">
    <div class="text-white inline-block align-middle p-20 text-center">
        Start a Test
        <br>
        <div class="mt-5">
            <label for="testType" class="mb-2 text-sm font-medium text-gray-900 dark:text-white">Presets: </label>
            <select id="testType" bind:value={val} class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                <option selected value="rb">Choose a type of test</option>
                <option value="rb">Reset (Reboot)</option>
                <option value="fr">Factory Reset</option>
                <option value="wps">WPS</option>
                <option value="inf">Info</option>
            </select>
        </div>
        <div class="flex justify-between">
            <label for="testType" class=" mt-auto mb-auto text-sm font-medium text-gray-900 dark:text-white">Button press time (sec): </label>
            <input type="number" value={presets[val].pressTime} class="bg-gray-50 text-right border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        </div>
        <div class="flex justify-between">
            <label for="testType" class=" mt-auto mb-auto text-sm font-medium text-gray-900 dark:text-white">Number of times to be pressed: </label>
            <input type="number" value={presets[val].ntimes} class="bg-gray-50 text-right border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        </div>
        <div class="flex justify-between">
            <label for="testType" class=" mt-auto mb-auto text-sm font-medium text-gray-900 dark:text-white">Maximum force to apply (N): </label>
            <input type="number" value={presets[val].maxForce} class="bg-gray-50 text-right border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        </div>
        <div class="flex justify-between">
            <label for="testType" class=" mt-auto mb-auto text-sm font-medium text-gray-900 dark:text-white">Interval between actuations (sec): </label>
            <input type="number" value={presets[val].interval} class="bg-gray-50 text-right border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        </div>
        <div class=" mt-auto mb-auto flex float-right">
            <button on:click={showResults} class=" bg-slate-500 w-52 h-10 mt-10 rounded-lg hover:bg-slate-600 transition-all">Start</button>
        </div>
        
    </div>


    <div class="text-white inline-block align-middle p-20 text-center">
        <div>
            Results
        </div>
        <div class="inline-block align-middle">
            {#if results == 1}
                <LinePlot />
            {/if}
        </div>
    </div>
</div>