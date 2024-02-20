from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import BuletinForm
import requests

def grozd(request):   
    f = open('catalog/grozd.txt', 'r')
    file_content = f.read()
    f.close()
    
    return render(request)      

# Форма для выбора города и культуры 
  #if request.method == 'POST':
        #city = request.POST.get('city') # получить значение поля Имя
        # = request.POST.get('cultura') 
        #meteostation = request.POST.get('meteostation') 
        #output = '<h2>Регистрация</h2><h3>Населённый пункт - {0}, Населённый пункт - {1},культура - {0}</h3>'.format(city,cultura)
        #return HttpResponse(output)
   #else:    
        #buletinform =BuletinForm()   

        #return render(request, 'prilojenie.html',{'form':buletinform})
        
        #html

#<body>
   
   #<div class="forma">
      #<form method="POST">
      #{% csrf_token %}
      #<tablе>
      #{{ form.as_table }}
      #</tаblе><br/>
      #<input type="submit" vаluе="Отправить" >
      #<select>
        # <option value="l" selected="selected">Heизвecтнo</option>
         #<option value="2">Дa</option>
         #<option value="З">Heт</option>
         #</select>
      #</form>
   #</div> 
#</body>   

def prilojenie(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
          city = form.cleaned_data['city']
            # Далее можно выполнить нужные действия с выбранным городом
            # например, сохранить его в сессии
          request.session['selected_city'] = city.pk
            
            # Сохраняем город в cookies на год
          response = redirect('prilojenie')
          response.set_cookie('city', city.pk, max_age=31536000)
          return response
    else:
        form = CityForm()
    
    # Если в cookies уже есть выбранный город, устанавливаем его в форме по умолчанию
    if 'city' in request.COOKIES:
        city_pk = request.COOKIES['city']
        try:
            default_city = City.objects.get(pk=city_pk)
            form.fields['city'].initial = default_city
        except City.DoesNotExist:
            pass
            
    return render(request, 'prilojenie_form.html', {'form': form})

def vita_de_vie(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city =form.cleaned_data['city']
            grozd_result = grozd(request, city) # вызываем функцию grozd
            acar_result = acar(request)
            context = {'grozd_result': grozd_result, 'acar_result': acar_result} # передаем результат в контекст шаблона
            return render(request, 'vita_de_vie.html', context=context)
    else:
        form = CityForm()
    return render(request, "prilojenie_form.html", {'form': form})    

def vita_de_vie(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            temperatures = Temperature.objects.filter(city=city)
            acar_result = acar(request)
            context = {'temperatures': temperatures, 'city': city, 'acar_result': acar_result} # modify context
            return render(request, 'vita_de_vie.html', context=context)
    else:
        form = CityForm()
    return render(request, "prilojenie_form.html", {'form': form})    


def vita_de_vie(request):
    if request.method == 'POST':
        city_name = request.POST.get('city')

        try:
            city = City.objects.get(name=city_name)
            temperature_data = Temperature.objects.filter(city=city)
        except City.DoesNotExist:
            return render(request, 'нет этого города', {'city': city_name})
        # Вызов функций grozd и acar и получение результатов
        grozd_result = grozd(request)
        acar_result = acar(request)
        
        # Вызов функции sat_vita_de_vie и получение результатов
        grape_phases = sat_vita_de_vie(temperature_data)
        
        # Передача результатов в контекст шаблона
        context = {
            'grape_phases': grape_phases,
            'grozd_result': grozd_result,
            'acar_result': acar_result,
            'city': city
        }
        
        return render(request, 'vita_de_vie.html', context)
    
    return render(request, 'vita_de_vie.html')


def sat_vita_de_vie(request):
    temperatures=Temperature.objects.filter (avg_t_gt=10.0, city=city)  
    city = request.POST.get('city')  # Запрос населённого пункта
    sat_dates = [[] for _ in range(15)]
    sat_values = [90.0, 215.0, 600.0, 925.0, 1500.0, 1825.0]
    current_sat = 0
    current_sat_date = None
    result = {"0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": "", "11": "", "12": "", "13": "", "14": "", "15": ""}  
    for t in temperatures:
        sred_t = t.avg_t 
        current_sat += sred_t

        if current_sat >= sat_values[0] and len(sat_dates[0]) == 0:
            sat_dates[0].append(t.data)
            current_sat_date =  t.data
            result["0"] += f"{current_set_date} - Начало сокодвижения\n"

        elif current_sat >= sat_values[1] and len(sat_dates[1]) == 0:
            sat_dates[1].append(t.data)
            current_sat_date = t.data
            result["1"] += f"{current_set_date} - Набухание почек\n"

        elif current_sat >= sat_values[2] and len(sat_dates[2]) == 0:
            sat_dates[2].append(t.data)
            current_set_date = t.data
            result["2"] += f"{current_set_date} - 3-5 лист\n"

        elif current_sat >= sat_values[3] and len(sat_dates[3]) == 0:
            sat_dates[3].append(t.data)
            current_set_date = t.data
            result["3"] += f"{current_set_date} - Побеги 20 см\n"

        elif current_sat >= sat_values[4] and len(sat_dates[4]) == 0:
            sat_dates[4].append(t.data)
            current_sat_date = t.data
            result["4"] += f"{current_set_date} - Начало разрыхления соцветий\n"

        elif current_sat >= sat_values[5] and len(sat_dates[5]) == 0:
            sat_dates[5].append(t.data)
            current_sat_date = t.data
            result["5"] += f"{current_sat_date} - Конец разрыхления соцветий\n"   
        elif current_sat >= sat_values[6] and len(sat_dates[6]) == 0:
            sat_dates[6].append(t.data)
            current_sat_date = t.data
            result["6"] += f"{current_sat_date} - Начало цветения\n"   
        elif current_sat >= sat_values[7] and len(sat_dates[7]) == 0:
            sat_dates[7].append(t.data)
            current_sat_date = t.data
            result["7"] += f"{current_sat_date} - Конец цветения\n"  
        elif current_sat >= sat_values[8] and len(sat_dates[8]) == 0:
            sat_dates[8].append(t.data)
            current_sat_date = t.data
            result["8"] += f"{current_sat_date} - Формирование ягод размером с горошину\n"  
        elif current_sat >= sat_values[9] and len(sat_dates[9]) == 0:
            sat_dates[9].append(t.data)
            current_sat_date = t.data
            result["9"] += f"{current_sat_date} - Смыкание ягод в грозди\n"  
        elif current_sat >= sat_values[10] and len(sat_dates[10]) == 0:
            sat_dates[10].append(t.data)
            current_sat_date = t.data
            result["10"] += f"{current_sat_date} - Начало созревания\n"           
        elif current_sat >= sat_values[11] and len(sat_dates[11]) == 0:
            sat_dates[11].append(t.data)
            current_sat_date = t.data
            result["11"] += f"{current_sat_date} - Размягчение ягод\n"   
        elif current_sat >= sat_values[12] and len(sat_dates[12]) == 0:
            sat_dates[12].append(t.data)
            current_sat_date = t.data
            result["12"] += f"{current_sat_date} - Подходящее время для сбора урожая\n" 
        elif current_sat >= sat_values[13] and len(sat_dates[13]) == 0:
            sat_dates[13].append(t.data)
            current_sat_date = t.data
            result["13"] += f"{current_sat_date} - Листопад\n"                   
      

    result = [result["0"], result["1"], result["2"], result["3"], result["4"], result["5"],result["6"], result["7"], result["8"], result["9"], result["10"], result["11"], result["12"], result["13"]]
     
    context = {'fileg': result} 
    return context['fileg']
   # return render(request, 'vita_de_vie.html', context=context

def mildiu(request):
    # Получение данных температуры, влажности и осадков
    temperatures = Temperature.objects.filter(data__month__range=[4, 8])
    # Проверка условий и вывод сообщения с датой
    result = []
    for temperature in temperatures:
        min_t = temperature.min_t 
        avg_vl = temperature.avg_vl if temperature.avg_vl is not None else 0
        rain = temperature.rain if temperature.rain is not None else 0

        if 13 <= min_t <= 32 and 95 <= avg_vl <= 100 and rain >= 10:
            result.append(f"Угроза заражения мильдью на дату {temperature.data}")

    if result:
        return {"fileg": result}
    else:
         return {"fileg": "Нет угрозы заражения мильдью"}