from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
import requests
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import City, Temperature
from .forms import CityForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required # Аутентификация для работы функций

# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required
def prilojenie(request):   
    user = request.user
    
    if user.groups.filter(name='inspector').exists() or user.groups.filter(name='admin').exists():
        # Если пользователь принадлежит к группе "inspector" или "admin",
        # отображаем всю страницу
        return render(request, 'prilojenie.html', {'user': user})
    else:
        # Если пользователь не принадлежит к указанным группам,
        # отображаем только вторую часть страницы
        return render(request, 'prilojenie.html', {'user': user, 'show_full_content': False})


@login_required
def vita_de_vie(request):
    grozd_result = grozd(request) # вызываем функцию grozd
    acar_result = acar(request)
    cicada_result = cicada(request)
    bacterian_result = bacterian(request)
    mildiu_result = mildiu(request)
    oidium_result = oidium(request)
    antracnoz_result = antracnoz(request)
    context = {'grozd_result': grozd_result, 'acar_result': acar_result, 'cicada_result': cicada_result, 'bacterian_result': bacterian_result, 'mildiu_result': mildiu_result, 'oidium_result': oidium_result, 'antracnoz_result': antracnoz_result} # передаем результат в контекст шаблона
    return render(request, 'vita_de_vie.html', context=context)
  
def grozd(request):
    city = request.POST.get('city')  # Запрос населённого пункта
    temperatures = Temperature.objects.filter (avg_t__gt=10.0)
    set_dates = [[] for _ in range(6)]
    set_values = [90.0, 215.0, 570.0, 702.0, 1100.0, 1235.0]
    current_set = 0
    current_set_date = None
    result = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}

    for t in temperatures:
        sred_t = t.avg_t - 10.0
        current_set += sred_t

        if current_set >= set_values[0] and len(set_dates[0]) == 0:
            set_dates[0].append(t.data)
            current_set_date =  t.data
            result["0"] += f"{current_set_date} - Начался лет гроздевки перезимовавшего поколения. Установите феромонные ловушки из расчёта одна на 3-5 га. На участках, где за сутки прилетит более 20 самцов на 1 ловушку, потребуются наблюдения за откладкой яиц, которая начнётся спустя 7-8 дней.\n"

        elif current_set >= set_values[1] and len(set_dates[1]) == 0:
            set_dates[1].append(t.data)
            current_set_date = t.data
            result["1"] += f"{current_set_date} - Начало отрождения первого поколения гроздевой листовёртки. В течении недели проводите обследования. На виноградниках, где  обнаружена яйцекладка на более 10% соцветий, в начле отрождения 1-2% гусениц, до их внедрения в соцветия проведите обработку одним из инсектицидов ларвицидного действия\n"

        elif current_set >= set_values[2] and len(set_dates[2]) == 0:
            set_dates[2].append(t.data)
            current_set_date = t.data
            result["2"] += f"{current_set_date} - Лет первого поколения\n"

        elif current_set >= set_values[3] and len(set_dates[3]) == 0:
            set_dates[3].append(t.data)
            current_set_date = t.data
            result["3"] += f"{current_set_date} - Отрождение второго поколения\n"

        elif current_set >= set_values[4] and len(set_dates[4]) == 0:
            set_dates[4].append(t.data)
            current_set_date = t.data
            result["4"] += f"{current_set_date} - Лёт второго поколения\n"

        elif current_set >= set_values[5] and len(set_dates[5]) == 0:
            set_dates[5].append(t.data)
            current_set_date = t.data
            result["5"] += f"{current_set_date} - Отрождение третьего  поколения\n"   

    result = [result["0"], result["1"], result["2"], result["3"], result["4"], result["5"]]
     
    context = {'fileg': result} 
    return context['fileg']
   # return render(request, 'vita_de_vie.html', context=context)

def acar(request):
    result = 'Первую обработку от клещей следует провести в фазе "третий лист".'
    context = {"fileg1" : result} 
    return context["fileg1"]

# Цикадка
message_dict = {}

