# Generated by Django 3.2.25 on 2025-02-08 13:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatroom',
            options={'ordering': ['-last_message_time', '-created_at']},
        ),
        migrations.AddField(
            model_name='chatroom',
            name='deleted_at_user1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='deleted_at_user2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='deleted_by',
            field=models.ManyToManyField(blank=True, related_name='deleted_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='chatroom',
            unique_together={('user1', 'user2')},
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='travel',
        ),
    ]
