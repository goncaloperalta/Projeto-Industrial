<script>
    import { onDestroy, onMount } from "svelte";

    let status = 'Ready'
    let parameters = {
        "pressTime": 1,
        "nTimes": 1,
        "interval": 1,
    }

    let setIntervalRefTopBar = setInterval(refreshVars, 5000)
    onMount(() => {
        refreshVars()
    })

    onDestroy(() => {
        clearInterval(setIntervalRefTopBar)
    })
    
    async function refreshVars(){
        let res = await fetch("http://localhost:8000/get-status")
        status = await res.json()
        status = status.message

        res = await fetch("http://localhost:8000/get-current-parameters")
        parameters = await res.json()
    }

    async function abortTest(){
        const res = await fetch("http://localhost:8000/abort-test")
        if(res.status == 400){
            alert("Test has already finished")
        }
    }
</script>

<div class="bg-slate-700 m-auto left-0 sm:left-1/2 w-full sm:ml-[-37.5%] sm:rounded-md fixed sm:w-3/4 top-4 text-white">
    <div class="text-lg flex py-2 px-4">
        <div>
            <span>Status: </span> <span class="{status == 'Ready' ? 'text-teal-500' : status == 'Running a test' ? 'text-yellow-500' : 'text-red-500'}">●</span> <span>{status}</span>
            {#if status != 'Ready'}
                <button data-tooltip="Abort current test" onclick={abortTest} class="mx-2 text-md bg-red-600 px-2 rounded-sm">Abort</button>
                <span data-tooltip="Button Press time">BPT: {parameters.pressTime}</span> <span data-tooltip="Number of times to press">N: {parameters.currentRun}/{parameters.nTimes}</span> <span data-tooltip="Interval between presses">I: {parameters.interval}</span>
            {/if}
        </div>
        <button data-tooltip="Refresh" onclick={refreshVars} class="hover:bg-slate-900 ml-auto px-2 rounded-lg">&#8634;</button>
    </div>
</div>
