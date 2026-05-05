from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.shortcuts import render, redirect
from tour.forms import CreateTourForm, tour_search_form
from django.contrib import messages
from tour.models import Tour, Package, TourCity, date_plan, tour_images, spacial_destinations, related_tour_city
from tour.forms import TourCityForm, tour_date_form


def superuser_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)


@superuser_required(login_url='login')
def create_tour(request):
    date = datetime.now()
    forms = CreateTourForm()
    user = request.user
    if request.method == 'POST':
        forms = CreateTourForm(request.POST, request.FILES)
        if forms.is_valid():
            tour = forms.save(commit=False)
            tour.Creator = user
            tour.updateDate = date
            tour.save()
            related_tour_city.objects.create(country=tour.Tcountry, city=tour.Tcity, tour=tour )
            files = request.FILES.getlist('files')
            for file in files:
                tour_file_instance = tour_images(tour=tour, image=file)
                tour_file_instance.save()
            return redirect('tour_date_plan', pk=tour.id)
        else:
            message = messages.error(request, 'به منظور ذخیره اطلاعات تــور لطفا تمام فیلدها را تکمیل نمایید')
            context = {
                'form': forms,
                'message': message
            }
            return render(request, 'tour/create-tour.html', context)
    context = {
        'form': forms
    }
    return render(request, 'tour/create-tour.html', context)


@superuser_required(login_url='login')
def update_tour(request, id):
    date = datetime.now()
    tour = Tour.objects.get(id=id)
    galley = tour_images.objects.filter(tour=tour)
    forms = CreateTourForm(instance=tour)
    if request.method == 'POST':
        forms = CreateTourForm(request.POST, request.FILES, instance=tour)

        if forms.is_valid():
            t = forms.save(commit=False)
            t.updateDate = date
            t.save()
            packages = Package.objects.filter(TourName=t.id)
            for i in packages:
                i.SingleBedPrice += t.add_peice_single
                i.DoubleBedPrice += t.add_peice_dubel
                i.BabyWithBedPrice += t.add_peice_with_bed
                i.BabyWithoutBedPrice += t.add_peice_without_bed
                i.InfontPrice += t.add_peice_infont
                i.save()
            tour.add_peice_dubel = 0
            tour.add_peice_single = 0
            tour.add_peice_with_bed = 0
            tour.add_peice_without_bed = 0
            tour.add_peice_infont = 0
            tour.save()
            files = request.FILES.getlist('files')
            for file in files:
                tour_file_instance = tour_images(tour=tour, image=file)
                tour_file_instance.save()
            return redirect('tour_date_plan', pk=tour.id)
    context = {
        'form': forms,
        'Data': tour,
        'galley': galley
    }
    return render(request, 'tour/create-tour.html', context)


@superuser_required(login_url='login')
def delete_tour(request, id):
    tour = Tour.objects.get(id=id)
    tour.delete()
    return redirect('tour-list')


@superuser_required(login_url='login')
def tour_list(request):
    forms = tour_search_form()
    context = {
        'forms': forms
    }
    return render(request, 'tour/list.html', context)


@superuser_required(login_url='login')
def add_city_tour(request, pk):
    tour = Tour.objects.get(id=pk)
    cities = TourCity.objects.filter(TourName_id=tour.id)
    form = TourCityForm()
    if request.method == 'POST':
        forms = TourCityForm(request.POST)
        if forms.is_valid():
            city = forms.save(commit=False)
            city.TourName = tour
            city.save()
            context = {
                'Tour': tour,
                'Cities': cities,
                'Form': form
            }
            return render(request, 'tour/tour-city-list.html', context)
    context = {
        'Tour': tour,
        'Cities': cities,
        'Form': form
    }
    return render(request, 'tour/tour-city-list.html', context)


