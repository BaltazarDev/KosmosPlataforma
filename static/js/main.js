document.addEventListener('DOMContentLoaded', function () {
    // Sidebar Toggle Logic
    const submenuToggles = document.querySelectorAll('.toggle-submenu');

    submenuToggles.forEach(toggle => {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            const menuItem = this.parentElement;
            const submenu = menuItem.querySelector('.submenu');
            const arrow = this.querySelector('.arrow');

            // Toggle current
            if (submenu) {
                submenu.classList.toggle('open');
                this.classList.toggle('active-parent');
            }
        });
    });

    // Auto-expand sidebar if active child
    const activeLink = document.querySelector('.submenu a.active');
    if (activeLink) {
        const submenu = activeLink.closest('.submenu');
        const parentToggle = submenu.previousElementSibling; // .menu-link
        if (submenu) {
            submenu.classList.add('open');
        }
        if (parentToggle) {
            parentToggle.classList.add('active-parent');
        }
    }
});
