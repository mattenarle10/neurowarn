document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', function() {
        const sidebar = document.getElementById('sidebar');
        const logo = document.getElementById('sidebar-logo');

        if (sidebar) {
            // Toggle collapsed class on sidebar
            if (sidebar.classList.contains('collapsed')) {
                sidebar.classList.remove('collapsed');
                logo.src = 'images/logo-neurowarn.png';  // Revert to the full logo when expanded
              
            } else {
                sidebar.classList.add('collapsed');
                logo.src = 'images/logo-n.png';  // Change to the smaller logo when collapsed

            }

            // Remove highlight from all menu items
            document.querySelectorAll('.menu-item').forEach(menuItem => {
                menuItem.classList.remove('highlight');
            });

            // Highlight the clicked menu item
            item.classList.add('highlight');
        } else {
            console.error('Sidebar element not found.');
        }
    });
});
