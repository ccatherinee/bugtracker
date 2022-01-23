# Generated by Django 4.0.1 on 2022-01-22 22:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.project'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 22, 22, 37, 14, 387451, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=60),
        ),
    ]