def cicada(request):
    current_date = datetime.datetime.now().date()
    target_date = datetime.date(current_date.year, 6, 18)

    if current_date == target_date:
        result = '2023.06.15  Установите жёлтые клеевые ловушки на винограднике.'
        message_dict["message"] = result
    else:
        result = message_dict.get("message")

    context = {"fileg1": result}
    return context["fileg1"]


def mildiu(request):
    # Получение данных температуры, влажности и осадков
    temperatures = Temperature.objects.filter(data__month__range=[5, 8])

    # Проверка условий и вывод сообщения с датой
    result = []
    for temperature in temperatures:
        avg_t = temperature.avg_t if temperature.avg_t is not None else 0
        avg_vl = temperature.avg_vl if temperature.avg_vl is not None else 0
        rain = temperature.rain if temperature.rain is not None else 0
        
        if 11 <= avg_t <= 32 and 85 <= avg_vl <= 100 and rain >= 4:
            result.append(f"Угроза заражения мильдью {temperature.data}")

    context = {"fileg": result} 
    return context['fileg']


def oidium(temperatures):
    # Получение данных температуры, влажности и осадков
    temperatures = Temperature.objects.filter(data__month__range=[6, 8])

    # Проверка условий и вывод сообщения с датой
    result = []
    for temperature in temperatures:
        #avg_t = temperature.avg_t if temperature.avg_t is not None else 0
        avg_vl = temperature.avg_vl if temperature.avg_vl is not None else 0
        min_t = temperature.min_t if temperature.min_t is not None else 0
        max_t = temperature.min_t if temperature.max_t is not None else 0

    
        if 60 <= avg_vl <= 90 and max_t <=28 and min_t >=26:
            result.append(f"Угроза заражения оидиумом {temperature.data}")

    context = {"fileg": result} 
    return context['fileg']    

def antracnoz(temperatures):
    # Получение данных температуры, влажности и осадков
    temperatures = Temperature.objects.filter(data__month__range=[6, 8])

    # Проверка условий и вывод сообщения с датой
    result = []
    for temperature in temperatures:
        vl_list = temperature.vl_list if temperature.vl_list is not None else 0
        avg_vl = temperature.avg_vl if temperature.avg_vl is not None else 0
        min_t = temperature.min_t if temperature.min_t is not None else 0
        max_t = temperature.min_t if temperature.max_t is not None else 0


        if 60 <= avg_vl <= 90 and max_t <=25 and min_t >=12 and vl_list >=200:
            result.append(f"Угроза заражения антракнозом {temperature.data}")

    context = {"fileg": result} 
    return context['fileg'] 
# Пример использования
#temperatures = Temperature.objects.filter(city__punct='Taraclia')  
#oidium (temperatures)

def bacterian(request):
    current_date = datetime.datetime.now().date()
    target_date = datetime.date(current_date.year, 9, 14)
    
    if current_date == target_date:
        result = 'проведите обследование виноградников на наличие бактериального рака'
        context = {"fileg" : result} 
        return context["fileg"]

@login_required
def prun(request):
    vierme_result = vierme(request) # вызываем функцию vierme
    context = {'vierme_result': vierme_result} # передаем результат в контекст шаблона
    return render(request, 'prun.html', context = context)

