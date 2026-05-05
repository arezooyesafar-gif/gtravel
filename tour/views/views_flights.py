from tour.pms_manager import *
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from tour.models import AirLineData, Airport
from tour.forms import CreateAirLineForm, CreateAirPortForm
from django.contrib import messages


# Airline CRUD Functions
@superuser_required(login_url='login')
def create_airline(request):
    forms = CreateAirLineForm()
    user = request.user
    if request.method == 'POST':
        forms = CreateAirLineForm(request.POST, request.FILES)
        if forms.is_valid():
            airlineform = forms.save(commit=False)
            airlineform.Creator = user
            airlineform.save()
            return redirect('airlines-list')
        else:
            messages.error(request, 'به منظور ذخیره اطلاعات ایرلاین لطفا تمام فیلدها را تکمیل نمایید')
            return redirect('airlines-list')
    context = {
        'form': forms,
    }
    return render(request, 'airlines/create-airline.html', context)


@superuser_required(login_url='login')
def update_airline(request, id):
    airline = AirLineData.objects.get(id=id)
    if request.method == 'POST':
        forms = CreateAirLineForm(request.POST, request.FILES, instance=airline)
        if forms.is_valid():
            forms.save()
            return redirect('airlines-list')
    else:
        forms = CreateAirLineForm(instance=airline)
        context = {
            'form': forms
        }
        return render(request, 'airlines/create-airline.html', context)


@superuser_required(login_url='login')
def delete_airline(request, id):
    airline = AirLineData.objects.get(id=id)
    airline.delete()
    return redirect('airlines-list')


@superuser_required(login_url='login')
def airline_list(request):
    return render(request, 'airlines/list.html')


# Airport CURD Funtions
@superuser_required(login_url='login')
def create_airport(request):
    forms = CreateAirPortForm()
    if request.method == 'POST':
        forms = CreateAirPortForm(request.POST)
        if forms.is_valid():
            forms.save()
            airport = Airport.objects.all()
            context = {
                'form': forms,
                'Data': airport
            }
            return render(request, 'airport/create-airport.html', context)
        else:
            airport = Airport.objects.all()
            message = messages.error(request, 'به منظور ذخیره اطلاعات ایرلاین لطفا تمام فیلدها را تکمیل نمایید')
            context = {
                'form': forms,
                'message': message,
                'Data': airport
            }
            return render(request, 'airport/create-airport.html', context)
    airport = Airport.objects.all()
    paginator = Paginator(airport, 10)
    pagenumber = request.GET.get('page')
    airport = paginator.get_page(pagenumber)
    context = {
        'form': forms,
        'Data': airport
    }
    return render(request, 'airport/create-airport.html', context)


@superuser_required(login_url='login')
def update_airport(request, id):
    airport = Airport.objects.get(id=id)
    forms = CreateAirPortForm(instance=airport)
    if request.method == 'POST':
        forms = CreateAirPortForm(request.POST, instance=airport)
        if forms.is_valid():
            forms.save()
            return redirect('create-airport')
        else:
            messages.error(request, 'به منظور ذخیره اطلاعات ایرلاین لطفا تمام فیلدها را تکمیل نمایید')
            return redirect('create-airport')
    context = {
        'form': forms,
        'Data': airport
    }
    return render(request, 'airport/create-airport.html', context)


@superuser_required(login_url='login')
def delete_airport(request, id):
    airport = Airport.objects.get(id=id)
    airport.delete()
    return redirect('create-airport')
