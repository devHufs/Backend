# Generated by Django 4.2.7 on 2024-01-13 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='job',
            field=models.CharField(blank=True, default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='link',
            field=models.URLField(default=' ', null=True),
        ),
    ]