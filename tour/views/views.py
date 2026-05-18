from blog.dataset import get_all_blog_posts, get_all_blog_cats
from hotels.forms import CreateHotelMenuForm
from hotels.models import Hotel_Menu
from tour.dataset import *
from django.contrib import messages
from django.shortcuts import render, redirect
from tour.forms import *
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from tour.pms_manager import *


@superuser_required(login_url='login')
def Dashboard(request):
    hotellist = get_all_hotels().count()
    gte_hotels = get_all_gte_hotels()
    prc_hotels = get_all_price_hotels().count
    tourlist = get_all_pub_tours_admin()
    alltours = get_all_tours().count()
    unpub_tours = get_all_unpub_tours().count()
    posts = get_all_blog_posts()
    cats = get_all_blog_cats().count()
    pub_post = get_all_blog_posts().filter(Publish=True).count()
    views = viewCounter.objects.get(id=1)
    user = request.user.id
    user = User.objects.get(id=user)
    airlinelist = AirLineData.objects.all().order_by('-id')
    packagelist = Package.objects.all()
    context = {
        'Packages': packagelist,
        'Tours': tourlist,
        'alltours': alltours,
        'unpub_tours': unpub_tours,
        'Hotels': hotellist,
        'gte_hotels': gte_hotels,
        'prc_hotels': prc_hotels,
        'posts': posts,
        'top_post': posts.order_by('-viewCount')[:4],
        'new_post': posts.order_by('-id')[:4],
        'low_post': posts.order_by('viewCount')[:4],
        'cats': cats,
        'pub_post': pub_post,
        'Airlines': airlinelist,
        'UserInfo': user,
        'Views': views
    }
    return render(request, 'admin-dashboard/dashboard.html', context)


# Hotel Menu CRUD
@superuser_required(login_url='login')
def CreateHotelMenu(request):
    forms = CreateHotelMenuForm()
    if request.method == 'POST':
        forms = CreateHotelMenuForm(request.POST)
        if forms.is_valid():
            forms.save()
            menus = Hotel_Menu.objects.all()
            context = {
                'form': forms,
                'Data': menus
            }
            return render(request, 'hotel/create-hotel-menu.html', context)
        else:
            menus = Hotel_Menu.objects.all()
            message = messages.error(request, 'به منظور ذخیره اطلاعات ایرلاین لطفا تمام فیلدها را تکمیل نمایید')
            context = {
                'form': forms,
                'message': message,
                'Data': menus
            }
            return render(request, 'hotel/create-hotel-menu.html', context)
    menus = Hotel_Menu.objects.all()
    context = {
        'form': forms,
        'Data': menus
    }
    return render(request, 'hotel/create-hotel-menu.html', context)


@superuser_required(login_url='login')
def UpdateHotelMenu(request, id):
    menu = Hotel_Menu.objects.get(id=id)
    forms = CreateHotelMenuForm(instance=menu)
    if request.method == 'POST':
        forms = CreateHotelMenuForm(request.POST, instance=menu)
        if forms.is_valid():
            forms.save()
            menus = Hotel_Menu.objects.all()
            return redirect('create-hotel-menu')
        else:
            menus = Hotel_Menu.objects.all()
            message = messages.error(request, 'به منظور ذخیره اطلاعات ایرلاین لطفا تمام فیلدها را تکمیل نمایید')
            context = {
                'form': forms,
                'message': message,
                'Data': menus
            }
            return render(request, 'hotel/create-hotel-menu.html', context)
    menus = Hotel_Menu.objects.all()
    context = {
        'form': forms,
        'Data': menus
    }
    return render(request, 'hotel/create-hotel-menu.html', context)


@superuser_required(login_url='login')
def DeleteHotelMenu(request, id):
    menu = Hotel_Menu.objects.get(id=id)
    menu.delete()
    return redirect('create-hotel-menu')


