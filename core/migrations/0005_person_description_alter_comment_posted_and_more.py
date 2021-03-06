# Generated by Django 4.0.1 on 2022-01-27 22:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_issue_pub_date_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='description',
            field=models.CharField(default='default description', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='posted',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 27, 22, 12, 32, 202689, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='issue',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 27, 22, 12, 32, 201656, tzinfo=utc)),
        ),
    ]
