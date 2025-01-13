<script>
    import LinePlot from "../../lib/LinePlot.svelte";
	
	export let data;

	let posts = data.tests;
	let filteredQuery = posts;

	let searchQuery = '';
	let fromDate = '';
	let toDate = '';
	function search(){
		filteredQuery = posts.filter(post => {
			let button = post.button.toLowerCase();
			let buttonfilter = button.includes(searchQuery.toLowerCase());
			if(fromDate != '' && toDate != ''){
				buttonfilter = buttonfilter && ((post.date >= fromDate && post.date <= toDate) ? 1 : 0);
			}
			return buttonfilter;
		})
	}

	let shDetails = -1;
	function showDetails(ind){
		if(shDetails != ind){
			shDetails = ind;
		} else{
			shDetails = -1;
		}
	}
</script>

<main class="min-h-screen bg-slate-800 text-white">
	<div class="text-center block">
		<div class="p-20 pb-10 text-3xl">
			History
		</div>
		<div class="m-auto flex sm:w-3/4 justify-end">
			<a href="http://192.168.43.97:8000:8000/get-test-data" target="_blank" class=" bg-teal-500 px-2 mb-1 rounded-sm">Download data as JSON</a>
		</div>
		<div class="text-center block pb-10">
			<div class="flex w-full sm:w-3/4 m-auto h-10 text-gray-200 rounded-sm shadow-2xl bg-slate-500">
				<svg class=" w-10 h-5 hidden sm:block mt-auto mb-auto ml-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
					<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
				</svg>
				<input bind:value={searchQuery} oninput={search} placeholder="Search for a button" class="outline-none placeholder-gray-200 hidden sm:block sm:w-full rounded-sm bg-slate-500">
				<span class="m-auto">From:</span>
				<input bind:value={fromDate} oninput={search} type="date" class="ml-1 bg-slate-500">
				<span class="m-auto ml-5">To:</span>
				<input bind:value={toDate} oninput={search} type="date" class="ml-1 mr-2 bg-slate-500">
			</div>

			<table class="w-full sm:w-3/4 mt-5 transparent m-auto p-10 justify-between table-fixed h-[50vh]">
				<thead class="text-white flex w-full">
					<tr class="h-12 bg-slate-700 flex w-full">
						<th class="w-1/3 m-auto" scope="col">BUTTON</th>
						<th data-tooltip="Success is 'Yes' when a push was done and a feedback from a button was received, else is 'No'" class="w-1/3 m-auto" scope="col">SUCCESS</th>
						<th class="w-1/3 m-auto" scope="col">DATE</th>
					</tr>
				</thead>
				<tbody class="border-b bg-grey-light flex flex-col items-center overflow-y-scroll w-full" >
					{#each filteredQuery as post, index}
						<tr onclick={() => showDetails(index)} class="h-12 border-b border-gray-700 hover:bg-slate-700 transition-all cursor-pointer flex w-full mb-4">
							<td class="w-1/3 m-auto">{post.button}</td>
							<td class="w-1/3 m-auto">
								{#if post.success == 1}
									<span class="p-1 pl-4 pr-4 rounded-sm bg-green-500">Yes</span>
								{:else}
									<span class="p-1 pl-4 pr-4 rounded-sm bg-red-500">No</span>
								{/if}
							</td>
							<td class="w-1/3 m-auto">{post.date}</td>
						</tr>
						{#if shDetails == index}
							<tr>
								<td colspan="3">
									<div class=" h-fit grid min-[1110px]:grid-cols-2 min-[1650px]:grid-cols-3">
										{#each post.time_val as _, ind}
											<div class="m-auto">
												<LinePlot X={post.time_val[ind]} Y={post.force_val[ind]} W=400 H=350/>
											</div>
										{/each}
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