# Order Functions
@superuser_required(login_url='login')
def OrderUpdate(request, id):
    order = TourOrder.objects.get(id=id)
    docs = OrderDoc.objects.filter(ordernum=order)
    ordertime = order.OrderTime
    forms = orderUpdateForm(instance=order)
    if request.method == 'POST':
        forms = orderUpdateForm(request.POST, request.FILES, instance=order)
        if forms.is_valid():
            orup = forms.save(commit=False)
            orup.OrderTime = ordertime
            orup.OrderPack = order.OrderPack
            orup.save()
            return redirect('order-list')
    context = {
        'Form': forms,
        'Order': order,
        'docs': docs
    }
    return render(request, 'tour/order-update.html', context)


@superuser_required(login_url='login')
def OrderDelete(request, id):
    order = TourOrder.objects.get(id=id)
    order.delete()
    return redirect('order-list')


@superuser_required(login_url='login')
def OrderInbox(request):
    orders = TourOrder.objects.all()
    paginator = Paginator(orders, 15)
    PageNumber = request.GET.get('page')
    orderList = paginator.get_page(PageNumber)
    context = {
        'OrderList': orderList
    }
    return render(request, 'tour/order-list.html', context)




def PMemoriesCreate(request):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    memories = PMemories.objects.filter(publish=True).order_by('-id')
    spacialTours = get_spacial_tours()
    paginator = Paginator(memories, 15)
    PageNumber = request.GET.get('page')
    memories = paginator.get_page(PageNumber)
    forms = PMemoriesForm()
    if request.method == 'POST':
        forms = PMemoriesForm(request.POST)
        if forms.is_valid():
            memo = forms.save()
            message_text = f"کاربر گرامی {memo.Name} {memo.Family} سفرنامه شما با موفقیت ثبت گردید."
            message = messages.success(request, message_text)
            return redirect('memories')
    forms2 = SubscribeForm()
    if request.method == 'POST':
        forms = SubscribeForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('/')
    categories = MemoryCategory.objects.all()
    ch_categories = MemoryCategory.objects.exclude(parentCat=None)
    ch_cat_number = []
    for i in categories:
        ch_cat_number.append(MemoryCategory.objects.filter(parentCat=i).count())
    parent_categories = zip(categories, ch_cat_number)
    
    if PageNumber and int(PageNumber) > 1:
        meta_robots = 'NOINDEX,FOLLOW'
    else:
        meta_robots = 'INDEX,FOLLOW'

    context = {
        'Form': forms,
        'Memories': memories,
        'Sub': forms2,
        'pubTours': spacialTours,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'ch_categories': ch_categories,
        'categories': parent_categories,
        'meta_robots': meta_robots
    }
    return render(request, 'ui/memories.html', context)

def memoriesSubmit(request, id):
    memories = PMemories.objects.filter(publish=True)
    paginator = Paginator(memories, 15)
    PageNumber = request.GET.get('page')
    memories = paginator.get_page(PageNumber)
    menus = Country.objects.filter(showInMenu=True)
    memo = PMemories.objects.get(id=id)
    footer = Footer.objects.all()
    categories = PostCategory.objects.all()
    hotels = Hotel_Data.objects.all()
    hotelcities = []
    for i in hotels:
        hotelcities.append(City.objects.get(Name=i.Hcity))
    hotelcities = City.objects.filter(showInMenu=True)
    hotelcities = list(dict.fromkeys(hotelcities))
    spacialtours = Tour.objects.filter(Feature=True, PubTour=True)
    packages = []
    for i in spacialtours:
        packages.append(Package.objects.filter(TourName=i.id))
    spacialdata = zip(spacialtours, packages)
    forms2 = SubscribeForm()
    if request.method == 'POST':
        forms2 = SubscribeForm(request.POST)
        if forms2.is_valid():
            forms2.save()
            return redirect('/')
    context = {
        'AllCat': categories,
        'Form': forms,
        'Memo': memo,
        'Footer': footer,
        'Sub': forms2,
        'Menus': menus,
        'SpacialData': spacialdata,
        'hmenu': hotelcities,
        'Memories': memories
    }
    return render(request, 'ui/submit-memo.html', context)

@superuser_required(login_url='login')
def MemoriesList(request):
    return render(request, 'tour/memo-list.html')

@superuser_required(login_url='login')
def memoriesCreate(request):
    forms = PMemoriesForm()
    if request.method == 'POST':
        forms = PMemoriesForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('memo-list')
    context = {
        'Form': forms,
    }
    return render(request, 'tour/memo-update.html', context)

