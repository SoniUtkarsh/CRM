# Generated by Django 5.0.4 on 2024-05-02 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0010_lead_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='converted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]