from django.contrib import admin
from .models import TranSum,CustomerMaster,MemberMaster,MOS_Sales
from django.contrib.auth.models import Group,User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
# admin.site.register(TranSum)

class UserAdmin(BaseUserAdmin):
    list_display = ('userId','username','group','firstName','lastName','emailId','contactNo','dob','active','address','companyCode','sw_CustomerId','registration_Date','valid_Date')
    list_filter =('username','group')
    fieldsets = (
        ('User Credentials', {'fields': ('username','password')}),
        (None,{'fields': ('group','firstName','lastName','emailId','contactNo','dob','address','active','companyCode','sw_CustomerId','registration_Date','valid_Date')}),
        ('Permissions', {'fields': ('is_active','is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('username','group','firstName','lastName','emailId','contactNo','dob','address','active','companyCode','sw_CustomerId','registration_Date','valid_Date','password1', 'password2')
        }),
    )
    search_fields = ('emailId',)
    ordering = ('emailId',)
    filter_horizontal = ()

admin.site.register(CustomerMaster, UserAdmin)
admin.site.unregister(Group)

# @admin.register(CustomerMaster)
# class CustomerMaster(admin.ModelAdmin):
#     list_display=['userId','userName','group','firstName','lastName','email','phoneNumber','dob','address','companyCode','swCustomerId','registrationDate','valid_date'] 

@admin.register(MemberMaster)
class MemberMasterAdmin(admin.ModelAdmin):
    list_display=['memberId','group','code','name','emailId','contactNo']



@admin.register(TranSum)
class TranSumAdmin(admin.ModelAdmin):
    list_filter = ('group', 'code','fy','againstType','part','sp')
    list_display=('trId','group','code','fy','againstType','sp','part','fmr','isinCode','trDate','qty','balQty','rate','sVal','sttCharges','otherCharges','noteAdd','marketRate','marketValue','HoldingValue','avgRate','sno','scriptSno','empCode','clDate','clRate','clQTY','clValue','clsttCharges','clOtherCharges')



@admin.register(MOS_Sales)
class MOS_SalesAdmin(admin.ModelAdmin):
    list_display=('trId','group','code','ay','againstType','scriptSno','purSno','sDate','srate','sqty','sVal','stt_Paid','stt','other','speculation','stgc','ltgc','fno','empCode')
