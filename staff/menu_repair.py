import io
import os

MENU_FILE = os.path.join('templates', 'admin-dashboard', 'base', 'header.html')

GROUPS = [
    ('مدیریت پروازها', 'can.flights.any', []),
    ('مدیریت مقاصد', 'can.destinations.any', []),
    ('مدیریت هتل ها', 'can.hotels.any', []),
    ('مدیریت تورها', 'can.tours.any or can.packages.any', [
        ('مدیریت پکیج', 'can.packages.any'),
        ('ایجاد تور', 'can.tours.add'),
        ('لیست تورها', 'can.tours.any'),
        ('منوی تور', 'can.tours.add'),
        ('لیست منوی تور', 'can.tours.any'),
        ('لیست دسته بندی ها', 'can.tours.any'),
        ('ایجاد دسته بندی جدید', 'can.tours.add'),
        ('کلیدهای API آژانس‌ها', 'can.settings.any'),
    ]),
    ('مجله گردشگری', 'can.blog.any', []),
    ('کامپوننت ها', 'can.pages.any or can.orders.any or can.reviews.any or can.memories.any or can.messages.any or can.visas.any or can.users.any or can.settings.any', [
        ('مدیریت صفحات', 'can.pages.any'),
        ('مدیریت فایل ها', 'can.pages.any'),
        ('رزرواسیون', 'can.orders.any'),
        ('سفارشات', 'can.orders.any'),
        ('درخواست اطلاع‌رسانی تور', 'can.tours.any'),
        ('نظرات مشتریان', 'can.reviews.any'),
        ('واحد پولی', 'can.settings.any'),
        ('بخش سفرنامه', 'can.memories.any'),
        ('صندوق پیام های ورودی', 'can.messages.any'),
        ('لیست مخاطبین', 'can.messages.any'),
        ('متن صفحه تمام تورها', 'can.settings.any'),
        ('پرسش و پاسخ صفحه اصلی', 'can.settings.any'),
        ('لیست درخواست های ویزا', 'can.visas.any'),
        ('مدیریت کاربران', 'can.users.any'),
    ]),
]

STAFF_ITEMS = [
    "{% if can.staff.any %}",
    '<li class="nk-menu-item">',
    "    <a href=\"{% url 'staff-list' %}\" class=\"nk-menu-link\"><span",
    '            class="nk-menu-text">کاربران پشتیبانی</span></a>',
    '</li>',
    '<li class="nk-menu-item">',
    "    <a href=\"{% url 'staff-change-log' %}\" class=\"nk-menu-link\"><span",
    '            class="nk-menu-text">تاریخچه تغییرات</span></a>',
    '</li>',
    '{% endif %}',
]


def _label_line(lines, label, start, stop):
    needle = 'nk-menu-text">%s<' % label
    for index in range(start, stop):
        if needle in lines[index]:
            return index
    return -1


def _item_start(lines, index):
    while index >= 0 and '<li' not in lines[index]:
        index -= 1
    return index


def _item_end(lines, start):
    depth = 0
    for index in range(start, len(lines)):
        depth += lines[index].count('<li') - lines[index].count('</li>')
        if depth == 0:
            return index
    return -1


def _already_wrapped(lines, start):
    index = start - 1
    while index >= 0 and not lines[index].strip():
        index -= 1
    return index >= 0 and lines[index].strip().startswith('{% if can.')


def _indent(line):
    return line[:len(line) - len(line.lstrip())]


def _wrap(lines, start, end, condition):
    indent = _indent(lines[start])
    lines.insert(end + 1, indent + '{% endif %}')
    lines.insert(start, indent + '{%% if %s %%}' % condition)


