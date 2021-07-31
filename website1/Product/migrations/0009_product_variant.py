# Generated by Django 3.1.5 on 2021-04-29 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0008_size_variants'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='variant',
            field=models.CharField(choices=[('None', 'None'), ('Size', 'Size'), ('Color', 'Color'), ('Size-Color', 'Size-Color')], default='None', max_length=10),
        ),
    ]
