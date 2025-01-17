<script>
    import { onDestroy } from "svelte";
    import LinePlot from "../lib/LinePlot.svelte";

    let {data} = $props();

    let setIntervalRef = setInterval(refreshLastTest, 5000);
    onDestroy(() => {
        clearInterval(setIntervalRef)
    })

    // ******************* Profiles System ******************
    let profiles = $state(data.profile);
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
                let res = await fetch("http://192.168.43.97:8000/add-profile", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        pName: profileName,
                        pressTime: Number(currentProfile.pressTime),
                        nTimes: Number(currentProfile.nTimes),
                        interval: Number(currentProfile.interval)
                    })
                });
                if(res.status == 400){
                    alert("A Profile with that name already exists")
                }
                
                res = await fetch("http://192.168.43.97:8000/get-profiles");
                const json = await res.json();
                profiles = json.profiles.profile;
                data = json.profiles;
            }
        } else{
            alert("The parameters for the new profile must be changed on the Custom profile")
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
        } else{
            alert("The Custom profile is needed on the system and cannot be deleted.");
        }
    }

    // ******************* Start Test system ******************
    let ind = $state(0);
    let lastTest = $state(data.lastTest);
    async function startTest(){
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
        await fetch('http://192.168.43.97:8000/start', {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                pressTime: Number(params.pressTime),
                nTimes: Number(params.nTimes),
                interval: Number(params.interval)
            })
        });
    }
    function isNumber(n){
        if(typeof n == 'number'){
            return true;
        }
        return false;
    }
    
    // ******************* Refresh Last test system ******************
    let updateLastTest = $state(0);
    async function refreshLastTest(){
        const res = await fetch('http://192.168.43.97:8000/get-last-test');
        const data = await res.json();
        if(lastTest != data){
            lastTest = data;
            lastTest.success = JSON.parse(lastTest.success);
            lastTest.force_val = JSON.parse(lastTest.force_val);
            lastTest.time_val = JSON.parse(lastTest.time_val);
            updateLastTest = !updateLastTest;
        }
    }    
</script>

<main class="min-h-screen bg-slate-800 text-white pb-20">
    <div class="text-center block">
        <div class="p-20 pb-10 text-3xl">Button testing web interface and platform</div>

        <div class="block lg:flex lg:items-center lg:justify-center bg-slate-800 text-white">
            <div class="lg:flex lg:items-center lg:bg-slate-600 rounded-lg shadow-lg h-fit w-fit mx-auto">
                <div class="text-center p-5 sm:p-10 bg-slate-600 rounded-lg">
                    <h2 class="text-2xl mb-5">Define the test</h2>
                    
                    <div class="mt-5 flex flex-col items-center ">
                        <label for="testType" class="text-gray-300">Profiles </label>
                        <select id="testType" bind:value={selected} onchange={selectChanges} class="border bg-slate-500 border-slate-500 rounded-lg p-2.5 text-center">
                            {#key profiles}
                                {#each profiles as profile, index}
                                    <option value="{index}">{profile.pName}</option>
                                {/each}
                            {/key}
                        </select>
                    </div>
        
                    <div class="mt-2">
                        <label data-tooltip="Time in seconds to keep the button pressed" for="pressTime" class="text-gray-300">Button press time (sec) </label>
                        <input type="number" id="pressTime" onchange={changeToCustom} bind:value={currentProfile.pressTime} class="text-center border text-sm rounded-lg p-2.5 w-full bg-slate-500 border-slate-500 outline-none">
                    </div>
                    <div class="mt-2">
                        <label data-tooltip="Number of times to press the button" for="ntimes" class="text-gray-300">Number of times to be pressed </label>
                        <input type="number" id="ntimes" onchange={changeToCustom} bind:value={currentProfile.nTimes} class="text-center border text-sm rounded-lg p-2.5 w-full bg-slate-500 border-slate-500 outline-none">
                    </div>
                    <div class="mt-2">
                        <label data-tooltip="Time in seconds wait after pressing a button (only makes sense for more than one press time)" for="interval" class="text-gray-300">Interval between actuations (sec) </label>
                        <input type="number" id="interval" onchange={changeToCustom} bind:value={currentProfile.interval} class="text-center border text-sm rounded-lg p-2.5 w-full bg-slate-500 border-slate-500 outline-none">
                    </div>
                    
                    <div class="w-full my-3">
                        <hr class="bg-gray-900">
                    </div>
        
                    <div class="text-center">
                        <span>
                            <button data-tooltip="Start the test with the above parameters" onclick={startTest} class="w-[8.5rem] py-2 font-bold rounded-lg transition-all bg-slate-500  hover:bg-slate-400 text-white">Start</button>
                        </span>
                        <span>
                            <button data-tooltip="Save the current profile. A text box will pop-up to insert it's name" onclick={saveProfile} class="w-[8.5rem] py-2 font-bold rounded-lg transition-all bg-slate-500  hover:bg-slate-400 text-white">Save</button>
                        </span>
                        <span>
                            <button data-tooltip="Delete the currently selected profile" onclick={deleteProfile} class="w-[8.5rem] py-2 font-bold rounded-lg transition-all bg-slate-500  hover:bg-slate-400 text-white">Delete</button>
                        </span>
                    </div>
        
                    {#if showProfileInputName}
                        <div class="mt-10">
                            <div>Enter a Name for the profile and press save again:</div>
                            <input bind:value={profileName} class="text-center border text-sm rounded-lg p-2.5 w-full bg-slate-500 border-slate-600 outline-none">
                        </div>
                    {/if}
                </div>
                
                <div class=" bg-slate-600 mt-10 lg:mt-0 p-5 sm:p-10 text-center rounded-lg">
                    {#key updateLastTest}
                        <div>
                            <span class="text-2xl m-auto">Last Test<button data-tooltip="Refresh" onclick={refreshLastTest} class="hover:bg-slate-900 transition-all ml-1 w-10 h-10 rounded-lg">&#8634;</button></span>
                            <select name="graph-number" bind:value={ind} class="bg-slate-500 border-slate-500 rounded-lg p-2 text-center">
                                {#each lastTest.time_val as _, index}
                                    <option value="{index}">{index+1}</option>
                                {/each}
                            </select>
                        </div>
                        <div>
                            <span>Button: {lastTest.button}</span>, <span data-tooltip="Success is '1' when a push was done and a feedback from a button was received, else is '0'">Success: [{lastTest.success}]</span> <br>
                            <span>Date: {lastTest.date}</span>, <span>Time: {lastTest.time}</span>
                        </div>
                            <div>
                                <LinePlot X={lastTest.time_val[ind]} Y={lastTest.force_val[ind]} W=400 H=350/>
                        </div>
                    {/key}
                </div>
            </div>
        </div>
    </div>
</main>