@superuser_required(login_url='login')
def memoriesUpdate(request, id):
    memo = PMemories.objects.get(id=id)
    forms = PMemoriesForm(instance=memo)
    if request.method == 'POST':
        forms = PMemoriesForm(request.POST, request.FILES, instance=memo)
        if forms.is_valid():
            forms.save()
            return redirect('memo-list')
    context = {
        'Form': forms,
        'data': memo
    }
    return render(request, 'tour/memo-update.html', context)


@superuser_required(login_url='login')
def memoriesDelete(request, id):
    memo = PMemories.objects.get(id=id)
    memo.delete()
    return redirect('memo-list')

## Memory Category CRUD Functions
@superuser_required(login_url='login')
def CreateMemoryCategory(request):
    forms = CreateMemoryCategoryForm()
    if request.method == 'POST':
        forms = CreateMemoryCategoryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('memo-category-list')
    context = {
        'form': forms
    }
    return render(request, 'tour/create-memo-category.html', context)

@superuser_required(login_url='login')
def UpdateMemoryCategory(request, id):
    category = MemoryCategory.objects.get(id=id)
    forms = CreateMemoryCategoryForm(instance=category)
    if request.method == 'POST':
        forms = CreateMemoryCategoryForm(request.POST, instance=category)
        if forms.is_valid():
            forms.save()
            return redirect('memo-category-list')
    context = {
        'form': forms
    }
    return render(request, 'tour/create-memo-category.html', context)

@superuser_required(login_url='login')
def DeleteMemoryCategory(request, id):
    category = MemoryCategory.objects.get(id=id)
    category.delete()
    return redirect('memo-category-list')

@superuser_required(login_url='login')
def MemoCategoryList(request):
    return render(request, 'tour/memo-category-list.html')

@superuser_required(login_url='login')
def TourMenuCreate(request):
    form = TourMenuForm()
    if request.method == 'POST':
        form = TourMenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tour-menu-list')
    context = {
        'form': form
    }
    return render(request, 'tour/create-menu.html', context)


@superuser_required(login_url='login')
def TourMenuUpdate(request, id):
    menu = TourMenu.objects.get(id=id)
    form = TourMenuForm(instance=menu)
    if request.method == 'POST':
        form = TourMenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('tour-menu-list')
    context = {
        'form': form
    }
    return render(request, 'tour/create-menu.html', context)


@superuser_required(login_url='login')
def TourMenuDelet(request, id):
    menu = TourMenu.objects.get(id=id)
    menu.delete()
    return redirect('tour-menu-list')


@superuser_required(login_url='login')
def TourMenuList(request):
    menus = TourMenu.objects.all()
    paginator = Paginator(menus, 10)
    pageNumber = request.GET.get('page')
    menus = paginator.get_page(pageNumber)
    context = {
        'Menus': menus
    }
    return render(request, 'tour/menu-list.html', context)

## Custom Tour Category CRUD Functions
@superuser_required(login_url='login')
def CreateTourCategory(request):
    forms = CreateTourCategoryForm()
    if request.method == 'POST':
        forms = CreateTourCategoryForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('list-tour-category')
    context = {
        'form': forms
    }
    return render(request, 'tour/create-tour-category.html', context)

@superuser_required(login_url='login')
def UpdateTourCategory(request, id):
    category = CustomTourCategory.objects.get(id=id)
    forms = CreateTourCategoryForm(instance=category)
    if request.method == 'POST':
        forms = CreateTourCategoryForm(request.POST, request.FILES, instance=category)

        if forms.is_valid():
            forms.save()
            return redirect('list-tour-category')
    context = {
        'form': forms
    }
    return render(request, 'tour/create-tour-category.html', context)

@superuser_required(login_url='login')
def DeleteTourCategory(request, id):
    category = CustomTourCategory.objects.get(id=id)
    category.delete()
    return redirect('list-tour-category')

@superuser_required(login_url='login')
def ListTourCategory(request):
    return render(request, 'tour/list-tour-category.html')

