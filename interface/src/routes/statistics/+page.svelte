<script>
    import PieChart2 from "./PieChart2.svelte";
    import LinePlot from "../LinePlot.svelte";

	export let data;
	console.log(data)

	let successRate = 0;
	let posts = data.devices;
	posts.forEach(post => {
		successRate += post.success
	});
	successRate = successRate / posts.length * 100;
</script>

<main class="bg-slate-800 h-screen text-white">
	<div class="text-center block">
		<div class="p-20 text-3xl">
			Statistics
		</div>
		<div class="m-auto flex justify-center bg-slate-600 w-3/4 rounded-sm shadow-lg">
			<div class="p-40">
				{#key successRate}
					<PieChart2 successRate={successRate} />
				{/key}
			</div>
			<div class="p-40">
				<LinePlot />
			</div>
		</div>
	</div>
		
</main>

<style>
	
</style>