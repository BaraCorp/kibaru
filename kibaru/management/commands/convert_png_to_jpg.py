#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.core.management.base import BaseCommand
import os

from kibaru.models import Article
from django.conf import settings


class Command(BaseCommand):
    help = 'Closes the specified apptts for voting'

    def add_arguments(self, parser):
        # parser.add_argument('apptts_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):

        print("handle")
        for ar in Article.objects.all():
            try:
                ar.save()
                # os.remove(os.path.join(settings.MEDIA_ROOT, ar.image))
            except Exception as e:
                print(ar.slug)
                print(e)
