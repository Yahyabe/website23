# Generated by Django 3.1.5 on 2021-04-29 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0006_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('code', models.CharField(blank=True, max_length=60, null=True)),
            ],
        ),
    ]
