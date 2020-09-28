# Generated by Django 3.0.3 on 2020-09-19 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=100)),
                ('mobileNo', models.CharField(max_length=100)),
                ('alternetMobileNo', models.CharField(blank=True, max_length=100, null=True)),
                ('PINCode', models.IntegerField()),
                ('home', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=1000)),
                ('landmark', models.CharField(blank=True, max_length=100, null=True)),
                ('town', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('action', models.CharField(max_length=100)),
                ('login_Id', models.ForeignKey(db_column='login_Id', on_delete=django.db.models.deletion.CASCADE, to='login.Loginmaster')),
            ],
        ),
    ]
