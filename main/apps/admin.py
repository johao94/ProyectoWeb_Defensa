import json
from typing import Annotated
from django.contrib import admin

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.aggregates import Sum
from django.db.models.functions import TruncDay, datetime
from django.http import JsonResponse
from django.urls import path

from .models import *

class ProductoA(admin.ModelAdmin):
    
    list_display=('nombre', 'precio','provedor', 'fecha')
    search_fields = ("nombre", )

    def changelist_view(self, request, extra_context=None):
        chart_data = self.chart_data()
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        return extra_urls + urls

    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            Producto.objects.annotate(date=TruncDay("fecha"))
            .values("date")
            .annotate(y=Sum("precio"))
            .order_by("-date")
        )
class ProvedorA(admin.ModelAdmin):
    list_display=('nombre',)
class ClienteA(admin.ModelAdmin):
    list_display=('nombre', 'apellidos')
class CompraA(admin.ModelAdmin):
    list_display=('cliente', 'producto')

    def changelist_view(self, request, extra_context=None):
        chart_data = self.chart_data()
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        return extra_urls + urls

    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            Producto.objects.annotate(date=TruncDay("fecha"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )


admin.site.register(Cliente,ClienteA)
admin.site.register(Provedor,ProvedorA)
admin.site.register(Producto,ProductoA)
admin.site.register(Compra,CompraA)

admin.site.site_header="Administracion"
