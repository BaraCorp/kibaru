#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import re

from django.db.models import Q


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Divise la chaîne de requête dans les mots clés strictement lié,
        se débarrasser des espaces non nécessaires et le regroupement cité
        mots ensemble.
        Exemple:
        >>> normalize_query('  toto bleni  alou  "dolo  "')
        ['toto', 'bleni', 'alou', 'dolo']
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(
            query_string)]


def get_query(query_string, search_fields):
    ''' Retourne une requête, qui est une combinaison d'objets Q. Cette combinaison
         vise à rechercher des mots-clés dans un modèle en testant les champs
         de recherche donnés.

    '''
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