def vierme(request):
    city = request.POST.get('city')  # Запрос населённого пункта
    temperatures = Temperature.objects.filter(avg_t__gt=10.0)
    set_dates = [[] for _ in range(6)]
    set_values = [65.0, 105, 190.0, 457.8, 1130.5, 1825.0]
    current_set = 0
    current_set_date = None
    result = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}

    for t in temperatures:
        sred_t = t.avg_t - 10.0
        current_set += sred_t

        if current_set >= set_values[0] and len(set_dates[0]) == 0:
            set_dates[0].append(t.data)
            current_set_date =  t.data
            result["0"]  += f"{current_set_date} - Начался лет сливовой плодожорки перезимовавшего поколения.Лёт продлится около 40 дней. При установлении температуры более 15градусов и влажной погоды, начнётся откладка яиц.\n"

        elif current_set >= set_values[1] and len(set_dates[1]) == 0:
            set_dates[1].append(t.data)
            current_set_date = t.data
            result["1"] += f"{current_set_date} - Массовый лёт и откладка яиц бабочками сливовой пплодожорки.\n"

        elif current_set >= set_values[2] and len(set_dates[2]) == 0:
            set_dates[2].append(t.data)
            current_set_date = t.data
            result["2"] += f"{current_set_date} - Начало отрождения гусениц сливовой плодожорки. Проведите обработку препаратами ларвицидного  действия. \n"

        elif current_set >= set_values[3] and len(set_dates[3]) == 0:
            set_dates[3].append(t.data)
            current_set_date = t.data
            result["3"] += f"{current_set_date} - Начало лёта сливовой плодожорки II поколения. Смените вкладыш и феромоны.\n"

        elif current_set >= set_values[4] and len(set_dates[4]) == 0:
            set_dates[4].append(t.data)
            current_set_date = t.data
            result["4"] += f"{current_set_date} -  \n"

        elif current_set >= set_values[5] and len(set_dates[5]) == 0:
            set_dates[5].append(t.data)
            current_set_date = t.data
            result["5"] += f"{current_set_date} - Отрождение третьего поколения\n"

       # if current_set_date and t.data != current_set_date:
            #current_set_date = None

    result = [result["0"], result["1"], result["2"], result["3"], result["4"], result["5"]]
        
    context = {'fileg': result} 
    return context['fileg']

@login_required
def mar(request):
    vierme_mar_result = vierme_mar(request) 
    context = {'vierme_mar_result': vierme_mar_result} # передаем результат в контекст шаблона
    return render(request, 'mar.html', context=context)
  

def vierme_mar(request):
    city = request.POST.get('city')  # Запрос населённого пункта
    temperatures = Temperature.objects.filter (avg_t__gt=10.0)
    set_dates = [[] for _ in range(6)]
    set_values = [126.0, 170.0, 235.0, 680.0, 1130.5, 1825.0]
    current_set = 0
    current_set_date = None
    result = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}

    for t in temperatures:
        sred_t = t.avg_t - 10.0
        current_set += sred_t

        if current_set >= set_values[0] and len(set_dates[0]) == 0:
            set_dates[0].append(t.data)
            current_set_date =  t.data
            result["0"] += f"{current_set_date} - Начался лет яблонной плодожорки перезимовавшего поколения. Установите феромонные ловушки из расчёта одна на 3-5 га. На участках, где за сутки прилетит более 5 самцов на 1 ловушку, потребуются наблюдения за откладкой яиц, которая начнётся спустя 5-6 дней.\n"

        elif current_set >= set_values[1] and len(set_dates[1]) == 0:
            set_dates[1].append(t.data)
            current_set_date = t.data
            result["1"] += f"{current_set_date} - Откладка яиц яблонной плодожоркой. \n"

        elif current_set >= set_values[2] and len(set_dates[2]) == 0:
            set_dates[2].append(t.data)
            current_set_date = t.data
            result["2"] += f"{current_set_date} - Отрождение гусениц яблонноой плодожорки\n"

        elif current_set >= set_values[3] and len(set_dates[3]) == 0:
            set_dates[3].append(t.data)
            current_set_date = t.data
            result["3"] += f"{current_set_date} - Начался лёт I поколения яблонной плодожорки, Смените вкладыш и феромоны. \n"

        elif current_set >= set_values[4] and len(set_dates[4]) == 0:
            set_dates[4].append(t.data)
            current_set_date = t.data
            result["4"] += f"{current_set_date} - Лёт второго поколения\n"

        elif current_set >= set_values[4] and len(set_dates[4]) == 0:
            set_dates[4].append(t.data)
            current_set_date = t.data
            result["5"] += f"{current_set_date} - Отрождение третьего  поколения\n"   

    result = [result["0"], result["1"], result["2"], result["3"], result["4"], result["5"]]
     
    context = {'fileg': result} 
    return context['fileg']
@login_required
def piersic(request):
    #vierm_v_result = grozd(request) # вызываем функцию grozd
    #context = {'grozd_result': grozd_result} # передаем результат в контекст шаблона
    return render(request, 'piersic.html')
