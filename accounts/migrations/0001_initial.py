# Generated by Django 3.2.1 on 2021-06-09 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='monitor',
            fields=[
                ('email', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
    ]
