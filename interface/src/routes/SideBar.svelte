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
        padding-top: 90px;
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
</style>

<!-- Hamburger icon to open sidebar -->
<button class="hamburger-icon text-3xl text-white scale-x-110" onclick={toggleSidebar}>&#9776;</button>

<!-- Sidebar menu -->
<div class="sidebar {sidebarOpen ? 'open' : ''}">
    <a href="/" onclick={toggleSidebar}>Home</a>
    <a href="/history" onclick={toggleSidebar}>History</a>
    <a href="/statistics" onclick={toggleSidebar}>Statistics</a>
    <a href="/APIDocumentation" onclick={toggleSidebar}>API Documentation</a>
    <a href="/about" onclick={toggleSidebar}>About</a>
</div>
