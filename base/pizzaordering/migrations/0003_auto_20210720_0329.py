# Generated by Django 3.2.4 on 2021-07-20 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaordering', '0002_alter_receipt_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='order',
            field=models.OneToOneField(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='pizza', to='pizzaordering.order'),
        ),
        migrations.AlterField(
            model_name='sauce',
            name='amount',
            field=models.CharField(choices=[('less', 'Less'), ('more', 'More'), ('regular', 'Regular')], default='regular', max_length=20),
        ),
    ]
