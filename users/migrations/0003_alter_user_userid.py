# Generated by Django 5.0.2 on 2024-07-07 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_phone_alter_user_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userId',
            field=models.CharField(default='oTOeIdp0CyJwxoMBgFOC81xywSoAIjCZ', max_length=255, unique=True),
        ),
    ]