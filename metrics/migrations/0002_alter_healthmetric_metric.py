# Generated by Django 4.2.4 on 2024-04-20 15:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metrics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="healthmetric",
            name="metric",
            field=models.CharField(
                choices=[
                    ("heart_rate", "Heart Rate"),
                    ("oxygen_spo2", "Oxygen - SpO2"),
                    ("steps", "Steps"),
                    ("resting_heart_rate", "Resting Heart Rate"),
                    ("sleep", "Sleep"),
                    ("exercise", "Exercises"),
                    ("stress", "Stress"),
                ],
                max_length=100,
            ),
        ),
    ]