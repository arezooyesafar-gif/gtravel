(function () {
    var audio = null;
    var currentBtn = null;
    var isOpen = false;
    var currentUrl = null;
    var dragging = false;

    function fmt(s) {
        s = Math.floor(s || 0);
        var m = Math.floor(s / 60);
        var ss = s % 60;
        return m + ':' + (ss < 10 ? '0' : '') + ss;
    }

    function closePlayer() {
        var bar = document.getElementById('fbp');
        if (bar) bar.remove();
        if (audio) { audio.pause(); audio = null; }
        if (currentBtn) {
            var i = currentBtn.querySelector('i');
            if (i) i.className = 'fa fa-play';
        }
        isOpen = false;
        currentUrl = null;
        currentBtn = null;
    }

    function openPlayer(url, title, btn) {
        closePlayer();
        currentBtn = btn;
        currentUrl = url;

        var bar = document.createElement('div');
        bar.id = 'fbp';
        bar.innerHTML =
            '<div id="fbp-inner">' +
                '<button id="fbp-close" title="بستن">&#10005;</button>' +
                '<div id="fbp-info">' +
                    '<span id="fbp-title">' + (title || 'فایل صوتی') + '</span>' +
                '</div>' +
                '<button id="fbp-play-btn"><i class="fa fa-play"></i></button>' +
                '<span id="fbp-cur">0:00</span>' +
                '<div id="fbp-track">' +
                    '<div id="fbp-fill"></div>' +
                    '<div id="fbp-thumb"></div>' +
                '</div>' +
                '<span id="fbp-dur">0:00</span>' +
                '<button id="fbp-vol-btn"><i class="fa fa-volume-up"></i></button>' +
            '</div>';
        document.body.appendChild(bar);

        setTimeout(function () { bar.classList.add('fbp-show'); }, 10);

        document.getElementById('fbp-close').onclick = closePlayer;

        audio = new Audio(url);

        var playBtn = document.getElementById('fbp-play-btn');
        var curEl = document.getElementById('fbp-cur');
        var durEl = document.getElementById('fbp-dur');
        var fill = document.getElementById('fbp-fill');
        var thumb = document.getElementById('fbp-thumb');
        var track = document.getElementById('fbp-track');
        var volBtn = document.getElementById('fbp-vol-btn');
        var muted = false;

        playBtn.onclick = function () {
            if (audio.paused) audio.play(); else audio.pause();
        };

        volBtn.onclick = function () {
            muted = !muted;
            audio.muted = muted;
            var vi = volBtn.querySelector('i');
            if (vi) vi.className = muted ? 'fa fa-volume-mute' : 'fa fa-volume-up';
        };

        audio.addEventListener('loadedmetadata', function () {
            durEl.textContent = fmt(audio.duration);
        });

        audio.addEventListener('timeupdate', function () {
            if (dragging) return;
            var pct = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
            fill.style.width = pct + '%';
            thumb.style.left = pct + '%';
            curEl.textContent = fmt(audio.currentTime);
        });

        audio.addEventListener('play', function () {
            var pi = playBtn.querySelector('i');
            if (pi) pi.className = 'fa fa-pause';
            if (currentBtn) { var bi = currentBtn.querySelector('i'); if (bi) bi.className = 'fa fa-pause'; }
        });

        audio.addEventListener('pause', function () {
            var pi = playBtn.querySelector('i');
            if (pi) pi.className = 'fa fa-play';
            if (currentBtn) { var bi = currentBtn.querySelector('i'); if (bi) bi.className = 'fa fa-play'; }
        });

        audio.addEventListener('ended', closePlayer);

        function seek(e) {
            var rect = track.getBoundingClientRect();
            var x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
            var pct = Math.max(0, Math.min(1, x / rect.width));
            fill.style.width = (pct * 100) + '%';
            thumb.style.left = (pct * 100) + '%';
            curEl.textContent = fmt(pct * audio.duration);
            if (!dragging) audio.currentTime = pct * audio.duration;
        }

        track.addEventListener('mousedown', function (e) { dragging = true; seek(e); });
        track.addEventListener('touchstart', function (e) { dragging = true; seek(e); }, { passive: true });
        document.addEventListener('mousemove', function (e) { if (dragging) seek(e); });
        document.addEventListener('touchmove', function (e) { if (dragging) seek(e); }, { passive: true });
        document.addEventListener('mouseup', function (e) {
            if (dragging) { dragging = false; var rect = track.getBoundingClientRect(); var x = e.clientX - rect.left; var pct = Math.max(0, Math.min(1, x / rect.width)); audio.currentTime = pct * audio.duration; }
        });
        document.addEventListener('touchend', function () { if (dragging) dragging = false; });

        audio.play();
        isOpen = true;
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.audio-play-btn').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                var url = btn.dataset.audioUrl;
                var title = btn.dataset.audioTitle;
                if (!url) return;
                if (isOpen && currentUrl === url) {
                    if (audio) { if (audio.paused) audio.play(); else audio.pause(); }
                } else {
                    openPlayer(url, title, btn);
                }
            });
        });
    });
})();
