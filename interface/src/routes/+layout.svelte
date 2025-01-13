<script>
    import "../app.css";
    import SideBar from "../lib/SideBar.svelte";
    import TopBar from "../lib/TopBar.svelte";
</script>

<TopBar />

<SideBar />

<slot />

<footer class="bg-slate-900 flex justify-center gap-20 border-t-black">
    <a class="pt-3" href="https://www.ua.pt/">
        <img alt="ua-logo" src="ua-logo.png" class="h-14">
    </a>
    <a href="https://www.alticelabs.com/">
        <img alt="altice-logo" src="altice-logo.png" class="h-20">
    </a>
</footer>