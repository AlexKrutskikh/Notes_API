# Generated by Django 5.1.1 on 2024-12-06 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freevet_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('sent_time', models.DateTimeField()),
                ('phone', models.CharField(max_length=50)),
                ('ip', models.GenericIPAddressField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
