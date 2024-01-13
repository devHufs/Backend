# Generated by Django 4.2.7 on 2024-01-13 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField(default='')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('attached', models.FileField(null=True, upload_to='uploads/')),
                ('link', models.URLField(null=True)),
                ('job', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('like_cnt', models.IntegerField(default=0)),
                ('comment_cnt', models.IntegerField(default=0)),
                ('scrap_cnt', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(default='')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.content')),
            ],
        ),
    ]
