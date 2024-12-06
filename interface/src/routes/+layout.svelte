<script>
    import "../app.css";
    import SideBar from "./SideBar.svelte";
</script>
  
<SideBar />

<slot />

<footer class="h-[10%] dark:bg-gradient-to-b dark:from-slate-800 dark:to-slate-950 flex justify-center gap-40 border-t-black">
    <a class="pt-3" href="https://www.ua.pt/">
        <img alt="ua-logo" src="ua-logo.png" class="h-14">
    </a>
    <a href="https://www.alticelabs.com/">
        <img alt="altice-logo" src="altice-logo.png" class="h-20">
    </a>
</footer>