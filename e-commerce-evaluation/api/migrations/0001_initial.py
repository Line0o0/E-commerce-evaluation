# Generated by Django 2.2.3 on 2019-08-08 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('create_time', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
    ]