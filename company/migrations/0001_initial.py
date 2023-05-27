# Generated by Django 4.1 on 2023-05-27 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adress', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('inn', models.IntegerField()),
                ('adress', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adress.adress')),
            ],
        ),
    ]
