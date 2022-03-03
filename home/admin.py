from django.contrib import admin
from .models import Stock,Sales,Credit,Salesbill,Salesbillitems,Purchasebill,Purchasebillitems,Expenses,Saving
# Register your models here.
admin.site.register(Stock)
admin.site.register(Sales)
admin.site.register(Credit)
admin.site.register(Salesbill)
admin.site.register(Purchasebill)
admin.site.register(Salesbillitems)
admin.site.register(Purchasebillitems)
admin.site.register(Expenses)
admin.site.register(Saving)