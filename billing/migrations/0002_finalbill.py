# Generated by Django 4.2.7 on 2024-02-02 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='finalbill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('mrp', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.product')),
            ],
        ),
    ]