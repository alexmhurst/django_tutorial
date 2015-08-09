# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='choice_test',
            new_name='choice_text',
        ),
    ]
