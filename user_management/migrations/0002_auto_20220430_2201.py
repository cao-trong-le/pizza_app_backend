# Generated by Django 3.2.4 on 2022-04-30 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newuser',
            old_name='user_name',
            new_name='username',
        ),
        migrations.AddField(
            model_name='newuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
