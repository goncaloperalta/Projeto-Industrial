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

<nav class="bg-white border-gray-200 dark:bg-gray-900">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Statistics</span>
        <button data-collapse-toggle="navbar-default" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-default" aria-expanded="false">
            <span class="sr-only">Open main menu</span>
            <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
            </svg>
        </button>
        <div class="hidden w-full md:block md:w-auto" id="navbar-default">
            <ul class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
                <li>
                    <a href="/" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Home</a>
                </li>
                <li>
                    <a href="/history" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">History</a>
                </li>
                <li>
                    <a href="/statistics" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Statistics</a>
                </li>
                <li>
                    <a href="/about" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">About</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

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