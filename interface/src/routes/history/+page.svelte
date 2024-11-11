<script>
    import { onMount } from "svelte";
	import TopBar from "../TopBar.svelte";
    import LinePlot from "../LinePlot.svelte";
	let posts = [];

    onMount(() => {
        fetch('http://localhost:3000/')
            .then(resp => resp.json())
            .then(data => {
                posts = data.devices
	    });
    });

	let shDetails = -1;
	function showDetails(ind){
		if(shDetails != ind){
			shDetails = ind
		} else{
			shDetails = -1;
		}
	}
</script>

<TopBar tabName="History" />

<main class="bg-slate-800 h-screen text-white">
	<div class="text-center block">
		<div class="p-20 text-3xl">
			History
		</div>
		<div class="text-center block">
			<div class="flex w-3/4 m-auto h-10 bg-gray-500 rounded-sm">
				<svg class=" text-gray-200 w-10 h-5 mt-auto mb-auto ml-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
					<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
				</svg>
				<input placeholder="Search for model, date, ..." class="bg-gray-500 outline-none placeholder-gray-200 w-full rounded-sm">
			</div>

			<table class="w-3/4 mt-5 transparent m-auto p-10 table-fixed">
				<thead class="italic">
					<tr class="bg-slate-700 h-12">
						<th scope="col">MODEL</th>
						<th scope="col">SUCCESS</th>
						<th scope="col">DATE</th>
					</tr>
				</thead>
				<tbody class="border-b">
					{#each posts as post, index}
						<tr onclick={() => showDetails(index)} class="h-12 border-b border-gray-700 hover:bg-slate-700 transition-all cursor-pointer">
							<td>{post.model}</td>
							<td>
								{#if post.success == 1}
									<span class="bg-green-500 p-1 pl-4 pr-4 rounded-sm">Yes</span>
								{:else}
									<span class="bg-red-500 p-1 pl-4 pr-4 rounded-sm">No</span>
								{/if}
							</td>
							<td>{post.date}</td>
						</tr>
						{#if shDetails == index}
							<tr>
								<td colspan="3">
									<div class="flex h-[400px] pl-20">
										<ul class="mt-auto mb-auto mr-20">
											<li>CPU:2.4GHz</li>
											<li>RAM:6GB</li>
										</ul>
										<LinePlot />
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

<style></style>