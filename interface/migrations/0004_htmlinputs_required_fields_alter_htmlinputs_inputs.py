# Generated by Django 4.2.3 on 2023-07-30 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0003_alter_htmlinputs_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='htmlinputs',
            name='required_fields',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='htmlinputs',
            name='inputs',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
