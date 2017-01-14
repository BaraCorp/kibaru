#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import facebook

from django.core.management.base import BaseCommand
from django.conf import settings

from kibaru.models import Article


class Command(BaseCommand):
    help = 'Closes the specified apptts for voting'

    def add_arguments(self, parser):
        parser.add_argument('art_id', nargs='+', type=int)

    def handle(self, *args, **options):

        for art_id in options['art_id']:
            try:
                self.art = Article.objects.get(pk=art_id)
                art_text = self.art.text
            except Article.DoesNotExist:
                raise CommandError('Article "%s" does not exist' % art_id)
        print(self.post_facebook())

    def post_facebook(self):
        attach = {
            "name": self.art.category.name,
            "link": self.art.article_url(),
            "caption": settings.APP_NAME,
            "description": self.art.legend,
            "page_token": settings.PAGE_TOKEN
        }

        if self.art.image:
            attach.update({"picture": self.art.article_image_url()})
        msg = self.art.title
        page_id = "1652451611660511"
        graph = facebook.GraphAPI(settings.PAGE_TOKEN)
        post = graph.put_wall_post(
            message=msg, attachment=attach, profile_id=page_id)
        if post:
            return 'posted'
        return "No post"
