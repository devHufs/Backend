# Generated by Django 4.2.7 on 2024-01-14 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_comment_user_content_like_users_content_scrap_users_and_more'),
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
