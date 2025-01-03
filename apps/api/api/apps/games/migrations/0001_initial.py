# Generated by Django 5.1.2 on 2024-10-25 17:04

import django.db.models.deletion
import django.db.models.expressions
import games.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seasons', '0001_initial'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('day', models.DateField(unique=True)),
                ('closing_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='closing_team_game_days', to='teams.team')),
                ('opening_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='opening_team_game_days', to='teams.team')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seasons.season')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start', models.TimeField()),
                ('duration', models.DurationField(default=games.models.default_game_duration)),
                ('end', models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(models.F('start'), '+', models.F('duration')), output_field=models.TimeField())),
                ('location', models.CharField(default='Tompkins Square Park', max_length=256)),
                ('court', models.CharField(choices=[('east', 'East'), ('west', 'West')], max_length=8)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='away_team_games', to='teams.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='home_team_games', to='teams.team')),
                ('game_day', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='games.gameday')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('game_day', 'start', 'home_team', 'away_team'), name='game_uniq')],
            },
        ),
    ]
