# Generated by Django 5.1.2 on 2024-10-19 22:43

import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared_lib', '0004_blogcategory_portfoliocategory_portfolio_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
