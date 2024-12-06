# Generated by Django 5.1 on 2024-12-05 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='error_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('error', 'Error')], default='completed', max_length=10),
        ),
        migrations.AlterField(
            model_name='chatsession',
            name='model_name',
            field=models.CharField(default='phi3', max_length=50),
        ),
    ]
