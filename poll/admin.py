from django.contrib import admin
from poll.models import *
from django.utils.translation import gettext as _


class PollItemInline(admin.TabularInline):
    model = Item
    extra = 0
    max_num = 15


class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'vote_count', 'is_published',
                    'date_expired', 'lang')
    inlines = [PollItemInline, ]

    list_filter = ('lang', 'is_published')

admin.site.register(Poll, PollAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'ip', 'user', 'datetime')
    list_filter = ('poll', 'datetime')

    ordering = ('datetime',)
admin.site.register(Vote, VoteAdmin)