@superuser_required(login_url='login')
def AboutUsCreate(request):
    forms = AboutUsForm()
    if request.method == 'POST':
        forms = AboutUsForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard')
    context = {
        'form': forms,
    }
    return render(request, 'tour/create-about.html', context)


@superuser_required(login_url='login')
def AboutUsUpdate(request, id):
    about = AboutUs.objects.get(id=id)
    forms = AboutUsForm(instance=about)
    if request.method == 'POST':
        forms = AboutUsForm(request.POST, instance=about)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard')
    context = {
        'form': forms,
    }
    return render(request, 'tour/create-about.html', context)


@superuser_required(login_url='login')
def ContactUsTextCreate(request):
    forms = ContactUsTextForm()
    if request.method == 'POST':
        forms = ContactUsTextForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard')
    context = {
        'form': forms,
    }
    return render(request, 'tour/create-contact-us-text.html', context)


@superuser_required(login_url='login')
def ContactUsTextUpdate(request, id):
    text = ContactUsText.objects.get(id=id)
    forms = ContactUsTextForm(instance=text)
    if request.method == 'POST':
        forms = ContactUsTextForm(request.POST, instance=text)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard')
    context = {
        'form': forms,
    }
    return render(request, 'tour/create-contact-us-text.html', context)


@superuser_required(login_url='login')
def CreateSlideShow(request, id):
    slideshow = SlideShow.objects.get(id=id)
    forms = SlideshowCreateForm(instance=slideshow)
    if request.method == 'POST':
        forms = SlideshowCreateForm(request.POST, request.FILES, instance=slideshow)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard')
    context = {
        'form': forms,
        'SlideShow': slideshow
    }
    return render(request, 'tour/slideshow.html', context)


@superuser_required(login_url='login')
def ContactUsInbox(request):
    messages = ContactUs.objects.all()
    paginator = Paginator(messages, 10)
    pageNumber = request.GET.get('page')
    messages = paginator.get_page(pageNumber)
    context = {
        'Messages': messages
    }
    return render(request, 'tour/contact-list.html', context)

@superuser_required(login_url='login')
def message_delete(request, id):
    item = ContactUs.objects.get(id=id)
    item.delete()
    return redirect('messages')


@superuser_required(login_url='login')
def export_contacts_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contact.csv"'

    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['FirstName', 'LastName', 'Mobile'])

    contacts = ContactUs.objects.all().values_list('FirstName', 'LastName', 'Mobile')
    for contact in contacts:
        writer.writerow(contact)

    return response


@superuser_required(login_url='login')
def subscribeList(request):
    sublist = Subscribe.objects.all()
    paginator = Paginator(sublist, 15)
    pagenumber = request.GET.get('page')
    sublist = paginator.get_page(pagenumber)
    context = {
        'List': sublist
    }
    return render(request, 'tour/sub-list.html', context)


@superuser_required(login_url='login')
def subscribeDelete(request, id):
    subitem = Subscribe.objects.get(id=id)
    subitem.delete()
    return redirect('subscribe')


@superuser_required(login_url='login')
def export_numbers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="number.csv"'

    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['Mobile'])

    numbers = Subscribe.objects.all()
    for i in numbers:
        writer.writerow([str(i.Mobile)])
    return response


@superuser_required(login_url='login')
def FooterUpdate(request, id):
    footer = Footer.objects.get(id=id)
    forms = FooterForm(instance=footer)
    if request.method == 'POST':
        forms = FooterForm(request.POST, instance=footer)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard')
    context = {
        'Form': forms
    }
    return render(request, 'tour/footer-conf.html', context)


@superuser_required(login_url='login')
def create_home_faq(request):
    forms = create_faq__home_form()
    if request.method == "POST":
        forms = create_faq__home_form(request.POST)
        if forms.is_valid():
            new_faq = forms.save(commit=False)
            new_faq.save()
            return redirect('create_home_faq')
    all_faqs = faq_home.objects.all()
    context = {
        'forms': forms,
        'all_faqs': all_faqs
    }
    return render(request, 'tour/create_faq_home.html', context)


