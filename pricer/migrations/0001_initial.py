# Generated by Django 2.0.4 on 2018-04-27 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='EquityOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strike', models.IntegerField(default=0)),
                ('expiration_date', models.DateTimeField()),
                ('contract_type', models.CharField(max_length=1)),
                ('exercise_early', models.BooleanField()),
                ('underlying', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pricer.Equity')),
            ],
        ),
    ]