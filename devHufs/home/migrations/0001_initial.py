# Generated by Django 4.2.7 on 2024-01-16 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
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
                ('link', models.URLField(default=' ', null=True)),
                ('job', models.CharField(blank=True, default=' ', max_length=100, null=True)),
                ('like_cnt', models.IntegerField(default=0)),
                ('comment_cnt', models.IntegerField(default=0)),
                ('scrap_cnt', models.IntegerField(default=0)),
                ('like_users', models.ManyToManyField(null=True, related_name='like_contents', to='accounts.userprofile')),
                ('scrap_users', models.ManyToManyField(null=True, related_name='scrap_contents', to='accounts.userprofile')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(default='')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
                ('content_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.content')),
            ],
        ),
    ]