@superuser_required(login_url='login')
def update_home_faq(request, id):
    up_faq = faq_home.objects.get(id=id)
    forms = create_faq__home_form(instance=up_faq)
    if request.method == "POST":
        forms = create_faq__home_form(request.POST, instance=up_faq)
        if forms.is_valid():
            new_faq = forms.save(commit=False)
            new_faq.save()
            return redirect('create_home_faq')
    all_faqs = faq_home.objects.all()
    context = {
        'forms': forms,
        'all_faqs': all_faqs
    }
    return render(request, 'tour/create_faq_home.html', context)


@superuser_required(login_url='login')
def delete_home_faq(request, id):
    up_faq = faq_home.objects.get(id=id)
    up_faq.delete()
    return redirect('create_home_faq')

@superuser_required(login_url='login')
def add_trip_plan(request, id):
    tour = Tour.objects.get(id=id)
    forms = TripPlan_form()
    if request.method == 'POST':
        forms = TripPlan_form(request.POST, request.FILES)
        if forms.is_valid():
            item = forms.save(commit=False)
            item.tour = tour
            item.save()
            return redirect('add_trip_plan', tour.id)
        else:
            return redirect('add_trip_plan', tour.id)
    context = {
        'Tour': tour,
        'forms': forms
    }
    return render(request, 'tour/add-trip-plan.html', context)

@superuser_required(login_url='login')
def update_trip_plan(request, id):
    plan = TripPlan.objects.get(id=id)
    tour = Tour.objects.get(id=plan.tour.id)
    forms = TripPlan_form(instance=plan)
    if request.method == 'POST':
        forms = TripPlan_form(request.POST,request.FILES, instance=plan)
        if forms.is_valid():
            forms.save()
            return redirect('add_trip_plan', tour.id)
        else:
            return redirect('add_trip_plan', tour.id)
    context = {
        'Tour': tour,
        'forms': forms
    }
    return render(request, 'tour/add-trip-plan.html', context)

@superuser_required(login_url='login')
def delete_trip_plan(request, id):
    plan = TripPlan.objects.get(id=id)
    tour = plan.tour
    plan.delete()
    return redirect('add_trip_plan', tour.id)

@superuser_required(login_url='login')
def add_city_to_spacial(request, id):
    city = City.objects.get(id=id)
    spaial_city = spacial_destinations.objects.filter(city=city)
    if len(spaial_city):
        return redirect('update_city_to_spacial', spaial_city[0].id)
    forms = spacial_form()
    if request.method == "POST":
        forms = spacial_form(request.POST, request.FILES)
        if forms.is_valid():
            new_item = forms.save(commit=False)
            new_item.city = city
            new_item.save()
            return redirect('city_list')
    context = {
        'forms': forms,
        'city': city
    }
    return render(request, 'tour/spacial-city.html', context)

@superuser_required(login_url='login')
def update_city_to_spacial(request, id):
    item = spacial_destinations.objects.get(id=id)
    forms = spacial_form(instance=item)
    if request.method == "POST":
        forms = spacial_form(request.POST, request.FILES, instance=item)
        if forms.is_valid():
           forms.save()
           return redirect('city_list')
    context = {
        'forms': forms,
        'item': item
    }
    return render(request, 'tour/spacial-city.html', context)


@superuser_required(login_url='login')
def delete_city_to_spacial(request, id):
    item = spacial_destinations.objects.get(id=id)
    item.delete()
    return redirect('spacial_destinations_list')

@superuser_required(login_url='login')
def spacial_destinations_list(request):
    items = spacial_destinations.objects.all()
    context = {
        'items': items
    }
    return render(request, 'tour/spacial-list.html', context)

@superuser_required(login_url='login')
def add_country_to_spacial(request, id):
    country = Country.objects.get(id=id)
    spaial_country = spacial_destinations.objects.filter(country=country)
    if len(spaial_country) > 0 :
        return redirect('update_city_to_spacial', spaial_country[0].id)
    forms = spacial_form()
    if request.method == "POST":
        forms = spacial_form(request.POST, request.FILES)
        if forms.is_valid():
            new_item = forms.save(commit=False)
            new_item.country = country
            new_item.save()
            return redirect('country_list')
    context = {
        'forms': forms
    }
    return render(request, 'tour/spacial-city.html', context)
