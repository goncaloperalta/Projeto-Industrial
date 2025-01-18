<script>
    import LinePlot from "../../lib/LinePlot.svelte";
	
	let url = "http://localhost:8000/"
    if(typeof document != "undefined"){
        url = `http://${window.location.hostname}:8000/`
    }

	export let data;

	let posts = data.tests;	
	$: filteredQuery = posts;
	let searchQuery = '';
	let ind = 0;
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

	function getSuccess(success){
		let sum = 0;
		success.forEach(x => {
			sum += x;
		});
		if(sum == success.length){
			return 'All actuations worked as expected';
		} else{
			return `Out of ${success.length} only ${sum} worked as expected`;
		}
	}

	let count = data.count;
	let offset = 0;
	let updateTable = 0;
	async function leftPage(){
		if(offset >= 10){
			offset -= 10;
			const res = await fetch(url+"get-tests-range", {
				method: "POST",
				headers: {"Content-Type": "application/json"},
				body: JSON.stringify({
					size: 10,
					offset: offset
				})
			});
        	const data = await res.json();
        
        	posts = data.tests.test;
			shDetails = -1;
			updateTable = !updateTable;
		}
	}
	async function changePage(pm){
		let flag = 0;
		if(pm == '-'){
			if(offset >= 10){
				flag = 1;
				offset -= 10;
			}
		} else{
			if(offset <= count - 10){
				flag = 1;
				offset += 10;
			}
		}

		if(flag){
			const res = await fetch(url+"get-tests-range", {
				method: "POST",
				headers: {"Content-Type": "application/json"},
				body: JSON.stringify({
					size: 10,
					offset: offset
				})
			});
        	const data = await res.json();

        	posts = data.tests.test;
			for(let i = 0; i < posts.length; i++){
				let timeVal = JSON.parse(posts[i].time_val);
				let forceVal = JSON.parse(posts[i].force_val);
				
				for(let j = 0; j < timeVal.length; j++){
					posts[i].time_val = timeVal;
					posts[i].force_val = forceVal;
				}

				posts[i].success = JSON.parse(posts[i].success);
				posts[i].parameters = JSON.parse(posts[i].parameters);
			}
			shDetails = -1;
			updateTable = !updateTable;
		}
	}
	console.log(filteredQuery)
</script>

<main class="min-h-screen bg-slate-800 text-white">
	<div class="text-center block">
		<div class="p-20 pb-10 text-3xl">
			History
		</div>
		<div class="m-auto flex sm:w-3/4 justify-end">
			<a href={url+"get-tests-data"} target="_blank" class=" bg-teal-500 px-2 mb-1 rounded-sm">Download data as JSON</a>
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

			{#key updateTable}
				<table class="w-full sm:w-3/4 mt-5 transparent m-auto p-10 justify-between table-fixed h-[50vh]">
					<thead class="text-white flex w-full">
						<tr class="h-12 bg-slate-700 flex italic w-full">
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
									{#if getSuccess(post.success) == 'All actuations worked as expected'}
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
										<div class="h-fit min-[1770px]:grid min-[1770px]:grid-cols-2">
											<div class="flex mx-auto">
												<select name="graph-number" bind:value={ind} class="bg-slate-500 border-slate-500 rounded-lg p-2 w-fit h-fit text-center">											
													{#each post.time_val as _, index}
														<option value="{index}">{index+1}</option>
													{/each}
												</select>
												{#key ind}
													<div>
														<LinePlot X={post.time_val[ind]} Y={post.force_val[ind]} W=400 H=350/>
													</div>
												{/key}
											</div>
											<div class=" text-left my-10  min-[1770px]:my-auto">
												<div>Test done at {post.time} of the day {post.date}.</div>
												<div>{getSuccess(post.success)}</div>
												<div>{post.error == 'No Error' ? 'No errors occured' : post.error}</div>
												<div>Test ran with a press time of {post.parameters[0]}s, number of actuations of {post.parameters[1]} and an interval of {post.parameters[2]}s</div>
												{#if post.presses == post.parameters[1]}
													<div>Test was not aborted</div>
												{:else}
													<div>Test was aborted at {post.presses} of {post.parameters[1]} actuations</div>
												{/if}
											</div>
										</div>
									</td>
								</tr>
							{/if}
						{/each}
					</tbody>
				</table>
			{/key}
			<div class="mx-auto mt-2 flex sm:w-3/4 justify-end">
				<span class="mx-2 pt-[1px]">
					Viewing most recent tests {offset+1} to {offset+10 > count ? count : offset+10} of {count}
				</span>
				<button onclick={() => changePage('-')} class="bg-teal-500 px-2 mb-1 rounded-sm font-bold pb-1">
					&lt
				</button>
				<button onclick={() => changePage('+')} class="bg-teal-500 px-2 mb-1 rounded-sm mx-2 font-bold pb-1">
					&gt
				</button>
			</div>
		</div>
	</div>
</main>
