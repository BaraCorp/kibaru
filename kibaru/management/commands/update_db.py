#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.core.management.base import BaseCommand

from kibaru.models import Article, New


class Command(BaseCommand):
    help = 'Closes the specified apptts for voting'

    def add_arguments(self, parser):
        # parser.add_argument('apptts_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):

        print("handle")
        for ar in Article.objects.filter(twitte=True):
            ar.twitte = False
            try:
                print(ar)
                ar.save()
            except:
                pass

        print("New")
        for new in New.objects.filter(twitte=True):
            new.twitte = False
            try:
                print(new)
                new.save()
            except:
                pass
