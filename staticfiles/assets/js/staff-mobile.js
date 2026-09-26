(function () {
    var BREAKPOINT = 992;
    var menu = null;
    var backdrop = null;

    function isMobile() {
        return window.innerWidth < BREAKPOINT;
    }

    function closeMenu() {
        if (menu) {
            menu.classList.remove('staff-menu-open');
        }
        if (backdrop) {
            backdrop.remove();
            backdrop = null;
        }
        document.body.style.overflow = '';
    }

    function openMenu() {
        if (!menu) {
            return;
        }
        menu.classList.add('staff-menu-open');
        backdrop = document.createElement('div');
        backdrop.className = 'staff-menu-backdrop';
        backdrop.addEventListener('click', closeMenu);
        document.body.appendChild(backdrop);
        document.body.style.overflow = 'hidden';
    }

    function toggleMenu(event) {
        if (event) {
            event.preventDefault();
        }
        if (!isMobile()) {
            return;
        }
        if (menu && menu.classList.contains('staff-menu-open')) {
            closeMenu();
        } else {
            openMenu();
        }
    }

    function setupSubmenus() {
        document.querySelectorAll('.nk-header-menu .nk-menu-toggle').forEach(function (link) {
            link.addEventListener('click', function (event) {
                if (!isMobile()) {
                    return;
                }
                event.preventDefault();
                var item = link.closest('.nk-menu-item');
                if (!item) {
                    return;
                }
                var parent = item.parentElement;
                if (parent) {
                    parent.querySelectorAll(':scope > .nk-menu-item.staff-open').forEach(function (other) {
                        if (other !== item) {
                            other.classList.remove('staff-open');
                        }
                    });
                }
                item.classList.toggle('staff-open');
            });
        });
    }

    function wrapTables() {
        document.querySelectorAll('table.table').forEach(function (table) {
            var parent = table.parentElement;
            if (!parent || parent.classList.contains('staff-scroll-x')) {
                return;
            }
            var box = document.createElement('div');
            box.className = 'staff-scroll-x';
            parent.insertBefore(box, table);
            box.appendChild(table);
        });
    }

    function syncMode() {
        if (!menu) {
            return;
        }
        menu.classList.toggle('mobile-menu', isMobile());
        if (!isMobile()) {
            menu.querySelectorAll('.nk-menu-item.staff-open').forEach(function (item) {
                item.classList.remove('staff-open');
            });
        }
    }

    function setup() {
        menu = document.querySelector('.nk-header-menu');
        syncMode();
        document.querySelectorAll('.nk-nav-toggle').forEach(function (trigger) {
            trigger.addEventListener('click', toggleMenu);
        });
        document.querySelectorAll('.nk-header-menu .nk-menu-link:not(.nk-menu-toggle)').forEach(function (link) {
            link.addEventListener('click', function () {
                if (isMobile()) {
                    closeMenu();
                }
            });
        });
        setupSubmenus();
        wrapTables();
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                closeMenu();
            }
        });
        window.addEventListener('resize', function () {
            syncMode();
            if (!isMobile()) {
                closeMenu();
            }
        });
        if (window.jQuery) {
            jQuery(document).ajaxComplete(function () {
                wrapTables();
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setup);
    } else {
        setup();
    }
})();
