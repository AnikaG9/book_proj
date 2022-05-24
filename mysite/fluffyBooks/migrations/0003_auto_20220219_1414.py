# Generated by Django 3.2.7 on 2022-02-19 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluffyBooks', '0002_book_userlikes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='books',
        ),
        migrations.AddField(
            model_name='book',
            name='book_author',
            field=models.ManyToManyField(blank=True, to='fluffyBooks.Author'),
        ),
    ]
