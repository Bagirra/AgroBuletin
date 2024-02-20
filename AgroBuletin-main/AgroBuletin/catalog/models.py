from datetime import date, datetime

from django.db import models
from django.urls import reverse


class Vozdeistvie(models.Model):
    name = models.CharField(max_length=200, help_text="Введите причину воздействия", verbose_name="Воздействие", default='')
    tip = models.BooleanField(help_text="Отметьте галочку, если воздействие - вредитель", verbose_name="Тип воздействия")
    describe = models.TextField(help_text="Введите описание воздействия", verbose_name="Описание воздействия",null=True, blank=True)
    describe_1 = models.TextField(help_text="Введите Стадии развития", verbose_name="Описание стадий",null=True, blank=True)
    describe2 = models.TextField(help_text="Введите повреждения от воздействия", verbose_name="Описание Повреждений",null=True, blank=True)
    describe3 = models.TextField(help_text="Введите методы борьбы", verbose_name="Описание методов",null=True, blank=True)
    fotos = models.ManyToManyField('Foto', blank=True, verbose_name="Фотографии",null=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vozdeistvie-detail', args=[str(self.id)])


class Foto(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__(self):
        return f"{self.id}"
     
    
class Culture(models.Model):
    title = models.CharField(max_length=200,
                             help_text="Введите название культуры",
                             verbose_name="Название культуры")
    vozdeistvie = models.ManyToManyField('Vozdeistvie',
                              help_text="Выберите воздействие",
                              verbose_name="Воздействие")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('culture-detail', args=[str(self.id)])

    
class City(models.Model):
    punct = models.CharField(max_length=30) 

    def __str__(self):
        return self.punct
    

class Temperature(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='temperatures')
    data = models.DateField(default=date.today) 
    max_t = models.FloatField(verbose_name="максимальная температура",null=True, blank=True) 
    min_t = models.FloatField(verbose_name="минимальная температура",null=True, blank=True) 
    avg_t = models.FloatField(verbose_name="средняя температура",null=True, blank=True)
    avg_vl = models.FloatField(verbose_name="Влажность воздуха",null=True, blank=True)
    vl_list = models.FloatField(verbose_name="Влажность листа", null=True, blank=True)
    rain = models.FloatField(verbose_name="осадки мм", null=True, blank=True)
    vl_sol = models.FloatField(verbose_name="Влажность почвы", null=True, blank=True)
    t_sol = models.FloatField(verbose_name="температура почвы", null=True, blank=True)
    soln_rad = models.FloatField(verbose_name="Солнечная радиация", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.avg_t = (self.min_t + self.max_t) / 2
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('temperature-detail', args=[str(self.city.id), str(self.id)])        