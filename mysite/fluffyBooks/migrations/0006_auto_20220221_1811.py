# Generated by Django 3.2.7 on 2022-02-21 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluffyBooks', '0005_auto_20220219_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='author_text',
            new_name='author_name',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='book_author',
            new_name='book_authors',
        ),
    ]
