# Generated by Django 2.0.13 on 2019-12-04 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videolist', '0003_auto_20191126_0627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryinfo',
            name='name1',
        ),
        migrations.RemoveField(
            model_name='categoryinfo',
            name='name2',
        ),
        migrations.AddField(
            model_name='categoryinfo',
            name='cname',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
