from decimal import Decimal
from .models import TranSum,MemberMaster,CustomerMaster
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
RetChangeDefaultSerializer,CustomerLoginSerializer,TranSumRetrivesc2Serializer,SavePurchSerializer1)
import copy
from django.contrib.auth import authenticate
from .renderers import UserRender

# <-------------------- SavePurch API ---------------------->
class SavePurch(APIView):
    def get(self, request, format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        dfy = self.request.query_params.get('dfy')
        part = self.request.query_params.get('part')

    
        primary=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,part=part).aggregate(total_balQty=Sum('balQty'),holding_Val=Sum(F('rate') * F('balQty')))
        print("Mastr Primary--->",primary)
        bal_qty=primary['total_balQty']
        hold_val=primary['holding_Val']
        avg_rate=hold_val / bal_qty
        print('Avg Rate---->',avg_rate)
        print("Holding val--->",hold_val)
        print("BalQty--->",bal_qty)
        update_bal_qty=TranSum.objects.filter(sp='M').update(balQty=bal_qty,HoldingValue=hold_val,avgRate=avg_rate)
        # primary1=TranSum.objects.values('isinCode','fmr').filter(group=group,code=code,againstType=againstType,fy=dfy,part=part)
        # bal_qty=0 if primary['total_balQty'] is None else primary['total_balQty']
        # hold_val1=0 if primary['holding_Val'] is None  else primary['holding_Val'] 

        # hold_val=hold_val1
        # bal_Qt=bal_qty
        # avg_rate=round(hold_val/bal_Qt)
        # print("Hold val",hold_val)
        # print("avg_rate ",avg_rate)
        # print("bal_Qt ",bal_Qt)
        # primary2=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,part=part)
        # primary2.update(balQty=bal_Qt,HoldingValue=hold_val,avgRate=avg_rate)

        # primary_ls={
        
        #     # 'avg_rate':avg_rate,
        #     'holdVal':primary['holding_Val'],
        #     'balQty':primary['total_balQty'],
        #     # 'avgRate':round(primary['holding_Val'] / primary['total_balQty'],2)
        # }
        return Response({'status':True,'msg':'done'})




    def post(self, request, format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        dfy = self.request.query_params.get('dfy')
        part = self.request.query_params.get('part')

        try:
            save=TranSum.objects.filter(Q(sp='O')|Q(sp='A')).latest('sno')
            print("Primry--->",save)
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
            s=sno1+1
        try:
            latsno=TranSum.objects.filter(sp='M').latest('sno')
            print('Save 1--->',latsno)
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
            # print("Saving Records---->",serializer.data)
          
            return Response({'status':True,'msg': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavePrimaryAPI(APIView):
    def get(self, request, format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        dfy = self.request.query_params.get('dfy')
        part = self.request.query_params.get('part')

    
        # primary=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,part=part).aggregate(total_balQty=Sum('balQty'),holding_Val=Sum(F('rate') * F('balQty')))
        # primary1=TranSum.objects.values('isinCode','fmr').filter(group=group,code=code,againstType=againstType,fy=dfy,part=part)
        # bal_qty=0 if primary['total_balQty'] is None else primary['total_balQty']
        # hold_val1=0 if primary['holding_Val'] is None  else primary['holding_Val'] 

        # hold_val=hold_val1
        # bal_Qt=bal_qty
        # avg_rate=round(hold_val/bal_Qt)
        # print("Hold val",hold_val)
        # print("avg_rate ",avg_rate)
        # print("bal_Qt ",bal_Qt)
        # primary2=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,part=part)
        # primary2.update(balQty=bal_Qt,HoldingValue=hold_val,avgRate=avg_rate)

        # primary_ls={
        
        #     # 'avg_rate':avg_rate,
        #     'holdVal':primary['holding_Val'],
        #     'balQty':primary['total_balQty'],
        #     # 'avgRate':round(primary['holding_Val'] / primary['total_balQty'],2)
        # }
        return Response({'status':True,'msg':'done'})



    def post(self, request,format=None): 
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        dfy = self.request.query_params.get('dfy')
        part = self.request.query_params.get('part') 

        try:
            primary=TranSum.objects.filter(sp='M').latest('sno')
        except:
            primary=0
        print("Primary RR",primary)
        
        try:
            sno1=primary.sno
        except:
            sno1=0
        if sno1 == 0:
            s=sno1+1
            print('yes',s)
        else:
            s=sno1+1
            print("no",s)

        request.data['sno']=s
        # scriptno=TranSum.objects.update(scriptSno=s)
        # print("requ code",request.data.get("sno"))
        
    
        # primary=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,part=part,sp=sp).latest('sno')
        # primary1=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,part=part,sp=sp).aggregate(total_balQty=Sum('balQty'),holding_Val=Sum(F('rate') * F('balQty')))
        # primary=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,part=part,sp="M")
        # print("Primry--->",primary)
        
        # scriptno=TranSum.objects.update(scriptSno=s)
        # print("requ code",request.data.get("sno"))
        serializer = SavePurchSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print("Primary Records---->",serializer.data)
            return Response({'status':True,'msg': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetPrimaryAPI(APIView):
    def get(self, request, format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        againstType = self.request.query_params.get('againstType')
        dfy = self.request.query_params.get('dfy')
        part = self.request.query_params.get('part') 
        # sp = self.request.query_params.get('sp')
        # primary=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,part=part).annotate(total_balQty=Sum('balQty')).annotate(holding_val=Sum(F('rate') * F('balQty'))).annotate(average_rate=(F('holding_val')/F('total_balQty')))

        primary=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,part=part).aggregate(total_balQty=Sum('balQty'),holding_Val=Sum(F('rate') * F('balQty')))
        primary1=TranSum.objects.values('isinCode','fmr').filter(group=group,code=code,againstType=againstType,fy=dfy,part=part)

        bal_qty=0 if primary['total_balQty'] is None else primary['total_balQty']
        hold_val1=0 if primary['holding_Val'] is None  else primary['holding_Val'] 

        hold_val=hold_val1
        bal_Qt=bal_qty
        avg_rate=round(hold_val/bal_Qt)
        print("Hold val",hold_val)
        print("avg_rate ",avg_rate)
        print("bal_Qt ",bal_Qt)
        primary2=TranSum.objects.filter(group=group,code=code,againstType=againstType,fy=dfy,part=part)
        # primary2.patch(balQty=bal_Qt)

        primary_ls={
            'isinCode':primary1[0]['isinCode'],
            'fmr':primary1[0]['fmr'],
            
            'avg_rate':avg_rate,
            'holdVal':primary['holding_Val'],
            'balQty':primary['total_balQty'],
            # 'avgRate':round(primary['holding_Val'] / primary['total_balQty'],2)
        }
        return Response({'status':True,'msg':'done','data':primary_ls})


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
            "avgRate":round((opening_val+addition_val)/(opening_su+addition_su),2),
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
        
        holding = TranSum.objects.filter(group=group,code=code,againstType=againstType).values('part').order_by().annotate(total_balQty=Sum('balQty')).annotate(invVal=Sum(F('rate')*F('balQty'))).annotate(mktVal=Sum(F('balQty')*F('marketRate')))
        # print("Ballllllll--->",holding)
        
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
        # print("groupp",group)
           
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



    
  
