# Generated by Django 4.1.7 on 2023-05-29 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_area_ats_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='tu',
            name='Area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.area'),
        ),
    ]
