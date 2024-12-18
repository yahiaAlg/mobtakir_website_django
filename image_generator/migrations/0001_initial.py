# Generated by Django 4.2.7 on 2024-12-18 00:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.TextField()),
                ('negative_prompt', models.TextField(blank=True)),
                ('guidance_scale', models.FloatField(default=7.5)),
                ('num_inference_steps', models.IntegerField(default=30)),
                ('image', models.ImageField(upload_to='generated_images/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
