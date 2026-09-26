// جایگزین vanilla-JS برای سه کامپوننت واقعاً استفاده‌شده از Bootstrap JS
// در سایت: offcanvas (منوی موبایل)، modal (ماشین‌حساب اقساط + گالری/رزرو
// هتل و تور)، accordion/collapse (فوتر + FAQ)، و تب‌های گالری هتل.
// مارک‌آپ/اتربیوت‌های data-bs-* تمپلیت‌ها دست‌نخورده می‌مونن، فقط منطق
// نمایش/پنهان‌سازی رو خودمون پیاده می‌کنیم؛ بدون jQuery.
(function () {
    'use strict';

    function qs(root, sel) { return (root || document).querySelector(sel); }
    function qsa(root, sel) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

    function dispatch(el, name) {
        el.dispatchEvent(new CustomEvent(name, { bubbles: true }));
    }

    // ===== Offcanvas =====
    var offcanvasBackdrop = null;

    function showOffcanvas(el) {
        if (!el || el.classList.contains('show')) return;
        el.classList.add('show');
        el.removeAttribute('aria-hidden');
        el.setAttribute('aria-modal', 'true');
        var lockScroll = el.getAttribute('data-bs-scroll') !== 'true';
        if (lockScroll) document.body.style.overflow = 'hidden';
        if (!offcanvasBackdrop) {
            offcanvasBackdrop = document.createElement('div');
            offcanvasBackdrop.className = 'offcanvas-backdrop fade';
            document.body.appendChild(offcanvasBackdrop);
            requestAnimationFrame(function () { offcanvasBackdrop.classList.add('show'); });
            offcanvasBackdrop.addEventListener('click', function () { hideOffcanvas(el); });
        }
        dispatch(el, 'shown.bs.offcanvas');
    }

    function hideOffcanvas(el) {
        if (!el || !el.classList.contains('show')) return;
        el.classList.remove('show');
        el.setAttribute('aria-hidden', 'true');
        el.removeAttribute('aria-modal');
        document.body.style.overflow = '';
        if (offcanvasBackdrop) {
            offcanvasBackdrop.remove();
            offcanvasBackdrop = null;
        }
        dispatch(el, 'hidden.bs.offcanvas');
    }

    document.addEventListener('click', function (e) {
        var toggle = e.target.closest('[data-bs-toggle="offcanvas"]');
        if (toggle) {
            e.preventDefault();
            var target = document.querySelector(toggle.getAttribute('data-bs-target'));
            showOffcanvas(target);
            return;
        }
        var dismiss = e.target.closest('[data-bs-dismiss="offcanvas"]');
        if (dismiss) {
            e.preventDefault();
            hideOffcanvas(dismiss.closest('.offcanvas'));
        }
    });

    // ===== Modal =====
    var modalBackdrop = null;
    var openModalCount = 0;

    function ModalInstance(el) {
        this.el = el;
    }
    ModalInstance.prototype.show = function () {
        var el = this.el;
        if (!el || el.classList.contains('show')) return;
        el.style.display = 'block';
        // یک فریم صبر می‌کنیم تا transition واقعی اجرا بشه
        requestAnimationFrame(function () {
            el.classList.add('show');
        });
        openModalCount++;
        document.body.classList.add('modal-open');
        document.body.style.overflow = 'hidden';
        if (!modalBackdrop) {
            modalBackdrop = document.createElement('div');
            modalBackdrop.className = 'modal-backdrop fade';
            document.body.appendChild(modalBackdrop);
            requestAnimationFrame(function () { modalBackdrop.classList.add('show'); });
        }
        setTimeout(function () { dispatch(el, 'shown.bs.modal'); }, 50);
    };
    ModalInstance.prototype.hide = function () {
        var el = this.el;
        if (!el || !el.classList.contains('show')) return;
        el.classList.remove('show');
        setTimeout(function () {
            el.style.display = 'none';
            openModalCount = Math.max(0, openModalCount - 1);
            if (openModalCount === 0) {
                document.body.classList.remove('modal-open');
                document.body.style.overflow = '';
                if (modalBackdrop) { modalBackdrop.remove(); modalBackdrop = null; }
            }
            dispatch(el, 'hidden.bs.modal');
        }, 150);
    };

    var modalInstances = new WeakMap();
    function getOrCreateModal(el) {
        if (!modalInstances.has(el)) modalInstances.set(el, new ModalInstance(el));
        return modalInstances.get(el);
    }

    document.addEventListener('click', function (e) {
        var toggle = e.target.closest('[data-bs-toggle="modal"]');
        if (toggle) {
            e.preventDefault();
            var target = document.querySelector(toggle.getAttribute('data-bs-target'));
            if (target) getOrCreateModal(target).show();
            return;
        }
        var dismiss = e.target.closest('[data-bs-dismiss="modal"]');
        if (dismiss) {
            e.preventDefault();
            var modalEl = dismiss.closest('.modal');
            if (modalEl) getOrCreateModal(modalEl).hide();
            return;
        }
        // کلیک روی بک‌دراپ خودِ مودال (بیرون از modal-dialog) هم می‌بندتش
        if (e.target.classList.contains('modal') && e.target.classList.contains('show')) {
            getOrCreateModal(e.target).hide();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key !== 'Escape') return;
        var openModal = document.querySelector('.modal.show');
        if (openModal) getOrCreateModal(openModal).hide();
        var openOffcanvas = document.querySelector('.offcanvas.show');
        if (openOffcanvas) hideOffcanvas(openOffcanvas);
    });

    // ===== Tab =====
    function TabInstance(el) { this.el = el; }
    TabInstance.prototype.show = function () {
        var trigger = this.el;
        if (!trigger) return;
        var targetSel = trigger.getAttribute('data-bs-target') || trigger.getAttribute('href');
        var pane = targetSel ? document.querySelector(targetSel) : null;
        if (!pane) return;

        var navContainer = trigger.closest('ul, div');
        if (navContainer) {
            qsa(navContainer, '[data-bs-toggle="tab"]').forEach(function (btn) {
                btn.classList.remove('active');
                btn.setAttribute('aria-selected', 'false');
            });
        }
        trigger.classList.add('active');
        trigger.setAttribute('aria-selected', 'true');

        var paneContainer = pane.parentElement;
        if (paneContainer) {
            qsa(paneContainer, ':scope > .tab-pane').forEach(function (p) {
                p.classList.remove('show', 'active');
            });
        }
        pane.classList.add('show', 'active');
        dispatch(trigger, 'shown.bs.tab');
    };

    var tabInstances = new WeakMap();
    function getOrCreateTab(el) {
        if (!tabInstances.has(el)) tabInstances.set(el, new TabInstance(el));
        return tabInstances.get(el);
    }

    document.addEventListener('click', function (e) {
        var trigger = e.target.closest('[data-bs-toggle="tab"]');
        if (trigger) {
            e.preventDefault();
            getOrCreateTab(trigger).show();
        }
    });

    // ===== Accordion / Collapse =====
    function showCollapse(el) {
        if (!el || el.classList.contains('show')) return;
        el.classList.add('show');
        qsa(document, '[data-bs-target="#' + el.id + '"], [href="#' + el.id + '"]').forEach(function (btn) {
            btn.classList.remove('collapsed');
            btn.setAttribute('aria-expanded', 'true');
        });
    }
    function hideCollapse(el) {
        if (!el || !el.classList.contains('show')) return;
        el.classList.remove('show');
        qsa(document, '[data-bs-target="#' + el.id + '"], [href="#' + el.id + '"]').forEach(function (btn) {
            btn.classList.add('collapsed');
            btn.setAttribute('aria-expanded', 'false');
        });
    }

    document.addEventListener('click', function (e) {
        var toggle = e.target.closest('[data-bs-toggle="collapse"]');
        if (!toggle) return;
        e.preventDefault();
        var sel = toggle.getAttribute('data-bs-target') || toggle.getAttribute('href');
        var target = sel ? document.querySelector(sel) : null;
        if (!target) return;

        var isOpen = target.classList.contains('show');
        var parentSel = toggle.getAttribute('data-bs-parent');
        if (parentSel && !isOpen) {
            var parent = document.querySelector(parentSel);
            if (parent) {
                qsa(parent, '.accordion-collapse.show, .collapse.show').forEach(function (openEl) {
                    if (openEl !== target) hideCollapse(openEl);
                });
            }
        }
        if (isOpen) hideCollapse(target); else showCollapse(target);
    });

    // ===== سازگاری با کد قدیمی که مستقیم API بوت‌استرپ رو صدا می‌زنه
    // (مثل detail-tour.html / hotel-detail.html که
    // bootstrap.Modal.getOrCreateInstance(...)/bootstrap.Tab... رو صدا
    // می‌زنن) — یه global شبیه‌سازی‌شده تعریف می‌کنیم که همون امضا رو داره =====
    window.bootstrap = window.bootstrap || {
        Modal: {
            getOrCreateInstance: function (el) { return getOrCreateModal(el); },
        },
        Tab: {
            getOrCreateInstance: function (el) { return getOrCreateTab(el); },
        },
    };
})();
