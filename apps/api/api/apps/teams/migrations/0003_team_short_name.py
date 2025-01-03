# Generated by Django 5.1.3 on 2024-11-14 03:21

from django.db import migrations, models


SHORT_NAMES = {
    'Butchers': 'BTCH',
    'Cobra Kai': 'CK',
    'Corlears Hookers': 'HOOK',
    'Dark Rainbows': 'DRKR',
    'Denim Demons': 'DEMS',
    'Filthier': 'FLTH',
    'Fresh Kills': 'FK',
    'Fuzz': 'FUZZ',
    'Gouging Anklebiters': 'GANK',
    'Gremlins': 'GREM',
    'Instant Karma': 'IK',
    'Lbs': 'LBS',
    'Mega Touch': 'MEGA',
    'Moby Dekes': 'MOBY',
    'Poutine Machine': 'POUT',
    'Renaissance': 'RENS',
    'Riots': 'RIOT',
    'Sky Fighters': 'SKYF',
    'Vertz': 'VERT',
    'What the Puck': 'WTP',
}


def forwards_func(apps, schema_editor):
    Team = apps.get_model('teams', 'Team')

    for t in Team.objects.all():
        t.short_name = SHORT_NAMES.get(t.name)
        t.save()


def reverse_func(apps, schema_editor):
    Team = apps.get_model('teams', 'Team')

    for t in Team.objects.all():
        t.short_name = None
        t.save()


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0002_team_created_by_team_updated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='short_name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.RunPython(forwards_func, reverse_code=reverse_func),
        migrations.AlterField(
            model_name='team',
            name='short_name',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