@login_required
def cires(request):
    #grozd_result = grozd(request) # вызываем функцию grozd
    #context = {'grozd_result': grozd_result} # передаем результат в контекст шаблона
    return render(request, 'cires.html')  
@login_required
def cereale(request):
    buha_fructificat_result = buha_fructificat(request) 
    context = {'buha_fructificat_result': buha_fructificat_result} # передаем результат в контекст шаблона
    return render(request, 'cereale.html', context=context)

def buha_fructificat(request):
    city = request.POST.get('city')  # Запрос населённого пункта
    temperatures = Temperature.objects.filter (avg_t__gt=10.0)
    set_dates = [[] for _ in range(6)]
    set_values = [230.0, 330.0, 580.0, 925.0, 1500.0, 1825.0]
    current_set = 0
    current_set_date = None
    result = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}

    for t in temperatures:
        sred_t = t.avg_t - 10.0
        current_set += sred_t

        if current_set >= set_values[0] and len(set_dates[0]) == 0:
            set_dates[0].append(t.data)
            current_set_date =  t.data
            result["0"] += f"{current_set_date} - Начался лет хлопковой совки.\n"

        elif current_set >= set_values[1] and len(set_dates[1]) == 0:
            set_dates[1].append(t.data)
            current_set_date = t.data
            result["1"] += f"{current_set_date} - Откладка яиц хлопковой совкой. Следует запустить трихограмму  или в начале отрождения провести обработку \n"

        elif current_set >= set_values[2] and len(set_dates[2]) == 0:
            set_dates[2].append(t.data)
            current_set_date = t.data
            result["2"] += f"{current_set_date} - Начался лёт первого поколения хлопковой совки, обновите феромон и вкладыши в ловушках, следите за динамикой лёта. Откладка яиц начнётся через 3-4 дня.\n"

        elif current_set >= set_values[3] and len(set_dates[3]) == 0:
            set_dates[3].append(t.data)
            current_set_date = t.data
            result["3"] += f"{current_set_date} - Отрождение второго поколения. Запустите трихограмму или проведите обработку во время массового отрождения\n"

        elif current_set >= set_values[4] and len(set_dates[4]) == 0:
            set_dates[4].append(t.data)
            current_set_date = t.data
            result["4"] += f"{current_set_date} - Начался лёт второго поколения хлопковой совки. Смените вкладыш и феромон\n"

        elif current_set >= set_values[4] and len(set_dates[4]) == 0:
            set_dates[4].append(t.data)
            current_set_date = t.data
            result["5"] += f"{current_set_date} - Отрождение третьего  поколения. Запустите трихограмму или проведите обработку одним из разрешённых на культуре препаратов\n"   

    result = [result["0"], result["1"], result["2"], result["3"], result["4"], result["5"]]
     
    context = {'fileg': result} 
    return context['fileg']
   

def weather(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            temperatures = Temperature.objects.filter(city=city)
            return render(request, 'weather.html', {'city': city, 'temperatures': temperatures})
    else:
        form = CityForm()
    return render(request, 'weather_form.html', {'form': form})

def calculator(request):
    return render(request, 'calculator.html')
    

class CultureListView(generic.ListView):
    model = Culture
    template_name = 'culture_list.html'

class CultureDetailView(generic.DetailView) :
    model = Culture
    template_name = 'culture_detail.html'

class VozdeistvieDetailView(generic.DetailView):
    model = Vozdeistvie
    template_name ='vozdeistvie_detail.html'

class CityListView(ListView):
    model = City
    context_object_name = 'cities'
    template_name = 'city_list.html'

class CityDetailView(DetailView):
    model = City
    context_object_name = 'city'
    template_name = 'city_detail.html'

def temperature_detail(request, city_id, temperature_id):
    temperature = get_object_or_404(Temperature, id=temperature_id, city_id=city_id)
    return render(request, 'temperature_detail.html', {'temperature': temperature})    

#class WeatherListView(generic.ListView):
    #model = Weather
    #template_name = 'weather.html'  



