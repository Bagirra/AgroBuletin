# Generated by Django 4.0.5 on 2022-07-05 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Uslovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите номер условия', max_length=1000, null=True, verbose_name='Номер условия')),
                ('niz_porog', models.FloatField(help_text='Введите нижний порог развития', verbose_name='Нижний порог развития')),
                ('verh_porog', models.FloatField(help_text='Введите верхний порог развития', verbose_name='Нижний порог развития')),
                ('set', models.BooleanField(help_text='Введите сумму эффективных температур', verbose_name='Сумма эффективных температур')),
                ('optim_tem', models.FloatField(help_text='Введите оптимальную температуру', verbose_name='Постоянная температура')),
                ('min_vlajnosti', models.FloatField(help_text='Ведите минимальную влажность', verbose_name='Минимальная влажность')),
                ('max_vlajnosti', models.FloatField(help_text='Ведите максимальную влажность', verbose_name='Максимальная влажность')),
            ],
        ),
        migrations.CreateModel(
            name='Vozdeistvie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите причину воздействия', max_length=200, null=True, verbose_name='Воздействие')),
                ('tip', models.BooleanField(help_text='Отметьте тип воздействия', verbose_name='Тип воздействия')),
                ('describe', models.CharField(help_text='Введите название воздействия', max_length=100, verbose_name='Название воздействия')),
            ],
        ),
        migrations.CreateModel(
            name='Culture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите название культуры', max_length=200, verbose_name='Название культуры')),
                ('uslovie', models.ForeignKey(help_text='Выберите нужные условия', null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.uslovie', verbose_name='Условия')),
                ('vozdeistvie', models.ForeignKey(help_text='Выберите воздействие', null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.vozdeistvie', verbose_name='Воздействие')),
            ],
        ),
    ]
