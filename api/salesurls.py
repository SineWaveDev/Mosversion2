from django.urls import path
from . import sales

urlpatterns = [
    path('retSaleSum/',sales.RetSaleSum.as_view()),
    path('retSalesList/',sales.RetSalesList.as_view()), 
    path('retSalesDet/',sales.RetSalesDet.as_view()) 
]