# Generated by Django 4.1 on 2023-05-27 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0004_alter_userwithinfo_tel_num'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponsiblePerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Works',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.user')),
                ('work', models.ManyToManyField(through='staff.ResponsiblePerson', to='staff.works')),
            ],
        ),
        migrations.AddField(
            model_name='responsibleperson',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='staff.works'),
        ),
        migrations.AddField(
            model_name='responsibleperson',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='staff.workers'),
        ),
    ]
