from decimal import Decimal
from .models import TranSum,MemberMaster,CustomerMaster,MOS_Sales
from rest_framework import generics
from rest_framework import status
from django.db.models import Sum,Q,F
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework.views import APIView
from .serializers import (SavePurchSerializer,RetTransSumSerializer,
SaveMemberSerializer,RetMemberSerializer,SavecustomerSerializer,
RetChangeDefaultSerializer,CustomerLoginSerializer,TranSumRetrivesc2Serializer,SaveMasterSerializer,RetHoldingReportSerializer)
import copy
from django.contrib.auth import authenticate
from .renderers import UserRender
import pandas as pd
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.conf import settings
from django.http import HttpResponse
from datetime import  datetime
from rest_framework.pagination import PageNumberPagination
from reportlab.pdfgen import canvas


# <-------------------- SavePurch API ---------------------->
class SavePurch(APIView):
    def post(self, request, format=None):
        try:
            save=TranSum.objects.filter(Q(sp='O')|Q(sp='A'),part=request.data['part']).latest('sno')
            # print("Primry--->",save)
        except:
            save=0
        # print("Primry--->",save)
        try:
            sno1=save.sno
        except:
            sno1=0
        # print("Serial no",sno1)
        if sno1 ==0 or None:
            s=sno1+1
        else:
            s=1 if sno1 is None else sno1+1
            # s=sno1+1
        try:
            latsno=TranSum.objects.filter(sp='M').latest('sno')
            # print('Save 1--->',latsno)
        except:
            latsno=0
        try:
            sn=latsno.sno
            # print("ssss",sn)
        except:
            sn=0
        print("ssss",sn)
        update1=TranSum.objects.filter(Q(sp='O')|Q(sp='A')).update(scriptSno=sn)

        request.data['sno'] = s
        request.data['scriptSno'] = sn

        dic = copy.deepcopy(request.data)
        dic["balQty"] = request.data["qty"]
        serializer = SavePurchSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            primary=TranSum.objects.filter(group=request.data['group'],code=request.data['code'],part=request.data['part'],againstType=request.data['againstType'],fy=request.data['fy']).aggregate(total_balQty=Sum('balQty'),holding_Val=Sum(F('rate') * F('balQty')))
            print("Mastr Primary2222222222222222222--->",primary)
            bal_qty=primary['total_balQty']
            hold_val=primary['holding_Val']
            avg_rate=hold_val / bal_qty
            update_bal_qty=TranSum.objects.filter(group=request.data['group'],code=request.data['code'],part=request.data['part'],againstType=request.data['againstType'],fy=request.data['fy'],sp='M').update(balQty=bal_qty,HoldingValue=hold_val,avgRate=avg_rate)
            return Response({'status':True,'msg': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavePrimaryAPI(APIView):
    def post(self, request,format=None): 
        try:
            primary=TranSum.objects.filter(sp='M').latest('sno')
        except:
            primary=0
        try:
            sno1=primary.sno
        except:
            sno1=0
        if sno1 == 0:
            s=sno1+1
            # print('yes',s)
        else:
            s=sno1+1
            # print("no",s)
        request.data['sno']=s

        serializer = SaveMasterSerializer(data=request.data)
        if serializer.is_valid():
            primary=TranSum.objects.filter(part=request.data['part'] , sp='M')
            # print("Primaryyy--->",primary)
            if primary:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            # print("Primary Records---->",serializer.data)
            return Response({'status':True,'msg': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# <--------------------RetTransSum API --------------------->
class RetTransSum(generics.ListAPIView):
    queryset=TranSum.objects.all()
    serializer_class=RetTransSumSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group','code','againstType','part']
    # <-------------------- Overriding Queryset --------------->
    def get_queryset(self):
        option = self.request.query_params.get('option') 
        dfy = self.request.query_params.get('dfy')
        try:
            start_fy = f"{dfy[:4]}-04-01"
            end_fy = f"{dfy[5:]}-03-31"
        except:
            raise Http404

        if option == 'O':

            return self.queryset.filter(trDate__lt=start_fy)
            
        elif option=='A':
            
            return self.queryset.filter(trDate__range=(start_fy,end_fy))
             
             
# <------------------------- Update and Retrive API ------------------->
class RetTransSumUpdate(generics.RetrieveUpdateAPIView):
    queryset=TranSum.objects.all()
    serializer_class=RetTransSumSerializer
    def update(self, request, *args, **kwargs):
       oldqty = self.request.query_params.get('oldqty')
       balqty = self.request.query_params.get('balqty')

       old = 0 if oldqty is None else oldqty
       balQ = 0 if balqty is None else balqty

       dict_ls =  copy.deepcopy(request.data)
       print(dict_ls)
       dict_ls["balQty"] = int(balQ) - int(old) + int((dict_ls["qty"]))

       partial = kwargs.pop('partial', False)
       instance = self.get_object()
       serializer = self.get_serializer(instance, data=dict_ls, partial=partial)
       serializer.is_valid(raise_exception=True)
       self.perform_update(serializer)
       result = {
        "status": True,
        "msg": "Data successfully updated",
        "data":dict_ls
        
       }
       return Response(result)

 # <-------------------------- Retrive API Screen No Two ------------->
 
class RetScriptSum(APIView):
    def get(self, request, format=None):
        # ------------ fetching parameter in  Url
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        part = self.request.query_params.get('part')
        dfy = self.request.query_params.get('dfy')
        try:
            start_fy = f"{dfy[:4]}-04-01"
            end_fy = f"{dfy[5:]}-03-31"
        except:
            raise Http404
        # --------------------- Opening
        opening=TranSum.objects.values('qty','sVal','marketRate','marketValue','isinCode','fmr','avgRate').order_by().filter(trDate__lt=start_fy,group=group,code=code,againstType=againstType,part=part).aggregate(opening_sum=Sum("qty"),opening_values=Sum("sVal"))
        # print("Opening1--->",opening,type(opening))
        addition=TranSum.objects.values('qty','sVal','marketRate','marketValue','isinCode','fmr','avgRate').order_by().filter(trDate__range=(start_fy,end_fy),group=group,code=code,againstType=againstType,part=part).aggregate(addition_sum=Sum("qty"),addition_values=Sum("sVal"))
        # print("Addition1--->",addition)

        opening_su = 0 if opening['opening_sum'] is None else opening['opening_sum']
        addition_su = 0 if addition['addition_sum'] is None else addition['addition_sum']
        opening_val = 0 if opening['opening_values'] is None else opening['opening_values']
        addition_val = 0 if addition['addition_values'] is None else addition['addition_values']
        
        context={
            "opening":opening_su,
            "addition":addition_su,
            "sales":0,
            "closing":opening_su+addition_su,
            "invVal":opening_val+addition_val,
            # "avgRate":round((opening_val+addition_val)/(opening_su+addition_su),2),
        }
        open_add=TranSum.objects.filter(group=group,code=code,part=part)
        serializer=TranSumRetrivesc2Serializer(open_add)
        return Response({'status':True,'msg':'done','data1':serializer.data,'data':context})


class RetHolding(APIView):
    def get(self,request,format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        dfy = self.request.query_params.get('dfy')
        againstType = self.request.query_params.get('againstType')
        
        holding = TranSum.objects.exclude(sp='M').filter(group=group,code=code,againstType=againstType,fy=dfy).values('part').order_by().annotate(total_balQty=Sum('balQty')).annotate(invVal=Sum(F('rate')*F('balQty'))).annotate(mktVal=Sum(F('balQty')*F('marketRate')))
        ls=[]
        for data in holding:
            data_ls={'part':data['part'],'holdQty':int(data['total_balQty']),'invValue':float(data['invVal']),'mktVal':float(data['mktVal'])}
            ls.append(data_ls)
        return Response({'status':True,'msg':'done','data':ls})


# <-------------------------- SaveMember api ----------------------->
class SaveMember(APIView):
    def post(self, request, format=None):
        try:
            mem=MemberMaster.objects.filter(group=request.data['group']).latest('code')
        except Exception:
          mem ='00000'
        # print("Member-->",mem)
        if mem==None or 0:
            me=mem+1
            code=me.zfill(5)
        else:
            cp=mem
            cpp=str(cp)
            cpp=int(cpp)+1
            code=str(cpp).zfill(5)
        request.data['code'] = code

        # print("Code --->",code) 
        # print("requ code",request.data.get("code"))
        
        serializer = SaveMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'Message': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# <-------------------------- RetMember API -------------------->
class RetMember(APIView):
    def get(self, request, format=None):
        group = self.request.query_params.get('group')
        member=MemberMaster.objects.filter(group=group)
        serializer=RetMemberSerializer(member,many=True)
        return Response({'status':True,'msg':'done','data':serializer.data})

# <---------------------------- updated delete api mrmber ----------------->
class MemberUpdadeDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset=MemberMaster.objects.all()
    serializer_class=SaveMemberSerializer

# <-------------------------- SaveCutomer api ---------------------------->
class SaveCustomer(APIView):
    def post(self, request,format=None):       
        gro=CustomerMaster.objects.latest('group')
        if gro==None or 0:
            ss=gro+1
            group=ss.zfill(5)
        else:
            gp=gro
            gpp=str(gp)
            gpp=int(gpp)+1
            group=str(gpp).zfill(5)
       
        request.data['group'] = group       
        # print("requ grp",request.data.get("group"))
        serializer = SavecustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'msg': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 # <---------------- RetCustomer API -------------------->
class RetCustomer(APIView):
    def get(self, request, format=None):
        username = self.request.query_params.get('username')
        customer=CustomerMaster.objects.filter(username=username)
        serializer=SavecustomerSerializer(customer,many=True)
        return Response({'status':True,'msg':'done','data':serializer.data})

# <------------ updated delete api Customer ---------------->
class CustomerUpdadeDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset=CustomerMaster.objects.all()
    serializer_class=SavecustomerSerializer

# < --------------- Login Customer Master Api ---------------->

class CustomerLogin(APIView):
    def post(self,request,format=None):
        serializer=CustomerLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username=serializer.data.get('username')
            password=serializer.data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None: 
                return Response({'status':True,'msg':'Login Success','data':serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({'status':False,'msg':'Username or Password is not Valid','data':' '})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# <----------------- RetChangeDefault ----------------->        
class RetChangeDefault(APIView):
    def get(self, request, format=None):
        group = self.request.query_params.get('group')
        member=MemberMaster.objects.filter(group=group)
        serializer=RetChangeDefaultSerializer(member,many=True)
        return Response({'status':True,'msg':'done','data':serializer.data})


#  <---------------------- HoldingReportExport ----------------->
class HoldingReportExport(APIView):
    def get(self,request):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        dfy = self.request.query_params.get('dfy')

        today = datetime.today().strftime("%d/%m/%Y")
        report=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,sp='M').values('part','balQty','HoldingValue').order_by('part')
        # print("Report---->",report)
        Master_Report_Total=TranSum.objects.values('part','balQty','HoldingValue').filter(group=group,code=code,againstType=againstType,sp='M').aggregate(hold_val_total=Sum('HoldingValue'),bal_qty_total=Sum('balQty'))
      
        total_holdRs=Master_Report_Total['hold_val_total']
        total_holdRs=0 if total_holdRs is None else total_holdRs
        total_holdRs=round(total_holdRs,2)

        total_qty=Master_Report_Total['bal_qty_total']
        total_qty=0 if total_qty is None else total_qty
        total_qty=int(total_qty)

        for data in report:
            holding_Per=round(data['HoldingValue']/total_holdRs*100,2)
            data['balQty']=int(data['balQty'])
            data['holding_Per']=holding_Per
            data['balQty']=f"{data['balQty']:,d}"
            data['HoldingValue']=f"{data['HoldingValue']:,}"
            
        member=MemberMaster.objects.filter(group=group,code=code).values('name')
        # print(':Member-------->',member)
        template_path = 'Reports/HoldingReport.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Holding Report.pdf"'
        # reader = PdfReader("Report.pdf")
        context={
            'report': report,
            'member':member,
            'total_holdRs':total_holdRs,
            'total_qty':total_qty,
            'againstType':againstType,
            'dfy':dfy,
            'today':today,
        }
        html = render_to_string(template_path,context )
        # print(html)
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response

# <--------------------  HoldingReport_Profit_Adjuste -------------------->    
class HoldingReport_Profit_Adjusted(APIView):
    def get(self,request):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        dfy = self.request.query_params.get('dfy')

        today = datetime.today().strftime("%d/%m/%Y")
        # print("today-->",today)

        report=TranSum.objects.exclude(sp='M').filter(group=group,code=code,againstType=againstType,fy=dfy).values('part').order_by('part').annotate(total_balQty=Sum('balQty')).annotate(total_rate=Sum('rate')).annotate(Purchase_Value=Sum(F('rate')*F('balQty'))).annotate(marketRate=Sum('marketRate'))
        # print('Reports----->',report)
        
        Master_Report_Total=TranSum.objects.exclude(sp='M').filter(group=group,code=code,againstType=againstType).aggregate(bal_qty_total=Sum('balQty'),final_total_rate=Sum('rate'),total_Purchase_value=Sum(F('rate')*F('balQty')))
        # print("Master ------>",Master_Report_Total)
      
        total_qty=int(Master_Report_Total['bal_qty_total'])
        total_qty=0 if total_qty is None else total_qty
        total_qty=f"{total_qty:,}"
        final_total_rate=f"{round(Master_Report_Total['final_total_rate'],2):,}"
        total_Purchase_value=f"{round(Master_Report_Total['total_Purchase_value'],2):,}"

        for data in report:
            data['part']=data['part']
            data['total_balQty']=f"{data['total_balQty']:,}"
            data['total_rate']= f"{data['total_rate']:,}"
            data['Purchase_Value']=f"{round(data['Purchase_Value'],2):,}"
            data['marketRate']=f"{round(data['marketRate'],2):,}"
           
        member=MemberMaster.objects.filter(group=group,code=code).values('name')
        # print(':Member-------->',member)
        template_path = 'Reports/Holding Report (Profit Adjusted).html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Holding Report-Profit Adjusted.pdf"'
        context={
            'report': report,
            'member':member,
            'final_total_rate':final_total_rate,
            'total_Purchase_value':total_Purchase_value,
            'total_qty':total_qty,
            'againstType':againstType,
            'dfy':dfy,
            'today':today,
        }
        html = render_to_string(template_path,context )
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response

# <---------------> Scriptwise_Profit_Report <------------->   
class Scriptwise_Profit_Report(APIView):
    def get(self,request):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        dfy = self.request.query_params.get('dfy')

        today = datetime.today().strftime("%d/%m/%Y")
        # print("today-->",today)

        report=TranSum.objects.exclude(sp='M').filter(group=group,code=code,againstType=againstType,fy=dfy).values('part').order_by('part').annotate(total_balQty=Sum('balQty'))
        # print('Reports----->',report)
        
        Master_Report_Total=TranSum.objects.exclude(sp='M').filter(group=group,code=code,againstType=againstType).aggregate(bal_qty_total=Sum('balQty'))
        print("Master ------>",Master_Report_Total)
      
        total_qty=int(Master_Report_Total['bal_qty_total'])
        total_qty=0 if total_qty is None else total_qty
        total_qty=f"{total_qty:,}"
       
        for data in report:
            data['part']=data['part']
            data['total_balQty']= f"{data['total_balQty']:,}"

           
        member=MemberMaster.objects.filter(group=group,code=code).values('name')
        # print(':Member-------->',member)
       
        template_path = 'Reports/Profit_Report(Scriptwise).html'

        response = HttpResponse(content_type='application/pdf')
       
        response['Content-Disposition'] = 'attachment; filename="Profit_Report(Scriptwise).pdf"'
    
        context={
            'report': report,
            'total_qty':total_qty,
            'member':member,
            'againstType':againstType,
            'dfy':dfy,
            'today':today,
        }
        html = render_to_string(template_path,context )
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
       
  
class TransactionReport(APIView):
    def get(self,request):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        dfy = self.request.query_params.get('dfy')
        type = self.request.query_params.get('type')

        today = datetime.today().strftime("%d/%m/%Y")
        # print("today-->",today)
        report=TranSum.objects.exclude(sp='M').filter(group=group,code=code,againstType=againstType).values('part','trDate','qty','rate','sVal','sttCharges','otherCharges','againstType')

        mos_sales=MOS_Sales.objects.values('trId','sDate','sqty','srate','sVal','stt','other').filter(group=group,code=code,againstType=type)
        print("mos_sales-->",mos_sales)
        # print('Reports----->',report)
        Master_Report_Total=TranSum.objects.exclude(sp='M').filter(group=group,code=code,againstType=againstType).aggregate(sVal_total=Sum('sVal'))
        # print("Master ------>",Master_Report_Total)
        try:
            sVal_total=int(Master_Report_Total['sVal_total'])
            sVal_total=f"{sVal_total:,}"
        except Exception:
            raise TypeError("pass parameter group ,code type ,fy")
        
        for data in report:
            data['part']=data['part']
            Purchase_Date=data['trDate'].strftime("%d/%m/%Y")
            data['trDate']=Purchase_Date
            data['sVal']=f"{data['sVal']:,}"
            data['qty']=f"{data['qty']:,}"
            data['rate']=f"{data['rate']:,}"
           
           
        # for data in mos_sales:
        #     mos_transction={
        #     'sdate':data['sDate'].strftime("%d/%m/%Y"),
        #     'sqty':data['sqty'],
        #     'srate':data['srate'],
        #     'sVal':data['sVal'],
        #     'stt':data['stt'],
        #     'other':data['other']
            
        #     }

        #     print("SSSS",mos_transction)
           

           
        member=MemberMaster.objects.filter(group=group,code=code).values('name')
        print(':Member-------->',member)
       
        template_path = 'Reports/Transaction Report.html'

        response = HttpResponse(content_type='application/pdf')
       
        response['Content-Disposition'] = 'attachment; filename="Transaction Report.pdf"'
    
        context={
            'report': report,
            'sVal_total':sVal_total,
            'member':member,
            'againstType':againstType,
            'dfy':dfy,
            'today':today,
            'mos_sales':mos_sales
        }
        html = render_to_string(template_path,context )
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
       
  

  
