<script>
    import PieChart2 from "../../lib/PieChart2.svelte";

	export let data;

	let successRate = 0;
	let length = 0;
	let posts = data.tests;
	posts.forEach(post => {
		post.forEach(el => {
			successRate += el
			length += 1
		})		
	});
	successRate = successRate / length * 100;
</script>

<main class="bg-slate-800 h-screen text-white">
	<div class="text-center block">
		<div class="p-20 text-3xl">
			Statistics
		</div>
		<div class="m-auto min-[1340px]:flex bg-slate-600 w-fit md:rounded-sm shadow-lg py-10">
			<div class="mx-10 md:mx-20 lg:mx-40 my-10 min-[1340px]:my-0">
				{#key successRate}
					<PieChart2 successRate={successRate} />
				{/key}
			</div>
			<div class="mx-10 md:mx-20 lg:mx-40 my-auto text-2xl">
				Total number of actuations: {length}
			</div>
		</div>
	</div>
		
</main>

<style>
	
</style>
