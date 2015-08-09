# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20150728_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_author',
            field=models.CharField(default=b'Alex Hurst', max_length=200),
        ),
    ]
