# Generated by Django 3.2.25 on 2025-02-12 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccommodationReview',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=50)),
                ('accommodation_name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='accommodation_reviews/')),
                ('is_parent', models.BooleanField(default=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('location_view', models.ImageField(blank=True, null=True, upload_to='accommodation_views/')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewComment',
            fields=[
                ('comment_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='accommodation.accommodationreview')),
            ],
            options={
                'db_table': 'review_comment',
            },
        ),
    ]