def repair(site_path):
    path = os.path.join(site_path, MENU_FILE)
    raw = io.open(path, 'rb').read().decode('utf-8')
    bom = raw.startswith('﻿')
    if bom:
        raw = raw[1:]
    eol = '\r\n' if '\r\n' in raw else '\n'
    lines = raw.replace('\r\n', '\n').split('\n')
    done = []

    users_line = -1
    for index, line in enumerate(lines):
        if "{% url 'user_list' %}" in line:
            users_line = index
            break
    if users_line < 0:
        raise RuntimeError('users menu not found in ' + MENU_FILE)

    if 'staff-list' not in raw:
        end = _item_end(lines, _item_start(lines, users_line))
        indent = _indent(lines[_item_start(lines, users_line)])
        block = [indent + item for item in STAFF_ITEMS]
        lines[end + 1:end + 1] = block
        done.append('staff menu items added')
    elif 'can.staff.any' not in raw:
        for index, line in enumerate(lines):
            if line.strip() == '{% if user.is_superuser %}' and 'staff-list' in '\n'.join(lines[index:index + 6]):
                lines[index] = _indent(line) + '{% if can.staff.any %}'
                done.append('staff menu condition fixed')
                break

    create_line = _label_line(lines, 'ایجاد کاربر', max(users_line - 12, 0), users_line + 12)
    if create_line >= 0:
        anchor = create_line
        while anchor >= 0 and '<a ' not in lines[anchor]:
            anchor -= 1
        if anchor >= 0 and 'href=' not in lines[anchor]:
            lines[anchor] = lines[anchor].replace('<a ', "<a href=\"{% url 'staff-create' %}\" ", 1)
            done.append('create user link added')

    wrapped = 0
    for label, condition, children in GROUPS:
        line = _label_line(lines, label, 0, len(lines))
        if line < 0:
            continue
        start = _item_start(lines, line)
        end = _item_end(lines, start)
        if start < 0 or end < 0:
            continue
        for child_label, child_condition in children:
            child_line = _label_line(lines, child_label, start, end)
            if child_line < 0:
                continue
            child_start = _item_start(lines, child_line)
            child_end = _item_end(lines, child_start)
            if child_start < 0 or child_end < 0 or _already_wrapped(lines, child_start):
                continue
            _wrap(lines, child_start, child_end, child_condition)
            wrapped += 1
            end = _item_end(lines, start)
        if not _already_wrapped(lines, start):
            _wrap(lines, start, _item_end(lines, start), condition)
            wrapped += 1
    if wrapped:
        done.append('%d menu sections gated' % wrapped)

    if not done:
        return 'menu already correct'
    text = ('﻿' if bom else '') + eol.join(lines)
    io.open(path, 'wb').write(text.encode('utf-8'))
    return ', '.join(done)


VISA_FILE = os.path.join('templates', 'layout', 'your-applications.html')
THAI_FILE = os.path.join('templates', 'layout', 'your-applications-thai.html')


def _if_above(lines, index):
    while index >= 0 and not lines[index].strip().startswith('{% if'):
        index -= 1
    return index


def _find(lines, needle, start=0):
    for index in range(start, len(lines)):
        if needle in lines[index]:
            return index
    return -1


def _read(path):
    raw = io.open(path, 'rb').read().decode('utf-8')
    bom = raw.startswith('\ufeff')
    if bom:
        raw = raw[1:]
    eol = '\r\n' if '\r\n' in raw else '\n'
    return raw, bom, eol


def _write(path, lines, bom, eol):
    text = ('\ufeff' if bom else '') + eol.join(lines)
    io.open(path, 'wb').write(text.encode('utf-8'))


def repair_visa_pages(site_path):
    done = []

    path = os.path.join(site_path, VISA_FILE)
    if os.path.exists(path):
        raw, bom, eol = _read(path)
        if 'can.visas' not in raw:
            lines = raw.replace('\r\n', '\n').split('\n')
            delete_cell = _find(lines, "{% url 'delete_visa_request'")
            gate = _if_above(lines, delete_cell)
            if delete_cell > 0 and gate > 0:
                lines[gate] = _indent(lines[gate]) + '{% if can.visas.delete %}'
                name_cell = _find(lines, 'item.user.get_full_name')
                start = name_cell
                while start > 0 and '<td>' not in lines[start]:
                    start -= 1
                stop = gate - 1
                while stop > start and '</td>' not in lines[stop]:
                    stop -= 1
                if start > 0 and stop > start:
                    indent = _indent(lines[start])
                    lines.insert(stop + 1, indent + '{% endif %}')
                    lines.insert(start, indent + '{% if can.visas.any %}')
                head = _find(lines, 'Applicant Name')
                head_gate = _if_above(lines, head)
                remove_head = _find(lines, 'Remove Request', head)
                if head_gate > 0 and remove_head > 0:
                    lines[head_gate] = _indent(lines[head_gate]) + '{% if can.visas.any %}'
                    indent = _indent(lines[remove_head])
                    lines.insert(remove_head, indent + '{% if can.visas.delete %}')
                    lines.insert(remove_head, indent + '{% endif %}')
                _write(path, lines, bom, eol)
                done.append('visa list columns')

    path = os.path.join(site_path, THAI_FILE)
    if os.path.exists(path):
        raw, bom, eol = _read(path)
        if 'can.visas' not in raw:
            lines = raw.replace('\r\n', '\n').split('\n')
            changed = 0
            for needle in ['Remove Request', "{% url 'delete_thai_visa_request'"]:
                target = _find(lines, needle)
                gate = _if_above(lines, target)
                if target > 0 and gate > 0 and 'is_superuser' in lines[gate]:
                    lines[gate] = _indent(lines[gate]) + '{% if can.visas.delete %}'
                    changed += 1
            if changed:
                _write(path, lines, bom, eol)
                done.append('thai visa columns')

    if not done:
        return 'visa pages already correct'
    return ', '.join(done)


