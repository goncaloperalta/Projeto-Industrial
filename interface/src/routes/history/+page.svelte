<script>
    import LinePlot from "../LinePlot.svelte";
    import PieChart2 from "../statistics/PieChart2.svelte";
	
	export let data;

	let posts = data.devices;
	let filteredQuery = posts;

	let searchQuery = '';
	let fromDate = '';
	let toDate = '';
	function search(){
		filteredQuery = posts.filter(post => {
			let model = post.model.toLowerCase();
			let modelfilter = model.includes(searchQuery.toLowerCase())
			if(fromDate != '' && toDate != ''){
				modelfilter = modelfilter && ((post.date >= fromDate && post.date <= toDate) ? 1 : 0)
			}
			return modelfilter
		})
	}

	let shDetails = -1;
	function showDetails(ind){
		if(shDetails != ind){
			shDetails = ind
		} else{
			shDetails = -1;
		}
	}
</script>

<main class="bg-[#ECDFCC] min-h-screen text-[#111827] dark:bg-slate-800 dark:text-white">
	<div class="text-center block">
		<div class="p-20 text-3xl">
			History
		</div>
		<div class="text-center block">
			<div class="flex w-3/4 m-auto h-10 bg-[#DA8359] text-gray-200 rounded-sm shadow-2xl dark:bg-slate-500">
				<svg class=" w-10 h-5 mt-auto mb-auto ml-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
					<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
				</svg>
				<input bind:value={searchQuery} oninput={search} placeholder="Search for model" class="bg-[#DA8359] outline-none placeholder-gray-200 w-full rounded-sm dark:bg-slate-500">
				<span class="m-auto">From:</span>
				<input bind:value={fromDate} oninput={search} type="date" class="bg-[#DA8359] ml-1 dark:bg-slate-500">
				<span class="m-auto ml-5">To:</span>
				<input bind:value={toDate} oninput={search} type="date" class="bg-[#DA8359] ml-1 mr-2 dark:bg-slate-500">
			</div>

			<table class="w-3/4 mt-5 transparent m-auto p-10 table-fixed">
				<thead class="text-white">
					<tr class="bg-[#DA8359] h-12 dark:bg-slate-700">
						<th scope="col">MODEL</th>
						<th scope="col">SUCCESS</th>
						<th scope="col">DATE</th>
					</tr>
				</thead>
				<tbody class="border-b">
					{#each filteredQuery as post, index}
						<tr onclick={() => showDetails(index)} class="h-12 border-b border-gray-700 hover:bg-slate-700 transition-all cursor-pointer">
							<td>{post.model}</td>
							<td>
								{#if post.success == 1}
									<span class="bg-[#aac597] p-1 pl-4 pr-4 rounded-sm dark:bg-green-500">Yes</span>
								{:else}
									<span class="bg-[#ef6d80] p-1 pl-4 pr-4 rounded-sm dark:bg-red-500">No</span>
								{/if}
							</td>
							<td>{post.date}</td>
						</tr>
						{#if shDetails == index}
							<tr>
								<td colspan="3">
									<div class="flex justify-start h-[500px] pl-20">
										<!-- Smaller square box for gateway information -->
										<div class="ml-20 mr-20 gateway-info-box mt-auto mb-auto dark:bg-slate-700">
											<ul class="info-list">
												<li>CPU: 2.4GHz</li>
												<li>RAM: 6GB</li>
											</ul>
										</div>
										
										<!-- Line plot with spacing applied via CSS above -->
										<div class="ml-20 mr-20 mt-20">
											<LinePlot X={[1, 2, 3, 4, 5]} Y={[1, 2, 3, 4, 5]}/>
										</div>
										
										<!-- Pie chart component -->
										<div class="ml-20 mr-20 mt-auto mb-auto">
											<PieChart2 successRate={92} />
										</div>
									</div>
								</td>
							</tr>
						{/if}
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</main>

<style>
    /* Styling for smaller square box */
    .gateway-info-box {
        background-color: #ffffff; /* White background */
        border-radius: 8px; /* Rounded corners */
        width: 150px; /* Fixed width to create a square */
        height: 150px; /* Fixed height to match width */
        padding: 15px; /* Inner padding for spacing */
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* Shadow effect */
        text-align: left; /* Left-align text */
        margin-right: 20px; /* Space between box and line plot */
        display: flex;
        align-items: center; /* Center content vertically */
        justify-content: center; /* Center content horizontally */
    }

    /* Adjust text inside the square box */
    .info-list li {
        color: #333; /* Text color */
        font-size: 0.9rem; /* Slightly smaller font size */
        margin-bottom: 5px;
    }
</style>