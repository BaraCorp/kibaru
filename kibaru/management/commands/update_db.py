#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from django.core.management.base import BaseCommand
from kibaru.models import Article, Language


class Command(BaseCommand):
    help = 'Closes the specified apptts for voting'

    def add_arguments(self, parser):
        # parser.add_argument('apptts_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        Language.objects.get_or_create(slug=Language.AR, name=u'Arabe')
        Language.objects.get_or_create(slug=Language.FR, name=u'Français')

        print("handle")
        for ar in Article.objects.filter(lang=None):
            ar.lang = Language.objects.get(slug="fr")
            try:
                ar.save()
            except:
                print(ar.title)
