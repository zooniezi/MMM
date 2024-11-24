# Generated by Django 3.2.13 on 2024-11-24 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0008_auto_20241121_1513'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('feed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='movies.feed')),
                ('user_receive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receive_notifications', to=settings.AUTH_USER_MODEL)),
                ('user_send', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send_notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]