@superuser_required(login_url='login')
def update_city_tour(request, id):
    city = TourCity.objects.get(id=id)
    tour = Tour.objects.get(id=city.TourName_id)
    nid = tour.id
    cities = TourCity.objects.filter(TourName_id=tour.id)
    form = TourCityForm(instance=city)
    if request.method == 'POST':
        forms = TourCityForm(request.POST, instance=city)
        if forms.is_valid():
            city = forms.save(commit=False)
            city.TourName = tour
            city.save()
            context = {
                'Tour': tour,
                'Cities': cities,
                'Form': form
            }
            return redirect('tour-city-list', pk=nid)
    context = {
        'Tour': tour,
        'Cities': cities,
        'Form': form
    }
    return render(request, 'tour/tour-city-list.html', context)


@superuser_required(login_url='login')
def delete_city_tour(request, id):
    city = TourCity.objects.get(id=id)
    tour = Tour.objects.get(id=city.TourName_id)
    nid = tour.id
    city.delete()
    return redirect('tour-city-list', pk=nid)


@superuser_required(login_url='login')
def tour_date_plan(request, pk):
    tour = Tour.objects.get(id=pk)
    dates = date_plan.objects.filter(tour_id=tour.id).order_by('start_date')
    form = tour_date_form()
    if request.method == 'POST':
        forms = tour_date_form(request.POST)
        if forms.is_valid():
            new_date = forms.save(commit=False)
            new_date.tour = tour
            new_date.save()
            context = {
                'Tour': tour,
                'Dates': dates,
                'Form': form
            }
            return render(request, 'tour/tour-date-list.html', context)
    context = {
        'Tour': tour,
        'Dates': dates,
        'Form': form
    }
    return render(request, 'tour/tour-date-list.html', context)


@superuser_required(login_url='login')
def tour_date_plan_update(request, id):
    date_item = date_plan.objects.get(id=id)
    tour = Tour.objects.get(id=date_item.tour.id)
    dates = date_plan.objects.filter(tour_id=tour.id).order_by('start_date')
    form = tour_date_form(instance=date_item)
    if request.method == 'POST':
        forms = tour_date_form(request.POST, instance=date_item)
        if forms.is_valid():
            new_date = forms.save(commit=False)
            new_date.tour = tour
            new_date.save()
            return redirect('tour_date_plan', tour.id)
    context = {
        'Tour': tour,
        'Dates': dates,
        'Form': form
    }
    return render(request, 'tour/tour-date-list.html', context)


@superuser_required(login_url='login')
def tour_date_plan_delete(request, id):
    date_item = date_plan.objects.get(id=id)
    tour_id = date_item.tour.id
    date_item.delete()
    return redirect('tour_date_plan', tour_id)


@superuser_required(login_url='login')
def copy_tour_data(request, id):
    main_tour = Tour.objects.get(id=id)
    tour = Tour.objects.get(id=id)
    tour.Title = tour.Title + '(کپی)'
    tour.Slug = tour.Slug + '_copy'
    tour.PubTour = False
    tour.id = None
    tour.viewCount = 0
    tour.save()
    print(tour.id)
    cities = TourCity.objects.filter(TourName=main_tour)
    for i in cities:
        i.id = None
        i.TourName = tour
        i.save()
    pakcages = Package.objects.filter(TourName=main_tour)
    for i in pakcages:
        i.id = None
        i.TourName = tour
        i.save()
    return redirect('tour-list')

@superuser_required(login_url='login')
def remove_tour_gallery(request, id):
    item = tour_images.objects.get(id=id)
    tour = Tour.objects.get(id=item.tour.id)
    item.delete()
    return redirect('update-tour', tour.id)

@superuser_required(login_url='login')
def remove_tour_featured_image(request, id):
    tour = Tour.objects.get(id=id)
    tour.TourImage = ''
    tour.save()
    return redirect('update-tour', tour.id)

@superuser_required(login_url='login')
def remove_tour_main_image(request, id):
    tour = Tour.objects.get(id=id)
    tour.tour_main = ''
    tour.save()
    return redirect('update-tour', tour.id)

@superuser_required(login_url='login')
def remove_tour_pdf(request, id):
    tour = Tour.objects.get(id=id)
    tour.TourPdf = ''
    tour.save()
    return redirect('update-tour', tour.id)