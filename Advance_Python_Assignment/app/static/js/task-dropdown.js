// task-dropdown.js : used in tasks.html

function toggleDropdown(taskId) {
    const dropdown = document.getElementById('dropdown-' + taskId);
    const allDropdowns = document.querySelectorAll('.task-dropdown');

    // Close all other dropdowns
    allDropdowns.forEach(d => {
        if (d !== dropdown) {
            d.style.display = 'none';
        }
    });

    // Toggle current dropdown
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.task-actions-dropdown')) {
        document.querySelectorAll('.task-dropdown').forEach(d => {
            d.style.display = 'none';
        });
    }
});
