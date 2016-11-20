from django.contrib import admin

from document.models import MentoringType, MentoringReport
from document.models import SpendingPlan
from document.models import Sign, Document
from document.models import DonationReceipt

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'doc_title', 'created']

class SpendingPlanAdmin(admin.ModelAdmin):
    # pass
    exclude = ['doc_title']

class MentoringReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'doc_title', 'mentor', 'project', 'title']
    # exclude = ['object_id']

#class DonationReceiptAdmin(admin.ModelAdmin):
#    #list_display = ['id', 'year', 'month', 'sign_users']
#    pass

admin.site.register(SpendingPlan, SpendingPlanAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Sign)
admin.site.register(MentoringType)
admin.site.register(MentoringReport, MentoringReportAdmin)
#admin.site.register(DonationReceipt, DonationReceiptAdmin)
admin.site.register(DonationReceipt)