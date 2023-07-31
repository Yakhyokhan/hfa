# Generated by Django 4.2.3 on 2023-07-31 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0011_remove_page_responsible_group'),
        ('responsible_group', '0005_responsibleperson_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsiblegroup',
            name='page',
            field=models.OneToOneField(default=4, on_delete=django.db.models.deletion.PROTECT, to='page.page'),
            preserve_default=False,
        ),
    ]
