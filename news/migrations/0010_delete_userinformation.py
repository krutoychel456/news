# Generated by Django 3.1.5 on 2024-12-02 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_userinformation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserInformation',
        ),
    ]
