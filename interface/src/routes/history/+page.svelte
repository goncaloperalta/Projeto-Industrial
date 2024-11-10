<script>
    import { onMount } from "svelte";
	import TopBar from "../TopBar.svelte";
	let posts = [];

    onMount(() => {
        fetch('http://localhost:3000/')
            .then(resp => resp.json())
            .then(data => {
                posts = data.devices
	    });
    });
</script>

<TopBar tabName="History" />

<main class="bg-slate-800 h-screen">
	<div class="flex flex-col bg-slate-700">
		<div class="overflow-x-auto">
		  	<div class="inline-block min-w-full py-2 sm:px-6 lg:px-8">
				<div class="overflow-hidden">
			  		<table class="min-w-full text-left text-sm font-light text-surface dark:text-white">
						<thead class="border-b border-neutral-200 font-medium dark:border-white/10">
							<tr>
								<th scope="col" class="px-6 py-4">Model</th>
								<th scope="col" class="px-6 py-4">Success</th>
								<th scope="col" class="px-6 py-4">Date</th>
							</tr>
						</thead>
						<tbody>
							{#each posts as post}
								<tr class="border-b border-neutral-200 dark:border-white/10">
									<td class="whitespace-nowrap px-6 py-4">{post.model}</td>
									<td class="whitespace-nowrap px-6 py-4">
										{#if post.success == 1}
											Yes
										{:else}
											No
										{/if}
									</td>
									<td class="whitespace-nowrap px-6 py-4">{post.date}</td>
								</tr>
							{/each}
						</tbody>
			  		</table>
				</div>
		  	</div>
		</div>
	</div>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>