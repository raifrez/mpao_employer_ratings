# Generated by Django 4.2.4 on 2023-08-24 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_rating_star_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ratinghistory',
            old_name='point_change',
            new_name='points',
        ),
        migrations.RenameField(
            model_name='ratinghistory',
            old_name='stars_change',
            new_name='stars',
        ),
        migrations.RenameField(
            model_name='ratinghistory',
            old_name='streak_change',
            new_name='streak',
        ),
    ]