# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=40, db_index=True)),
                ('url', models.URLField()),
                ('submitted', models.DateField(auto_now_add=True)),
                ('approved', models.NullBooleanField(default=None, db_index=True)),
                ('approved_on', models.DateField(default=None, null=True)),
                ('handled_by', models.CharField(default=None, max_length=20, null=True)),
                ('user_note', models.CharField(default='', max_length=400)),
                ('admin_note', models.CharField(default='', max_length=400)),
                ('data', models.TextField(default='{}')),
            ],
        ),
        migrations.CreateModel(
            name='Blueprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('floor', models.IntegerField(default=1)),
                ('style', models.CharField(max_length=20)),
                ('min_rooms', models.IntegerField(default=5)),
                ('max_rooms', models.IntegerField(default=5)),
                ('min_room_size', models.IntegerField(default=5)),
                ('max_room_size', models.IntegerField(default=5)),
                ('door_chance', models.IntegerField(default=75)),
                ('min_danger_level', models.IntegerField(default=1)),
                ('max_danger_level', models.IntegerField(default=1)),
                ('trap_ratio', models.DecimalField(default=0, max_digits=3, decimal_places=2)),
                ('resource_ratio', models.DecimalField(default=0, max_digits=3, decimal_places=2)),
                ('enemy_ratio', models.DecimalField(default=0, max_digits=3, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dungeon_List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=20, db_index=True)),
                ('name', models.CharField(max_length=60)),
                ('tileset', models.CharField(max_length=30)),
                ('floors', models.IntegerField(default=1)),
                ('public', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default='', max_length=10, db_index=True)),
                ('tile', models.CharField(default='', max_length=20)),
                ('image', models.CharField(default='', max_length=20)),
                ('name', models.CharField(default='', max_length=40)),
                ('danger_level', models.IntegerField(default=1, db_index=True)),
                ('desc', models.CharField(default='', max_length=250)),
                ('data', models.TextField(default='{}')),
                ('collectible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(max_length=40)),
                ('image', models.CharField(default='blank.png', max_length=10)),
                ('opens', models.DateField()),
                ('closes', models.DateField(null=True)),
                ('guilds', models.CharField(default='EHR', max_length=8)),
                ('rewards', models.TextField(default='{}')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('details', models.TextField(null=True)),
                ('approval', models.ForeignKey(default=None, to='pmdunity.Approval', null=True, on_delete=models.SET_NULL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('cost', models.IntegerField(default=0)),
                ('image', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('explanation', models.TextField()),
                ('appears', models.DateTimeField()),
                ('disappears', models.DateTimeField(null=True)),
                ('attributes', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('ip', models.GenericIPAddressField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Logbook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('custom_name', models.CharField(default='', max_length=40)),
                ('custom_icon', models.IntegerField(default=0)),
                ('approved', models.NullBooleanField(default=None)),
                ('approved_on', models.DateField(default=None, null=True)),
                ('rewarded', models.BooleanField(default=False)),
                ('rewarded_on', models.DateField(default=None, null=True)),
                ('reputation', models.IntegerField(default=0)),
                ('handled_by', models.CharField(default=None, max_length=20, null=True)),
                ('user_note', models.CharField(default='', max_length=400)),
                ('admin_note', models.CharField(default='', max_length=400)),
                ('order', models.IntegerField(default=1000)),
                ('submitted', models.DateField(auto_now_add=True)),
                ('dungeon_map', models.IntegerField(default=0)),
                ('resources', models.CharField(default='{}', max_length=100)),
                ('event', models.ForeignKey(to='pmdunity.Event', on_delete=models.SET_NULL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, db_index=True)),
                ('species', models.IntegerField(default=0, db_index=True)),
                ('shiny', models.BooleanField(default=False)),
                ('gender', models.CharField(max_length=20)),
                ('ability', models.CharField(max_length=30)),
                ('nature', models.CharField(max_length=8)),
                ('trait', models.CharField(max_length=30)),
                ('move1', models.CharField(default='-', max_length=40)),
                ('move2', models.CharField(default='-', max_length=40)),
                ('move3', models.CharField(default='-', max_length=40)),
                ('move4', models.CharField(default='-', max_length=40)),
                ('strength', models.IntegerField(default=0)),
                ('intelligence', models.IntegerField(default=0)),
                ('agility', models.IntegerField(default=0)),
                ('charisma', models.IntegerField(default=0)),
                ('bonus_strength', models.IntegerField(default=0)),
                ('bonus_intelligence', models.IntegerField(default=0)),
                ('bonus_agility', models.IntegerField(default=0)),
                ('bonus_charisma', models.IntegerField(default=0)),
                ('comments', models.CharField(max_length=500)),
                ('lock_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.IntegerField()),
                ('quantity', models.IntegerField(default=1)),
                ('logbook', models.ForeignKey(to='pmdunity.Logbook', on_delete=models.SET_NULL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spotlight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.URLField(null=True)),
                ('text', models.TextField(null=True)),
                ('summary', models.TextField()),
                ('appears', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, db_index=True)),
                ('application', models.CharField(max_length=150)),
                ('alt_app', models.URLField(default='', null=True)),
                ('guild', models.CharField(max_length=12, db_index=True)),
                ('joined', models.DateTimeField()),
                ('stars', models.IntegerField(default=0)),
                ('merits', models.IntegerField(default=0)),
                ('strikes', models.IntegerField(default=0)),
                ('lock_time', models.DateTimeField(null=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('cameos', models.CharField(default='Ask', max_length=12, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team_Dungeon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('floor', models.IntegerField(default=1)),
                ('dive', models.IntegerField(default=1)),
                ('seed', models.CharField(max_length=32)),
                ('data', models.TextField(default='')),
                ('completed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('key', models.ForeignKey(to='pmdunity.Dungeon_List', on_delete=models.SET_NULL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('end_time', models.IntegerField(default=0)),
                ('what', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('change', models.IntegerField(default=0)),
                ('username', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20, db_index=True)),
                ('icon', models.CharField(default='', max_length=70)),
                ('default_team', models.IntegerField(default=0)),
                ('results', models.IntegerField(default=25)),
                ('ip', models.GenericIPAddressField(default='')),
                ('admin', models.BooleanField(default=False)),
                ('beta', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamOOC',
            fields=[
                ('team', models.OneToOneField(primary_key=True, serialize=False, to='pmdunity.Team', on_delete=models.SET_NULL, null=True)),
                ('tumblr', models.URLField(default='')),
                ('type', models.CharField(default='Drawn', max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='team',
            field=models.ForeignKey(to='pmdunity.Team', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='team_dungeon',
            name='team',
            field=models.ForeignKey(to='pmdunity.Team', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='pkmn1',
            field=models.ForeignKey(related_name='poke1', on_delete=django.db.models.deletion.SET_NULL, to='pmdunity.Pokemon', null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='pkmn2',
            field=models.ForeignKey(related_name='poke2', on_delete=django.db.models.deletion.SET_NULL, to='pmdunity.Pokemon', null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='pkmn3',
            field=models.ForeignKey(related_name='poke3', on_delete=django.db.models.deletion.SET_NULL, to='pmdunity.Pokemon', null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='pkmn4',
            field=models.ForeignKey(related_name='poke4', on_delete=django.db.models.deletion.SET_NULL, to='pmdunity.Pokemon', null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='user',
            field=models.ForeignKey(to='pmdunity.User', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='spotlight',
            name='team',
            field=models.ForeignKey(to='pmdunity.Team', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='team',
            field=models.ForeignKey(to='pmdunity.Team', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='team',
            field=models.ForeignKey(to='pmdunity.Team', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='logbook',
            name='team',
            field=models.ForeignKey(to='pmdunity.Team', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='item',
            field=models.ForeignKey(to='pmdunity.Item', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='team',
            field=models.ForeignKey(to='pmdunity.Team', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='team',
            field=models.ForeignKey(to='pmdunity.Team', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(to='pmdunity.User', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='blueprint',
            name='key',
            field=models.ForeignKey(to='pmdunity.Dungeon_List', on_delete=models.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='approval',
            name='pokemon',
            field=models.ForeignKey(to='pmdunity.Pokemon', null=True, on_delete=models.SET_NULL),
        ),
        migrations.AddField(
            model_name='approval',
            name='team',
            field=models.ForeignKey(to='pmdunity.Team', null=True, on_delete=models.SET_NULL),
        ),
        migrations.AddField(
            model_name='approval',
            name='user',
            field=models.ForeignKey(to='pmdunity.User', on_delete=models.SET_NULL, null=True),
        ),
    ]
