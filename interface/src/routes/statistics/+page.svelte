<script>
    import { onMount } from "svelte";
	let posts = [];

    onMount(() => {
        fetch('http://localhost:3000/')
            .then(resp => resp.json())
            .then(data => {
                posts = data.devices
	    });
    });
</script>

<nav>
	<a href="/">Home</a>
	<a href="/history">History</a>
	<a href="/statistics">Statistics</a>
	<a href="/about">About</a>
</nav>

<main>
    <h1 class="text-3xl font-bold underline">
        Hello world!
    </h1>
	{#each posts as post}
		<h3>model: {post.model}, success: {post.success}!</h3>
		<hr>
	{/each}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>