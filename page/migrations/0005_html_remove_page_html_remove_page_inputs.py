# Generated by Django 4.2.1 on 2023-06-22 10:51

from django.db import migrations, models
import page.models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_remove_page_list_alter_page_inputs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Html',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
     
    ]
