<script>
    let sidebarOpen = false;

    function toggleSidebar() {
        sidebarOpen = !sidebarOpen;
    }
</script>

<style>
    /* Sidebar styling */
    .sidebar {
        position: fixed;
        top: 0;
        left: -250px; /* Hidden initially */
        width: 250px;
        height: 100%;
        background-color: #A5B68D;
        color: white;
        overflow-x: hidden;
        transition: 0.3s;
        padding-top: 60px;
        z-index: 1000;
    }

    .sidebar.open {
        left: 0;
    }

    .sidebar a {
        padding: 15px 25px;
        text-decoration: none;
        font-size: 18px;
        color: white;
        display: block;
        transition: 0.3s;
    }

    /* Hamburger icon styling */
    .hamburger-icon {
        position: fixed;
        top: 50px;
        left: 25px;
        cursor: pointer;
        z-index: 1001;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .hamburger-icon span {
        width: 25px;
        height: 3px;
        background-color: white;
        border-radius: 2px;
    }

    /* Main content styling */
    .main-content {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Full viewport height */
        text-align: center;
        background-color: #ECDFCC; /* Set background color */
    }

    .main-content h1 {
        font-size: 2rem; /* Increase font size */
        color: white; /* Dark text color for readability */
        top: 50px;
        padding: 20px;
        margin: 0;
    }
</style>

<!-- Hamburger icon to open sidebar -->
<div class="hamburger-icon" on:click={toggleSidebar}>
    <span></span>
    <span></span>
    <span></span>
</div>

<!-- Sidebar menu -->
<div class="sidebar {sidebarOpen ? 'open' : ''}">
    <a href="#" on:click={toggleSidebar}></a>
    <a href="/">Home</a>
    <a href="/history">History</a>
    <a href="/statistics">Statistics</a>
    <a href="/about">About</a>
</div>
