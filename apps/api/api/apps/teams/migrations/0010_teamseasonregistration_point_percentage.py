# Generated by Django 5.1.4 on 2024-12-27 19:36

import django.db.models.expressions
import django.db.models.functions.comparison
import django.db.models.functions.math
import django.db.models.lookups
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0009_teamseasonregistration_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamseasonregistration',
            name='point_percentage',
            field=models.GeneratedField(db_persist=True, expression=models.Case(models.When(django.db.models.lookups.LessThan(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_games_played'), '+', models.F('away_games_played')), '*', models.Value(2)), 1), then=None), default=django.db.models.functions.math.Round(django.db.models.expressions.CombinedExpression(django.db.models.functions.comparison.Cast(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_regulation_wins'), '+', models.F('home_overtime_wins')), '+', models.F('home_shootout_wins')), '+', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('away_regulation_wins'), '+', models.F('away_overtime_wins')), '+', models.F('away_shootout_wins'))), '*', models.Value(2)), '+', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_overtime_losses'), '+', models.F('away_overtime_losses')), '*', models.Value(1))), '+', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_shootout_losses'), '+', models.F('away_shootout_losses')), '*', models.Value(1))), '+', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_ties'), '+', models.F('away_ties')), '*', models.Value(1))), output_field=models.FloatField()), '/', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('home_games_played'), '+', models.F('away_games_played')), '*', models.Value(2))), precision=3)), output_field=models.FloatField()),
        ),
    ]