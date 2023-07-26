from xml.etree.ElementTree import ParseError

from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import render, redirect
import os
from .models import *
from .forms import *
from .utils import *
from .calc_model import Calc_model

def cp(request):
    cp = Сounterparty.objects.all()
    context = {'cp': cp}
    return render(request, 'main/cp.html', context)


def counterparty(request, counterparty_id):
    cp = Сounterparty.objects.get(pk=counterparty_id)
    context = {"cp": cp}
    return render(request, 'main/view_cp.html', context)


def index(request):
    return render(request, 'main/index.html')


def cp_create(request):
    if request.method == 'POST':
        form = addCpForm(request.POST)
        if form.is_valid():
            #  print(form.cleaned_data)
            try:
                Сounterparty.objects.create(**form.cleaned_data)
                return redirect('cp')
            except:
                form.add_error(None, 'Ошибка добавления контрагента')
    else:
        form = addCpForm()

    return render(request, 'main/cp_create.html', {'form': form})


def cont(request):
    cont = Contract.objects.all()
    context = {'cont': cont}
    return render(request, 'main/cont.html', context)


def cont_create(request):
    if request.method == 'POST':
        form = addContForm(request.POST)
        if form.is_valid():
            #  print(form.cleaned_data)
            try:
                Contract.objects.create(**form.cleaned_data)
                return redirect('cont')
            except:
                form.add_error(None, 'Ошибка добавления контракта')
    else:
        form = addContForm()

    return render(request, 'main/cont_create.html', {'form': form})


def tu(request):
    tu = Tu.objects.all()
    context = {'tu': tu}
    return render(request, 'main/tu.html', context)


def tu_view(request, tu_pk):
    tu = Tu.objects.get(id=tu_pk)
    context = {'tu': tu}
    return render(request, 'main/tu.html', context)


def tu_create(request):
    if request.method == 'POST':
        form = addTuForm(request.POST)
        if form.is_valid():
            #  print(form.cleaned_data)
            try:
                Tu.objects.create(**form.cleaned_data)
                Tu.save()
                return redirect('tu')
            except:
                form.add_error(None, 'Ошибка добавления точки учета')
    else:
        form = addTuForm()

    return render(request, 'main/tu_create.html', {'form': form})


def rate(request):
    rate = Rate.objects.all()
    context = {'rate': rate}
    return render(request, 'main/rate.html', context)


def import1(request):
    return render(request, 'main/import_page.html')


def import80000(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main/uploaded_maket.html')
    else:
        form = DocumentForm()
    return render(request, 'main/upload_file.html', {'form': form})


def upload_success(request):
    return redirect('tu')


def uploaded_maket(request):
    maket = UploadedFile.objects.all()
    context = {'maket': maket}
    return render(request, 'main/uploaded_maket.html', context)


def import_data_80000(request, pk):
    file = UploadedFile.objects.get(id=pk).file
    # -----------обработка 80000--------------
    if file.name[21:26]=='80000':
        with open(file.path, 'r') as f:
            file_content = f.read()
            comment = ' '
            comment = comment + str(read_80000_area(file))

        file = UploadedFile.objects.get(id=pk).file
        with open(file.path, 'r') as f:
            file_content = f.read()
            comment1 = ' '
            comment1 = comment1 + str(read_80000_tu(file))
        file = UploadedFile.objects.get(id=pk).file
        with open(file.path, 'r') as f:
            file_content = f.read()
            comment2 = str(' ')
            comment2 = comment2 + str(read_80000_measuring_point(file))
        file = UploadedFile.objects.get(id=pk).file
        with open(file.path, 'r') as f:
            file_content = f.read()
            comment3 = ' '
            comment3 = comment2 + str(read_80000_link(file))
        file = UploadedFile.objects.get(id=pk).file
        with open(file.path, 'r') as f:
            file_content = f.read()
            comment4 = ' '
            comment4 = str(read_80000_channels(file))
        context = {
            'file_content': file_content,
            'comment':comment,'comment1':comment1,'comment2':comment2,'comment3':comment3,
            'comment4':comment4,
            'filename': file.path
        }
        return render(request, 'main/parsed_maket.html', context)
    #-----------обработка 80020--------------
    elif file.name[21:26]=='80020':
        file = UploadedFile.objects.get(id=pk).file
        with open(file.path, 'r') as f:
            file_content = f.read()
            comment_80020 =  str(read_80020(file))
            context={'file_content': file_content,'comment_80020':comment_80020,'filename': file.path}
        return render(request, 'main/parsed_maket_80020.html', context)
    # -----------обработка 60002--------------
    elif file.name[21:26]=='60002':
        return HttpResponse('обработка 60002')
    else:
        return HttpResponse('некорректный файл'+'но название файла'+str(file.name[21:26]))




def area(request):
    area = Area.objects.all()
    context = {'area': area}
    return render(request, 'main/area.html', context)


def measuring_point(request):
    measuring_point = Measuring_point.objects.all()
    context = {'measuring_point': measuring_point}
    return render(request, 'main/measuring_point.html', context)

def measuring_channel(request):
    measuring_channel = Measuring_channel.objects.all()
    context = {'measuring_channel': measuring_channel}
    return render(request, 'main/measuring_channel.html', context)

def measuring_data(request):
    measuring_data = Measuring_data.objects.all()
    context = {'measuring_data': measuring_data}
    return render(request, 'main/measuring_data.html', context)

def create_calc_model(request,area_ats_code):
    calc_model_instance = Calc_model(area_ats_code)
    context={'calc_model_instance':calc_model_instance}
    return render(request,'main/area_view.html',context)

def calculate(request):
    if request.method == 'POST':
        # Retrieve form data
        start_day = request.POST.get('start_day')
        end_day = request.POST.get('end_day')

        context = {
            'start_day': start_day,
            'end_day': end_day,
            # Add more results as needed
        }

        return render(request, 'main/calc_dump.html', context)

        # If the request method is not POST, simply render the form page
    return render(request, 'main/calculate.html')
