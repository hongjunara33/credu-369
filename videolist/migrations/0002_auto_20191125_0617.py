# Generated by Django 2.0.13 on 2019-11-25 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videolist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoryinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.CharField(max_length=10)),
                ('name1', models.CharField(max_length=20)),
                ('name2', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Mylearninginfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=20)),
                ('videoid', models.CharField(max_length=20)),
                ('categoryid', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Videoinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vid', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=50)),
                ('thumbnailurl', models.CharField(max_length=50)),
                ('videourl', models.CharField(max_length=50)),
                ('duration', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]