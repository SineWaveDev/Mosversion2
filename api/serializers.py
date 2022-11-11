from pyexpat import model
from rest_framework import serializers
from .models import TranSum,CustomerMaster,MemberMaster,MOS_Sales
from django.contrib.auth.hashers import make_password


 # <----------------Saving API --------------------->
class SavePurchSerializer(serializers.ModelSerializer):
    class Meta:
        model=TranSum
        fields=('trId','group','code','fy','againstType','sp','sno','scriptSno','part','fmr','isinCode','trDate','qty','rate','sVal','sttCharges','otherCharges','noteAdd','balQty','marketRate')

class SavePurchSerializer1(serializers.ModelSerializer):
    class Meta:
        model=TranSum
        fields=('trId','group','code','fy','againstType','sp','sno','scriptSno','part','fmr','isinCode','marketRate','HoldingValue','marketValue','avgRate','dayTrade','strategyDate','strategyTrigger')

   





# <---------------Retriveing API ------------------>
class RetTransSumSerializer(serializers.ModelSerializer):
    class Meta:
        model=TranSum
        fields=['trId','trDate','qty','balQty','rate','sVal','sttCharges','otherCharges','noteAdd']

# <----------------- Retrivng API Screen No2 (opening, addition, closing) ------------------>
class TranSumRetrivesc2Serializer(serializers.ModelSerializer):
    class Meta:
        model=TranSum
        fields=['fmr','isinCode']
    
    
# class RetInvSc1serializer(serializers.ModelSerializer):
#     class Meta:
#         model=TranSum
#         fields=['trId','part','marketValue']

# <--------------- Member saving API ------------------->
class SaveMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=MemberMaster
        fields=['group','name','code','emailId','contactNo']

# <-----------------RetMember api ------------------>
class RetMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=MemberMaster
        fields=['memberId','name','emailId','contactNo']

# <---------------- Retchange Default Api serializer -------------->

class RetChangeDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model=MemberMaster
        fields=['code','name']


class SavecustomerSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True,required=False)
    class Meta:
        model=CustomerMaster
        fields=['userId','username','group','firstName','lastName','emailId','contactNo','dob','photo','address','active','companyCode','sw_CustomerId','registration_Date','valid_Date','password','password2']
      
        # extra_kwargs = {
        #     'password': {'write_only':True}
        # }
        extra_kwargs = {
            'password': {'write_only':True},
            'password': {'required': False},
            'password2': {'required': False},
        }
  
#<------------------ Validating  Password and ConformPasswordwhie Registration -------------->

    def create(self, validated_data):
        if validated_data.get('password') != validated_data.get('password2'):
            raise serializers.ValidationError("Those password don't match") 

        elif validated_data.get('password') == validated_data.get('password2'):
            validated_data['password'] = make_password(
                    validated_data.get('password')
                )

        validated_data.pop('password2') # add this
        return super(SavecustomerSerializer, self).create(validated_data)

# <-------------------- Customer Login Serializer --------------------->

class CustomerLoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=30)
    class Meta:
        model=CustomerMaster
        fields=['username','password','firstName']

# <---------------------- Sales Api Serializer (Sales) --------------->
class RetTransSumSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model=TranSum
        fields=['trId','trDate','qty','rate','sVal','balQty']


# <--------------------- salesSave API in serializer ------------------->

class SaleSaveAPISerializer(serializers.ModelSerializer):
    class Meta:
        model=MOS_Sales
        fields=['trId','group','code','ay','againstType','sDate','sqty','srate','sVal','stt','other']


# <------------------- RetSalesDetSerializer ------------------------->
class RetSalesDetSerializer(serializers.ModelSerializer):
    class Meta:
        model=MOS_Sales
        fields=['trId','sDate','sqty','srate','sVal','stt','other']








        
    