FORM_FILE = os.path.join('templates', 'layout', 'form-2.html')
THAI_FORM_FILE = os.path.join('templates', 'layout', 'form-thai.html')

READONLY_NOTICE = [
    '{% if staff_readonly %}',
    '<div style="background:#fff6d9; border:1px solid #e0c97f; border-radius:8px; padding:12px 16px; margin:12px 0; font-weight:bold; text-align:center;">',
    '    شما فقط اجازه مشاهده این درخواست را دارید؛ امکان ثبت تغییرات وجود ندارد.',
    '</div>',
    '{% endif %}',
]


def _add_notice(lines):
    index = _find(lines, '<form method="POST"')
    if index < 0:
        return False
    indent = _indent(lines[index])
    lines[index + 1:index + 1] = [indent + item for item in READONLY_NOTICE]
    return True


def repair_visa_form(site_path):
    done = []

    path = os.path.join(site_path, FORM_FILE)
    if os.path.exists(path):
        raw, bom, eol = _read(path)
        if 'can.visas' not in raw:
            lines = raw.replace('\r\n', '\n').split('\n')
            status = _find(lines, 'name="req_stat"')
            gate = _if_above(lines, status)
            if status > 0 and gate > 0 and 'is_superuser' in lines[gate]:
                lines[gate] = _indent(lines[gate]) + '{% if can.visas.edit %}'
                done.append('visa form status fields')
            info = _find(lines, "{% url 'visa_pdf'")
            info_gate = _if_above(lines, info)
            if info > 0 and info_gate > 0 and 'is_superuser' in lines[info_gate]:
                lines[info_gate] = _indent(lines[info_gate]) + '{% if can.visas.any and item %}'
            if 'staff_readonly' not in raw:
                _add_notice(lines)
            _write(path, lines, bom, eol)

    path = os.path.join(site_path, THAI_FORM_FILE)
    if os.path.exists(path):
        raw, bom, eol = _read(path)
        if 'can.visas' not in raw:
            lines = raw.replace('\r\n', '\n').split('\n')
            changed = False
            for index, line in enumerate(lines):
                if line.strip() == '{% if request.user.is_superuser %}':
                    lines[index] = _indent(line) + '{% if can.visas.edit %}'
                    changed = True
                    break
            if 'staff_readonly' not in raw:
                changed = _add_notice(lines) or changed
            if changed:
                _write(path, lines, bom, eol)
                done.append('thai visa form')

    if not done:
        return 'visa form already correct'
    return ', '.join(done)


MSG_FILE = os.path.join('templates', 'ajax', 'ajax_msg_list.html')

MSG_TOOLBAR = """{% if can.messages.delete %}
<form method="post" action="{% url 'messages-bulk-delete' %}" id="msg-delete-form">
    {% csrf_token %}
    <input type="hidden" name="mode" value="selected" id="msg-delete-mode">
    <div class="msg-tools">
        <button type="submit" class="btn btn-outline-danger" data-mode="selected">حذف پیام های انتخاب شده</button>
        {% if allmsg.paginator.count %}
        <button type="submit" class="btn btn-danger" data-mode="all" data-count="{{ allmsg.paginator.count }}">حذف همه پیام ها ({{ allmsg.paginator.count }})</button>
        {% endif %}
    </div>
{% endif %}"""

MSG_SCRIPT = """{% if can.messages.delete %}
</form>
<style>
    .msg-tools{display:flex;gap:10px;justify-content:flex-end;margin:0 0 12px}
    #msg-delete-form input[type="checkbox"]{width:16px;height:16px;cursor:pointer}
</style>
<script>
    (function () {
        const form = document.getElementById('msg-delete-form');
        if (!form) {
            return;
        }
        const mode = document.getElementById('msg-delete-mode');
        const all = document.getElementById('msg-select-all');
        if (all) {
            all.addEventListener('change', function () {
                form.querySelectorAll('.msg-select').forEach(function (box) {
                    box.checked = all.checked;
                });
            });
        }
        form.querySelectorAll('button[data-mode]').forEach(function (button) {
            button.addEventListener('click', function (event) {
                if (button.dataset.mode === 'all') {
                    if (!confirm('همه ' + button.dataset.count + ' پیام حذف شود؟')) {
                        event.preventDefault();
                        return;
                    }
                    mode.value = 'all';
                    return;
                }
                const count = form.querySelectorAll('.msg-select:checked').length;
                if (!count) {
                    event.preventDefault();
                    alert('هیچ پیامی انتخاب نشده است');
                    return;
                }
                if (!confirm(count + ' پیام انتخاب شده حذف شود؟')) {
                    event.preventDefault();
                    return;
                }
                mode.value = 'selected';
            });
        });
    })();
</script>
{% endif %}"""

