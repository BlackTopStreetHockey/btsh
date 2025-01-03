# Generated by Django 5.1.4 on 2024-12-20 22:17

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_teamseasonregistration_away_overtime_losses_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamseasonregistration',
            name='points',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_regulation_wins'), '+', models.F('home_overtime_wins')), '+', models.F('home_shootout_wins')), '+', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('away_regulation_wins'), '+', models.F('away_overtime_wins')), '+', models.F('away_shootout_wins'))), '*', models.Value(2)), '+', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_overtime_losses'), '+', models.F('away_overtime_losses')), '*', models.Value(1))), '+', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_shootout_losses'), '+', models.F('away_shootout_losses')), '*', models.Value(1))), '+', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_ties'), '+', models.F('away_ties')), '*', models.Value(1))), output_field=models.PositiveSmallIntegerField()),
        ),
    ]
