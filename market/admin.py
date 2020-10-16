from django.contrib import admin

from market.models import Dyqan, Kategori, Product, Receipt, ReceiptProducts


@admin.register(Dyqan)
class DyqanAdmin(admin.ModelAdmin):
    list_display = ("emri", "adresa", "tel")


admin.site.register(Kategori)
admin.site.register(Product)
admin.site.register(Receipt)
admin.site.register(ReceiptProducts)
