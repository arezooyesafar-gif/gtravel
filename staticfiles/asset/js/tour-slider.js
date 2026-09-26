// اسلایدر «تورهای ویژه» صفحه اصلی — جایگزین سبک owl-carousel/jQuery.
// اسکرول افقی با CSS scroll-snap انجام می‌شود؛ این اسکریپت فقط دکمه‌های
// قبلی/بعدی و پخش خودکار را اضافه می‌کند و بدون آن هم اسلایدر کار می‌کند.
(function () {
    function initTourSlider(track) {
        var viewport = track.closest('.tour-slider-viewport');
        if (!viewport) return;
        var prevBtn = viewport.querySelector('.tour-slider-prev');
        var nextBtn = viewport.querySelector('.tour-slider-next');
        var items = track.children;
        if (!items.length) return;

        function step() {
            var item = items[0];
            var style = window.getComputedStyle(track);
            var gap = parseFloat(style.columnGap || style.gap || 0) || 0;
            return item.getBoundingClientRect().width + gap;
        }

        function atStart() {
            return Math.abs(track.scrollLeft) < 2;
        }

        function atEnd() {
            return Math.abs(track.scrollLeft) + track.clientWidth >= track.scrollWidth - 2;
        }

        // در RTL جهت اسکرول برعکس LTR است: "بعدی" یعنی مقدار منفی‌تر
        function goNext() {
            if (atEnd()) {
                track.scrollTo({left: 0, behavior: 'smooth'});
            } else {
                track.scrollBy({left: -step(), behavior: 'smooth'});
            }
        }

        function goPrev() {
            if (atStart()) {
                track.scrollTo({left: -(track.scrollWidth), behavior: 'smooth'});
            } else {
                track.scrollBy({left: step(), behavior: 'smooth'});
            }
        }

        if (nextBtn) nextBtn.addEventListener('click', function () {
            stopAutoplay();
            goNext();
        });
        if (prevBtn) prevBtn.addEventListener('click', function () {
            stopAutoplay();
            goPrev();
        });

        var autoplayId = null;

        function startAutoplay() {
            if (autoplayId || items.length < 2) return;
            autoplayId = setInterval(goNext, 4000);
        }

        function stopAutoplay() {
            if (autoplayId) {
                clearInterval(autoplayId);
                autoplayId = null;
            }
        }

        track.addEventListener('mouseenter', stopAutoplay);
        track.addEventListener('touchstart', stopAutoplay, {passive: true});
        track.addEventListener('mouseleave', startAutoplay);

        startAutoplay();
    }

    function init() {
        document.querySelectorAll('.tour-slider').forEach(initTourSlider);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
