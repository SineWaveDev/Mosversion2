from django.urls import path
from . import views

urlpatterns = [
    path('purchTransDet/',views.SavePurch.as_view()),
    path('savePrimaryAPI/',views.SavePrimaryAPI.as_view()),
    path('purchTransSum/',views.RetTransSum.as_view()),
    path('retTransSumUpdate/<int:pk>',views.RetTransSumUpdate.as_view()),
    path('scriptSum/',views.RetScriptSum.as_view()),
    path('holdings/',views.RetHolding.as_view()),
    path('saveMember/',views.SaveMember.as_view()),
    path('retMember/',views.RetMember.as_view()),
    path('updatesMember/<int:pk>',views.MemberUpdadeDelete.as_view()),
    path('saveCustomer/',views.SaveCustomer.as_view()),
    path('retCustomer/',views.RetCustomer.as_view()),
    path('updateCustomer/<int:pk>',views.CustomerUpdadeDelete.as_view()),
    path('customerLogin/',views.CustomerLogin.as_view()),
    path('retChangeDefault/',views.RetChangeDefault.as_view()),  
    # <=================== Report ==============================>
    path('holdingReportExport/',views.HoldingReportExport.as_view()),
    # path('holdingReportExportAll',views.HoldingReportExportAll.as_view()),
    path('holdingReport_Profit_Adjusted/',views.HoldingReport_Profit_Adjusted.as_view()),
    path('scriptwise_Profit_Report/',views.Scriptwise_Profit_Report.as_view()),
    path('transactionReport/',views.TransactionReport.as_view()),
]