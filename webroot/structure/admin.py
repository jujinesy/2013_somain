from django.contrib import admin
from structure.models import Notice, NoticeCategory

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'created']

admin.site.register(Notice, NoticeAdmin)
admin.site.register(NoticeCategory)