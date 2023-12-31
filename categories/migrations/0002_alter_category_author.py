# Generated by Django 4.2.6 on 2023-10-30 20:32

from django.conf import settings
from django.db import migrations, models
import pocket.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='author',
            field=models.ForeignKey(on_delete=models.SET(pocket.models.get_sentinel_user), related_name='categories', to=settings.AUTH_USER_MODEL),
        ),
    ]
