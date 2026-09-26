(function () {
    var _open = false;
    var _pollTimer = null;

    function _sid() {
        var k = 'cb_sid';
        var v = localStorage.getItem(k);
        if (!v) {
            v = 'u' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
            localStorage.setItem(k, v);
        }
        return v;
    }

    window.toggleChatbot = function () {
        var panel = document.getElementById('chatbot-panel');
        _open = !_open;
        if (_open) {
            panel.classList.add('open');
            if (!document.querySelector('#chatbot-messages .cb-msg')) {
                _addMsg('assistant', 'سلام! 👋 من دستیار هوشمند آرزو سفر هستم. درباره تورها، ویزا، هتل و سفر می‌توانم راهنماییتان کنم.');
            }
            setTimeout(function () { var i = document.getElementById('chatbot-input'); if (i) i.focus(); }, 150);
            _startPoll();
        } else {
            panel.classList.remove('open');
            _stopPoll();
        }
    };

    function _startPoll() {
        _stopPoll();
        _pollTimer = setInterval(function () {
            fetch('/chat-poll/' + _sid())
                .then(function (r) { return r.json(); })
                .then(function (d) {
                    if (d.messages && d.messages.length) {
                        d.messages.forEach(function (m) {
                            _addMsg('assistant', '👨‍💼 پشتیبان: ' + m);
                        });
                    }
                }).catch(function () {});
        }, 5000);
    }

    function _stopPoll() {
        if (_pollTimer) { clearInterval(_pollTimer); _pollTimer = null; }
    }

    window.sendChatMessage = function () {
        var input = document.getElementById('chatbot-input');
        var msg = (input.value || '').trim();
        if (!msg) return;
        input.value = '';

        var sendBtn = document.getElementById('chatbot-send');
        if (sendBtn) sendBtn.disabled = true;

        _addMsg('user', msg);
        _showTyping();

        var csrf = ((document.getElementsByName('csrfmiddlewaretoken')[0] || {}).value) || '';
        fetch('/chat-message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
            body: JSON.stringify({
                message: msg,
                session_id: _sid(),
                page_url: window.location.href
            })
        }).then(function (r) { return r.json(); }).then(function (d) {
            _removeTyping();
            if (sendBtn) sendBtn.disabled = false;
            if (d.type === 'lead') {
                _addMsg('assistant', d.message);
                _addLeadForm();
            } else {
                _addMsg('assistant', d.message);
            }
        }).catch(function () {
            _removeTyping();
            if (sendBtn) sendBtn.disabled = false;
            _addMsg('assistant', 'خطا در ارتباط. لطفاً دوباره تلاش کنید.');
        });
    };

    function _addMsg(role, text) {
        var box = document.getElementById('chatbot-messages');
        if (!box) return;
        var d = document.createElement('div');
        d.className = 'cb-msg ' + role;
        d.textContent = text;
        box.appendChild(d);
        box.scrollTop = box.scrollHeight;
    }

    function _showTyping() {
        var box = document.getElementById('chatbot-messages');
        if (!box || document.getElementById('_cb_typing')) return;
        var d = document.createElement('div');
        d.className = 'cb-msg typing';
        d.id = '_cb_typing';
        d.textContent = '···';
        box.appendChild(d);
        box.scrollTop = box.scrollHeight;
    }

    function _removeTyping() {
        var el = document.getElementById('_cb_typing');
        if (el) el.remove();
    }

    function _addLeadForm() {
        var box = document.getElementById('chatbot-messages');
        if (!box || document.getElementById('_cb_lead')) return;
        var d = document.createElement('div');
        d.className = 'cb-lead-form';
        d.id = '_cb_lead';
        d.innerHTML =
            '<input id="_cb_name" type="text" placeholder="نام" />' +
            '<input id="_cb_family" type="text" placeholder="نام خانوادگی" />' +
            '<input id="_cb_phone" type="tel" placeholder="شماره موبایل" />' +
            '<button onclick="submitChatLead(this)">ثبت اطلاعات</button>';
        box.appendChild(d);
        box.scrollTop = box.scrollHeight;
    }

    window.submitChatLead = function (btn) {
        var name = (document.getElementById('_cb_name') || {}).value || '';
        var family = (document.getElementById('_cb_family') || {}).value || '';
        var phone = (document.getElementById('_cb_phone') || {}).value || '';
        if (!phone) { alert('لطفاً شماره موبایل را وارد کنید'); return; }
        btn.disabled = true;
        btn.textContent = 'در حال ثبت...';
        var csrf = ((document.getElementsByName('csrfmiddlewaretoken')[0] || {}).value) || '';
        fetch('/save-tour-interest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
            body: JSON.stringify({ name: name, family: family, phone: phone, page_type: 'chat', page_slug: window.location.pathname })
        }).then(function (r) { return r.json(); }).then(function () {
            document.getElementById('_cb_lead').innerHTML = '<p style="color:green;margin:0;font-size:13px;">✓ اطلاعات شما ثبت شد. کارشناسان ما تماس می‌گیرند.</p>';
        }).catch(function () {
            btn.disabled = false;
            btn.textContent = 'ثبت اطلاعات';
        });
    };

    document.addEventListener('DOMContentLoaded', function () {
        var input = document.getElementById('chatbot-input');
        if (input) {
            input.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChatMessage(); }
            });
        }
    });
})();
