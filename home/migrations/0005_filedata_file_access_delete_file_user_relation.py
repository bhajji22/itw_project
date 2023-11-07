# Generated by Django 4.2.6 on 2023-10-30 13:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_file_user_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedata',
            name='file_access',
            field=models.ManyToManyField(related_name='access', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='file_user_relation',
        ),
    ]