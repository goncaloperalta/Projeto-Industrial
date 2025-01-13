<script>
    import { onMount } from "svelte";

    let status = 'Ready'
    let parameters = {
        "pressTime": 1,
        "nTimes": 1,
        "interval": 1,
    }
    refreshVars()

    onMount(() => {
        setInterval(refreshVars, 10000)
    })
    
    async function refreshVars(){
        let res = await fetch("http://192.168.43.97:8000:8000/get-status")
        status = await res.json()
        status = status.message

        res = await fetch("http://192.168.43.97:8000:8000/get-current-parameters")
        parameters = await res.json()
    }

    async function abortTest(){
        await fetch("http://192.168.43.97:8000:8000/abort-test")
    }
</script>

<div class="bg-slate-700 m-auto left-0 sm:left-1/2 w-full sm:ml-[-37.5%] sm:rounded-md fixed sm:w-3/4 top-4 text-white">
    <div class="text-lg flex py-2 px-4">
        <div>
            <span>Status: </span> <span class="{status == 'Ready' ? 'text-teal-500' : status == 'Running a test' ? 'text-yellow-500' : 'text-red-500'}">●</span> <span>{status}</span>
            {#if status != 'Ready'}
                <button onclick={abortTest} class="mx-2 text-md bg-red-600 px-2 rounded-sm">Abort</button>
                <span data-tooltip="Button Press time">BPT: {parameters.pressTime}</span> <span data-tooltip="Number of times to press">N: 1/{parameters.nTimes}</span> <span data-tooltip="Interval between presses">I: {parameters.interval}</span>
            {/if}
        </div>
        <button data-tooltip="Refresh" onclick={refreshVars} class="hover:bg-slate-900 ml-auto px-2 rounded-lg">&#8634;</button>
    </div>
</div>