document.addEventListener('DOMContentLoaded', function() {
    // Function to adjust sidebar and content based on screen size
    function adjustLayout() {
        var sidebar = document.getElementById('sidebar-wrapper');
        var header = document.querySelector('.header-container');
        var contentWrapper = document.querySelector('.content-wrapper');
        var logo = document.querySelector('.logo');

        // Screen width threshold to hide/show sidebar
        var screenWidth = window.innerWidth;

        // Adjust sidebar and content for small screens
        if (screenWidth <= 768) {
            // Hide sidebar, expand content width
            sidebar.style.display = 'none';
            contentWrapper.style.marginLeft = '0';
            contentWrapper.style.width = '100%';
            
            // Adjust logo size for smaller screens
            if (logo) {
                logo.style.width = '30%';
            }
        } else {
            // Show sidebar, adjust content and sidebar for larger screens
            sidebar.style.display = 'block';
            contentWrapper.style.marginLeft = '220px';
            contentWrapper.style.width = 'calc(100% - 220px)';
            
            // Reset logo size for larger screens
            if (logo) {
                logo.style.width = '40%';
            }
        }
    }

    // Call the function when the page loads
    adjustLayout();

    // Listen for window resize event and adjust layout accordingly
    window.addEventListener('resize', function() {
        adjustLayout();
    });
    
    // Add a sidebar toggle button for small screens
    var toggleButton = document.createElement('button');
    toggleButton.innerText = "Toggle Sidebar";
    toggleButton.style.position = 'fixed';
    toggleButton.style.top = '15px';
    toggleButton.style.right = '15px';
    toggleButton.style.zIndex = '1000';
    toggleButton.style.display = 'none'; // Hidden by default, show on small screens

    document.body.appendChild(toggleButton);

    toggleButton.addEventListener('click', function() {
        var sidebar = document.getElementById('sidebar-wrapper');
        if (sidebar.style.display === 'none') {
            sidebar.style.display = 'block';
        } else {
            sidebar.style.display = 'none';
        }
    });

    // Show toggle button on small screens
    if (window.innerWidth <= 768) {
        toggleButton.style.display = 'block';
    } else {
        toggleButton.style.display = 'none';
    }

    // Update toggle button visibility on resize
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768) {
            toggleButton.style.display = 'block';
        } else {
            toggleButton.style.display = 'none';
        }
    });
});