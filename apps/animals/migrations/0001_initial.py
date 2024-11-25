# Generated by Django 5.1.1 on 2024-11-25 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art', models.CharField(max_length=100)),
                ('weight', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=50)),
                ('is_homeless', models.BooleanField()),
            ],
        ),
    ]
