# Generated by Django 3.2.25 on 2025-02-12 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flash',
            fields=[
                ('meeting_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('latitude', models.DecimalField(decimal_places=6, default=0.0, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=6, default=0.0, max_digits=10)),
                ('date_time', models.DateTimeField()),
                ('max_people', models.IntegerField()),
                ('explanation', models.TextField()),
                ('tags', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('now_member', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FlashParticipants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlashRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlashZzim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('flash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flash.flash')),
            ],
        ),
    ]
