<script>
    import LinePlot from "./LinePlot.svelte";
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

<nav class="bg-white border-gray-200 dark:bg-gray-900">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Home</span>
        <button data-collapse-toggle="navbar-default" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-default" aria-expanded="false">
            <span class="sr-only">Open main menu</span>
            <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
            </svg>
        </button>
        <div class="hidden w-full md:block md:w-auto" id="navbar-default">
            <ul class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
                <li>
                    <a href="/" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Home</a>
                </li>
                <li>
                    <a href="/history" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">History</a>
                </li>
                <li>
                    <a href="/statistics" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Statistics</a>
                </li>
                <li>
                    <a href="/about" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">About</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

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