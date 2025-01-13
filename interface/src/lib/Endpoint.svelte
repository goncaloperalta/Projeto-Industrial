<script>
    let { verb, endpoint, message, jsonReturn, code } = $props();
    
    let shDetails = $state(0);
    let arrow = $state('⮟');
    function details(){
        shDetails = !shDetails;
        if(arrow == '⮟'){
            arrow = '⮝';
        } else{
            arrow = '⮟';
        }
    }
    
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<div role="button" tabindex="0" onclick={details} class="bg-slate-700 flex h-12 rounded-sm my-3">
    <div class="w-24 rounded-sm flex {verb == "GET" ? "bg-teal-500" : verb == "POST" ? "bg-blue-600" : "bg-red-600"}"><div class="m-auto">{verb}</div></div>
    <div class="py-2 px-7"><code class="text-lg px-1 bg-gray-800 rounded-sm">{endpoint}</code></div>
    <div class="my-auto ml-auto pr-7">{arrow}</div>
</div>

{#if shDetails}
<div class="px-4 my-4">
    {message}
    <div class="bg-slate-900 my-4 rounded-md py-5 px-4">            
        <pre><code>{jsonReturn}</code></pre>
    </div>
    Sample <code class="px-1 bg-slate-900 rounded-sm">python</code> code:
    <div class="bg-slate-900 my-3 rounded-md py-5 px-4">
        <pre><div class="whitespace-pre-warp" id="codebox">{code}</div></pre>
    </div>
</div>
{/if}