MSG_CHECKBOX_CELL = '<td class="TbCells"><input type="checkbox" name="ids" value="{{ message.id }}" class="msg-select"></td>'
MSG_CHECKBOX_HEAD = '<th class="TbHead"><input type="checkbox" id="msg-select-all" title="انتخاب همه"></th>'


def repair_messages_list(site_path):
    path = os.path.join(site_path, MSG_FILE)
    if not os.path.exists(path):
        return 'messages list not found'
    raw, bom, eol = _read(path)
    if 'msg-delete-form' in raw:
        return 'messages list already correct'
    lines = raw.replace('\r\n', '\n').split('\n')

    delete_link = _find(lines, "{% url 'message_delete'")
    if delete_link > 0:
        indent = _indent(lines[delete_link])
        lines[delete_link:delete_link + 1] = [
            indent + '{% if can.messages.delete %}',
            lines[delete_link],
            indent + '{% else %}',
            indent + '-',
            indent + '{% endif %}',
        ]

    table = _find(lines, '<table class="table BranchTable">')
    head = _find(lines, 'TbHead">ردیف<')
    cell = _find(lines, 'TbCells serial">')
    close = _find(lines, '</table>')
    if min(table, head, cell, close) < 0:
        return 'messages list layout not recognised'

    lines[close + 1:close + 1] = MSG_SCRIPT.split('\n')

    indent = _indent(lines[cell])
    lines[cell:cell] = [
        indent + '{% if can.messages.delete %}',
        indent + MSG_CHECKBOX_CELL,
        indent + '{% endif %}',
    ]

    indent = _indent(lines[head])
    lines[head:head] = [
        indent + '{% if can.messages.delete %}',
        indent + MSG_CHECKBOX_HEAD,
        indent + '{% endif %}',
    ]

    lines[table:table] = MSG_TOOLBAR.split('\n')
    _write(path, lines, bom, eol)
    return 'messages bulk delete added'


HEAD_FILE = os.path.join('templates', 'admin-dashboard', 'base', 'head.html')

HEAD_LINES = [
    '<link rel="stylesheet" href="/static/assets/css/staff-mobile.css">',
    '<script src="/static/assets/js/staff-mobile.js" defer></script>',
]


def repair_dashboard_head(site_path):
    path = os.path.join(site_path, HEAD_FILE)
    if not os.path.exists(path):
        return 'dashboard head not found'
    raw, bom, eol = _read(path)
    if 'staff-mobile.css' in raw:
        return 'dashboard head already correct'
    lines = raw.replace('\r\n', '\n').split('\n')
    anchor = -1
    for index, line in enumerate(lines):
        if 'rel=' + chr(34) + 'stylesheet' + chr(34) in line:
            anchor = index
    if anchor < 0:
        anchor = _find(lines, 'viewport')
    if anchor < 0:
        anchor = len(lines) - 1
    lines[anchor + 1:anchor + 1] = HEAD_LINES
    _write(path, lines, bom, eol)
    return 'mobile styles linked'


LOGIN_FILE = os.path.join('templates', 'person', 'login.html')

LOGIN_STYLE = """    <style>
        @media (max-width: 767.98px) {
            body {
                overflow-x: hidden;
            }

            .container.login_page {
                width: auto !important;
                max-width: 100%;
                margin: 40px 16px;
                padding: 24px 18px;
                border-radius: 14px;
                box-shadow: 0 6px 24px rgba(0, 0, 0, .08);
            }

            .login_image_ {
                text-align: center;
                margin-bottom: 18px;
            }

            .login_image_ img {
                position: static !important;
                max-width: 170px;
                height: auto;
            }

            .login_form_ {
                margin: 0 !important;
            }

            .login_form_ input {
                width: 100% !important;
                box-sizing: border-box;
                height: 44px;
                font-size: 15px;
            }

            .login_form_ .login-btn {
                width: 100% !important;
                height: 46px;
                font-size: 16px;
            }
        }
    </style>"""


def repair_login_page(site_path):
    path = os.path.join(site_path, LOGIN_FILE)
    if not os.path.exists(path):
        return 'login page not found'
    raw, bom, eol = _read(path)
    done = []
    lines = raw.replace('\r\n', '\n').split('\n')

    meta = _find(lines, 'name="viewport"')
    if meta >= 0 and 'width=device-width' not in lines[meta]:
        indent = _indent(lines[meta])
        lines[meta] = indent + '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        done.append('viewport fixed')

    if 'max-width: 767.98px' not in raw:
        anchor = _find(lines, '<title')
        if anchor < 0:
            anchor = _find(lines, '</head>')
        if anchor >= 0:
            lines[anchor:anchor] = LOGIN_STYLE.split('\n')
            done.append('mobile styles added')

    if not done:
        return 'login page already correct'
    _write(path, lines, bom, eol)
    return ', '.join(done)
