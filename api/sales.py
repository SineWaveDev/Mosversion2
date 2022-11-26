from .models import TranSum,MOS_Sales
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView
from .serializers import RetTransSumSalesSerializer,RetSalesDetSerializer,SaleSaveAPISerializer

# <---------------------- RetSalesSum API ------------------->
class RetSaleSum(APIView):
    def get(self,request,format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        part = self.request.query_params.get('part')
        againstType = self.request.query_params.get('againstType')
        dfy = self.request.query_params.get('dfy')
        sales=TranSum.objects.filter(group=group,code=code,part=part,againstType=againstType)
        serializer = RetTransSumSalesSerializer(sales, many=True)
        return Response({'status':True,'msg': 'done','data':serializer.data})

#<------------------------ SalesSaveAPI ------------------------>
class SaleSaveAPI(APIView):
    def get(self,request,format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        dfy = self.request.query_params.get('dfy')
        part = self.request.query_params.get('part')
        trId = self.request.query_params.get('trId')
        againstType = self.request.query_params.get('againstType')
        mos_transum=TranSum.objects.values('qty','rate','sVal').filter(group=group,code=code,fy=dfy,againstType=againstType,part=part,trId=trId)
    
        for data in mos_transum:
            dic={'qty':data['qty']}
            # print(dic)
            ss=dic['qty']
            # print(ss)
        
        # serializer=RetSalesDetSerializer(mos_transum,many=True)
        return Response({'status':True,'msg':'done'})

    def post(self, request, format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        dfy = self.request.query_params.get('dfy')
        part = self.request.query_params.get('part')
        ay = self.request.query_params.get('ay')
        trId = self.request.query_params.get('trId')
        againstType = self.request.query_params.get('againstType')
        mos_transum=TranSum.objects.values('qty','rate','sVal','scriptSno','sno').filter(group=group,code=code,fy=dfy,againstType=againstType,part=part,trId=trId)
        print("Data--->",mos_transum)
        for data in mos_transum:
            dic={'qty':data['qty'],'sno':data['sno']}
            Pur_qty=dic['qty']
            serial_no=data['sno']
            scriptSno1=data['scriptSno']
            print("Purchase Qty-->",Pur_qty)
            print("serial_no--->",serial_no)
        sell_sqty=request.data['sqty']
        print('Sell id--->',sell_sqty)
        # Pur_qty=0 if Pur_qty is None or 0 else Pur_qty
       
        final_qty=Pur_qty-sell_sqty
        

        print("Final Qty-->",final_qty)
        up=TranSum.objects.filter(group=group,code=code,fy=dfy,againstType=againstType,part=part,trId=trId).update(qty=final_qty,balQty=final_qty)

    
        sell_api=MOS_Sales.objects.update(purSno=serial_no,scriptSno=scriptSno1)
        # request.data['group']
        # print("Group--->",sell_api)
        serializer = SaleSaveAPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({'status':True,'msg': 'You have successfully Created','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# <---------------------- RetSalesDet API ------------------->
class RetSalesDet(APIView):
    def get(self,request,format=None):
        group = self.request.query_params.get('group')
        code = self.request.query_params.get('code')
        dfy = self.request.query_params.get('dfy')
        part = self.request.query_params.get('part')
        trId = self.request.query_params.get('trId')
        againstType = self.request.query_params.get('againstType')
        mos_transum=TranSum.objects.values('qty','rate','sVal').filter(group=group,code=code,fy=dfy,againstType=againstType,part=part,trId=trId)
    
        for data in mos_transum:
            dic={'qty':data['qty']}
            print(dic)
            ss=dic['qty']-300
            print(ss)
        
        # serializer=RetSalesDetSerializer(mos_transum,many=True)
        return Response({'status':True,'msg':'done'})
