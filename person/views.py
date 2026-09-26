import random
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from aps import settings
from tour.views.views_tour import superuser_required
from visa.forms import visa_request_form, thaiVisaForm
from visa.models import visa_request_item, ThaiVisa
from staff.access import user_can
from .forms import LoginForm
from .models import person_profile, profile
from wallet.models import wallet


def LoginPage(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            formusername = forms.cleaned_data['Username']
            formpassword = forms.cleaned_data['Password']
            x = authenticate(username=formusername, password=formpassword)
            if x:
                login(request, x)
                return redirect('/dashboard/')
    context = {'form': forms}
    return render(request, "person/login.html", context)


def LogoutPage(request):
    logout(request)
    return redirect('/')

def create_user(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    agancy_name = request.POST.get('agancy_name')
    mobile_number = request.POST.get('mobile_number')
    otp = random.randint(10000, 99999)
    if request.method == 'POST':
        if not first_name and not last_name and not mobile_number:
            messages.warning(request, 'نام، نام خانوادگی و شماره موبایل الزامیست')
            return redirect('create_user')
        if User.objects.filter(username=mobile_number):
            url = 'http://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber'
            payload = {
                'username': 'arezooyesafar',
                'password': 'Mm@1361n',
                'to': mobile_number,
                'bodyId': 180225,
                'text': otp,
            }
            prof = profile.objects.get(user=User.objects.get(username=mobile_number))
            prof.otp_code = otp
            prof.save()
            response = requests.request('POST', url, data=payload)
            return redirect('varify_otp_login', User.objects.get(username=mobile_number).id)
        new_user = User.objects.create_user(username=mobile_number, first_name=first_name, last_name=last_name)
        password = User.objects.make_random_password()
        new_user.set_password(password)
        new_user.save()
        new_profile = profile.objects.create(user=new_user, otp_code=otp, agancy_name=agancy_name)
        new_profile.save()
        url = 'http://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber'
        payload = {
            'username': 'arezooyesafar',
            'password': 'Mm@1361n',
            'to': mobile_number,
            'bodyId': 180225,
            'text': otp,
        }
        response = requests.request('POST', url, data=payload)
        return redirect('varify_otp', new_user.id)
    return render(request, 'layout/sign-up.html')

def varify_otp(request, id):
    user = User.objects.get(id=id)
    prof = profile.objects.get(user=user)
    otp = request.POST.get('otp_user')
    if request.method == 'POST':
        if  otp == prof.otp_code:
            user.is_active = True
            user.save()
            messages.success(request, 'حساب کاربری با موفقیت ایجاد شد. برای ورود شماره موبایل خود را وارد کنید.')
            return redirect('otp_login')
        else:
            otp = random.randint(10000, 99999)
            prof.otp_code = otp
            prof.save()
            url = 'http://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber'
            payload = {
                'username': 'arezooyesafar',
                'password': 'Mm@1361n',
                'to': user.username,
                'bodyId': 180225,
                'text': otp,
            }
            response = requests.request('POST', url, data=payload)
            messages.warning(request, 'کد اعتبار سنجی وارد شده صحیح نمیباشد')
            return redirect('varify_otp', user.id)
    return render(request, 'layout/varify_otp_login.html')

@login_required(login_url='otp_login')
def visa_panel(request, id):
    user = User.objects.get(id=id)
    prof = profile.objects.get(user=user)
    context = {
        'user_info': user,
        'prof': prof,
    }
    return render(request, 'layout/panel.html', context)

def otp_login(request):
    mobile = request.POST.get('mobile_number')
    if request.method == 'POST':
        if not User.objects.filter(username=mobile):
            messages.warning(request, 'حساب کاربری با این شماره پیدا نشد.')
            return redirect('otp_login')
        otp = random.randint(10000, 99999)
        url = 'http://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber'
        payload = {
            'username': 'arezooyesafar',
            'password': 'Mm@1361n',
            'to': mobile,
            'bodyId': 180225,
            'text': otp,
        }
        response = requests.request('POST', url, data=payload)
        user = User.objects.get(username=mobile)
        prof = profile.objects.get(user=user)
        prof.otp_code = otp
        prof.save()
        return redirect('varify_otp_login', user.id)
    return render(request, 'layout/sign-in.html')

def varify_otp_login(request, id):
    user = User.objects.get(id=id)
    prof = profile.objects.get(user=user)
    if request.method == 'POST':
        otp = request.POST.get('otp_user')
        if otp == prof.otp_code:
            if user:
                login(request, user)
                return redirect('visa_country', user.id)
        else:
            otp = random.randint(10000, 99999)
            prof.otp_code = otp
            prof.save()
            url = 'http://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber'
            payload = {
                'username': 'arezooyesafar',
                'password': 'Mm@1361n',
                'to': user.username,
                'bodyId': 180225,
                'text': otp,
            }
            response = requests.request('POST', url, data=payload)
            messages.warning(request, 'کد اعتبار سنجی وارد شده صحیح نمیباشد')
            return redirect('varify_otp_login', user.id)
    return render(request, 'layout/varify_otp_login.html')

@login_required(login_url='otp_login')
def profile_view(request):
    user = User.objects.get(id=request.user.id)
    prof = profile.objects.get(user=request.user)
    context = {
        'user_info': user,
        'prof': prof
    }
    return render(request, 'layout/your-profile.html', context)

@login_required(login_url='otp_login')
def visa_list(request):
    user = request.user
    prof, _ = profile.objects.get_or_create(user=user)

    # 1) ساختن کوئری پایه
    if user_can(user, 'visas', 'view'):
        qs = visa_request_item.objects.all()
    else:
        qs = visa_request_item.objects.filter(user=user.id)

    qs = qs.order_by('-id')

    # 2) گرفتن مقدار سرچ از GET و فیلتر
    search_query = (request.GET.get('search') or '').strip()
    if search_query:
        # اگر trs_number از نوع CharField است:
        qs = qs.filter(trs_number__icontains=search_query)

        # اگر trs_number از نوع عددی (Integer/BigInteger) است، به‌جایش این را بگذار:
        # if search_query.isdigit():
        #     qs = qs.filter(trs_number=int(search_query))
        # else:
        #     qs = qs.none()

    # 3) صفحه‌بندی (بعد از فیلتر)
    paginator = Paginator(qs, 10 if user.is_superuser else 20)
    page_number = request.GET.get('page')
    all_items = paginator.get_page(page_number)

    context = {
        'all_items': all_items,
        'prof': prof,
        'user': user,
        'search_query': search_query,  # برای استفاده در تمپلیت
    }
    return render(request, 'layout/your-applications.html', context)

@login_required(login_url='otp_login')
def update_visa_request(request, id):
    item = visa_request_item.objects.get(id=id)
    visa_manager = user_can(request.user, 'visas', 'edit')
    if not visa_manager:
        forms = visa_request_form(instance=item)
        if request.method == 'POST':
            forms = visa_request_form(request.POST, request.FILES, instance=item)
            if forms.is_valid():
                data = forms.save(commit=False)
                data.gender = request.POST.get('gender')
                marial_stat = request.POST.get('marial')
                if marial_stat == 'yes':
                    data.marial_stat = True
                if marial_stat == 'no':
                    data.marial_stat = False
                if request.POST.get('russia') == 'yes':
                    data.russia_relative_stat = True
                if request.POST.get('russia') == 'no':
                    data.russia_relative_stat = False
                if request.POST.get('highschool') == 'yes':
                    data.uni_degree_stat = True
                if request.POST.get('highschool') == 'no':
                    data.uni_degree_stat = False
                data.save()
                return redirect('visa_list')
        context = {
            'forms': forms,
            'item': item,
            'meta_robots':'NOINDEX,FOLLOW'
        }
        return render(request, 'layout/form-2.html', context)
    if visa_manager:
        forms = visa_request_form(instance=item)
        if request.method == 'POST':
            sex = request.POST.get('sex')
            forms = visa_request_form(request.POST, request.FILES, instance=item)
            if forms.is_valid():
                data = forms.save(commit=False)
                data.gender = request.POST.get('gender')
                marial_stat = request.POST.get('marial')
                data.req_stat = request.POST.get('req_stat')
                if request.POST.get('payment_stat') == 'Pending':
                    data.payment_stat = False
                if request.POST.get('payment_stat') == 'Paid':
                    data.payment_stat = True
                if marial_stat == 'yes':
                    data.marial_stat = True
                if marial_stat == 'no':
                    data.marial_stat = False
                if request.POST.get('russia') == 'yes':
                    data.russia_relative_stat = True
                if request.POST.get('russia') == 'no':
                    data.russia_relative_stat = False
                if request.POST.get('highschool') == 'yes':
                    data.uni_degree_stat = True
                if request.POST.get('highschool') == 'no':
                    data.uni_degree_stat = False
                data.save()
                if data.req_stat == 'Confirmed':
                    data.confirmed = True
                    data.save()
                return redirect('visa_list')
        context = {
            'forms': forms,
            'item': item,
            'meta_robots':'NOINDEX,FOLLOW'
        }
        return render(request, 'layout/form-2.html', context)
    return redirect('thai_visa_list')

@login_required(login_url='otp_login')
def visa_country(request, id):
    user = User.objects.get(id=id)
    prof = profile.objects.get(user=user)
    context = {
        'user_info': user,
        'prof': prof,
    }
    return render(request, 'layout/country-select.html', context)

@login_required(login_url='otp_login')
def thai_visa_panel(request, id):
    user = User.objects.get(id=id)
    prof = profile.objects.get(user=user)
    context = {
        'user_info': user,
        'prof': prof,
    }
    return render(request, 'layout/panel-thai.html', context)


@login_required(login_url='otp_login')
def thai_visa_list(request):
    if user_can(request.user, 'visas', 'view'):
        user = User.objects.get(id=request.user.id)
        prof, _ = profile.objects.get_or_create(user=user)
        all_items = ThaiVisa.objects.all().order_by('-id')
        paginator = Paginator(all_items, 20)
        pagenumber = request.GET.get('page')
        all_items = paginator.get_page(pagenumber)
        context = {
            'all_items': all_items,
            'prof':prof,
            'user': user
        }
        return render(request, 'layout/your-applications-thai.html', context)
    else:
        user = User.objects.get(id=request.user.id)
        prof, _ = profile.objects.get_or_create(user=user)
        all_items = ThaiVisa.objects.filter(user=request.user.id).order_by('-id')
        paginator = Paginator(all_items, 20)
        pagenumber = request.GET.get('page')
        all_items = paginator.get_page(pagenumber)
        context = {
            'all_items':all_items,
            'prof': prof,
            'user': user
        }
        return render(request, 'layout/your-applications-thai.html', context)

@login_required(login_url='otp_login')
def update_thai_visa_request(request, id):
    item = ThaiVisa.objects.get(id=id)
    visa_manager = user_can(request.user, 'visas', 'edit')
    if not visa_manager:
        forms = thaiVisaForm(instance=item)
        if request.method == 'POST':
            forms = thaiVisaForm(request.POST, request.FILES, instance=item)
            if forms.is_valid():
                data = forms.save(commit=False)
                payment_stat = request.POST.get('payment_stat')
                male = request.POST.get('gender1')
                female = request.POST.get('gender2')
                if male:
                    data.gender = "Male"
                if female:
                    data.gender = "Female"
                single = request.POST.get('marial1')
                maried = request.POST.get('marial2')
                if single:
                    data.marial_stat = False
                if maried:
                    data.marial_stat = True
                owner = request.POST.get('owner1')
                employee = request.POST.get('owner2')
                if owner:
                    data.job_owner = True
                if employee:
                    data.job_owner = False
                tripthai_yes = request.POST.get('tripthai1')
                tripthai_no = request.POST.get('tripthai12')
                if tripthai_yes:
                    data.thai_trip = True
                if tripthai_no:
                    data.thai_trip = False
                thaiapply_yes = request.POST.get('thaiapply1')
                thaiapply_no = request.POST.get('thaiapply2')
                if thaiapply_yes:
                    data.thai_applied = True
                if thaiapply_no:
                    data.thai_applied = False
                if payment_stat == 'Pending':
                    data.payment_stat = False
                if payment_stat == 'Paid':
                    data.payment_stat = True
                data.save()
                return redirect('thai_visa_list')
        context = {
            'forms': forms,
            'item': item,
        }
        return render(request, 'layout/form-thai.html', context)
    if visa_manager:
        forms = thaiVisaForm(instance=item)
        if request.method == 'POST':
            forms = thaiVisaForm(request.POST, request.FILES, instance=item)
            if forms.is_valid():
                data = forms.save(commit=False)
                payment_stat = request.POST.get('payment_stat')
                male = request.POST.get('gender1')
                female = request.POST.get('gender2')
                if male:
                    data.gender = "Male"
                if female:
                    data.gender = "Female"
                single = request.POST.get('marial1')
                maried = request.POST.get('marial2')
                if single:
                    data.marial_stat = False
                if maried:
                    data.marial_stat = True
                owner = request.POST.get('owner1')
                employee = request.POST.get('owner2')
                if owner:
                    data.job_owner = True
                if employee:
                    data.job_owner = False
                tripthai_yes = request.POST.get('tripthai1')
                tripthai_no = request.POST.get('tripthai12')
                if tripthai_yes:
                    data.thai_trip = True
                if tripthai_no:
                    data.thai_trip = False
                thaiapply_yes = request.POST.get('thaiapply1')
                thaiapply_no = request.POST.get('thaiapply2')
                if thaiapply_yes:
                    data.thai_applied = True
                if thaiapply_no:
                    data.thai_applied = False
                if payment_stat == 'Pending':
                    data.payment_stat = False
                if payment_stat == 'Paid':
                    data.payment_stat = True
                data.req_stat = request.POST.get('req_stat')
                data.save()
                return redirect('thai_visa_list')
        context = {
            'forms': forms,
            'item': item,
        }
        return render(request, 'layout/form-thai.html', context)
    return redirect('thai_visa_list')

@login_required(login_url='otp_login')
def visa_list_admin(request):
    user = request.user
    prof, _ = profile.objects.get_or_create(user=user)
    all_items = visa_request_item.objects.all().order_by('-id')
    paginator = Paginator(all_items, 30)
    pagenumber = request.GET.get('page')
    all_items = paginator.get_page(pagenumber)
    context = {
        'all_items': all_items,
        'prof': prof,
        'user': user,
        'search_query': '',
    }
    return render(request, 'layout/your-applications.html', context)

@login_required(login_url='otp_login')
def visa_view(request, id):
    item = visa_request_item.objects.get(id=id)
    context = {
        'item': item
    }
    return render(request, 'layout/form-details.html', context)

@login_required(login_url='otp_login')
def delete_visa_request(request, id):
    if request.user.is_superuser:
        item = visa_request_item.objects.get(id=id)
        item.delete()
        return redirect('visa_list')
    
@login_required(login_url='otp_login')
def delete_thai_visa_request(request, id):
    if request.user.is_superuser:
        item = ThaiVisa.objects.get(id=id)
        item.delete()
        return redirect('thai_visa_list')

@login_required(login_url='login')
def user_profile(request,id):
    user = User.objects.get(id=id)
    prof, _ = person_profile.objects.get_or_create(user=user)
    first_name = request.POST.get('first_name')
    username = request.POST.get('username')
    last_name = request.POST.get('last_name')
    proviance = request.POST.get('proviance')
    city = request.POST.get('city')
    address = request.POST.get('address')
    if request.method == 'POST':
        user.first_name = first_name
        user.last_name = last_name
        old_user = User.objects.filter(username=username)
        if old_user.count() != 0:
            old_user = User.objects.get(username=username)
            if old_user.id != request.user.id:
                messages.warning(request, 'نام کاربری در سیستم ثبت شده است.')
                return redirect('user_profile', user.id)
        user.username = username
        prof.provinace = proviance
        prof.city = city
        prof.adress = address
        user.save()
        prof.save()
        messages.success(request, 'تغییرات با موفقیت در سیستم ثبت شد.')
        return redirect('user_profile', user.id)
    context = {
        'data':user,
        'info': prof
    }
    if request.user_agent.is_mobile:
        return render(request, 'ui/mobile/user_profile.html', context)
    else:
        return render(request, 'ui/user_profile.html', context)

@login_required(login_url='login')
def user_list(request):
    data = User.objects.all()
    paginator = Paginator(data, 25)
    pagenumber = request.GET.get('page')
    data = paginator.get_page(pagenumber)
    context = {
        'data':data
    }
    return render(request, 'person/user_list.html', context)

@login_required(login_url='login')
def user_profile_update(request,id):
    user = User.objects.get(id=id)
    prof, _ = person_profile.objects.get_or_create(user=user)
    first_name = request.POST.get('first_name')
    username = request.POST.get('username')
    last_name = request.POST.get('last_name')
    proviance = request.POST.get('proviance')
    city = request.POST.get('city')
    address = request.POST.get('address')
    if request.method == 'POST':
        user.first_name = first_name
        user.last_name = last_name
        old_user = User.objects.filter(username=username)
        if old_user.count() != 0:
            old_user = User.objects.get(username=username)
            if old_user.id != request.user.id:
                messages.warning(request, 'نام کاربری در سیستم ثبت شده است.')
                return redirect('user_profile_update', user.id)
        user.username = username
        prof.provinace = proviance
        prof.city = city
        prof.adress = address
        user.save()
        prof.save()
        messages.success(request, 'تغییرات با موفقیت در سیستم ثبت شد.')
        return redirect('user_profile_update', user.id)
    context = {
        'data':user,
        'info': prof
    }
    return render(request, 'person/user_update.html', context)

@login_required(login_url='login')
def delete_user(request, id):
    user = User.objects.filter(id=id, is_superuser=False).first()
    if user:
        user.delete()
        messages.success(request, 'کاربر حذف شد.')
    return redirect('user_list')

@login_required(login_url='login')
def reset_password_admin(request, id):
    user = User.objects.get(id=id)
    pass1 = request.POST.get('password1')
    pass2 = request.POST.get('password2')
    if request.method == 'POST':
        if pass1 != pass2:
            messages.warning(request, 'کلمه عبور وارد شده یکسان نیست')
            return redirect('reset_password_admin', user.id)
        user.set_password(pass1)
        user.save()
        return redirect('user_list')
    context = {
        'user_data': user
    }
    return render(request, 'person/reset_password.html', context)

# @superuser_required(login_url='login')
# def add_reseller_profile(request, id):
#     user= User.objects.get(id=id)
#     agancy_code = random.randint(100000, 999999)
#     agancy_code = f'AG-{agancy_code}'
#     forms = reseller_prof_form()
#     if request.method == 'POST':
#         forms = reseller_prof_form(request.POST, request.FILES)
#         if forms.is_valid():
#             reseller = forms.save(commit=False)
#             reseller.user = user
#             reseller.reseller_code = agancy_code
#             reseller.save()
#             return redirect('user_list')
#     else:
#         context = {
#             'forms': forms
#         }
#         return render(request, 'person/add-reseller-profile.html', context)
#
# @superuser_required(login_url='login')
# def update_reseller_profile(request, id):


# from django.contrib.auth import get_user_model
# def rest_password(u, password):
#     try:
#         user = get_user_model().objects.get(username=u)
#     except:
#         return 'کاربر پیدا نشد'
#     user.set_password(password)
#     user.save()
#     return 'رمز با موفقیت تغییر یافت'

# rest_password('admin', '09122714808n@')