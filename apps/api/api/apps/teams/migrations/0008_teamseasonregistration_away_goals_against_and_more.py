# Generated by Django 5.1.4 on 2024-12-21 03:57

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_teamseasonregistration_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamseasonregistration',
            name='away_goals_against',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamseasonregistration',
            name='away_goals_for',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamseasonregistration',
            name='home_goals_against',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamseasonregistration',
            name='home_goals_for',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamseasonregistration',
            name='goals_against',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(models.F('home_goals_against'), '+', models.F('away_goals_against')), output_field=models.PositiveSmallIntegerField()),
        ),
        migrations.AddField(
            model_name='teamseasonregistration',
            name='goal_differential',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_goals_for'), '+', models.F('away_goals_for')), '-', django.db.models.expressions.CombinedExpression(models.F('home_goals_against'), '+', models.F('away_goals_against'))), output_field=models.PositiveSmallIntegerField()),
        ),
        migrations.AddField(
            model_name='teamseasonregistration',
            name='goals_for',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(models.F('home_goals_for'), '+', models.F('away_goals_for')), output_field=models.PositiveSmallIntegerField()),
        ),
    ]
