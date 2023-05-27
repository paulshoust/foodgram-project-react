# Generated by Django 3.2 on 2023-05-14 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipes',
            name='tags',
        ),
        migrations.AddField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='recipe.Tag'),
        ),
    ]
