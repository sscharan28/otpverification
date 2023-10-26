from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import Reg
from .form import Regmodelform,Loginform
import random
import requests
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
class Home(View):
    def get(self,request):
        return render(request,'home.html')
class RegInput(View):
    def get(self,request):
        con_dic={'regform':Regmodelform}
        return render(request,"reginput.html",context=con_dic)
class LoginInput(View):
    def get(self,request):
        con_dic={'loginform':Loginform}
        return render(request,'logininput.html',context=con_dic)
class RegView(View):
    def post(self,request):
        rf=Regmodelform(request.POST)
        if rf.is_valid():
            otp=str(random.randint(10000000,99999999))
            request.session['details']=request.POST
            request.session['otp']=otp
            resp=requests.post('http://textbelt.com/text',data={
                'phone':'+91'+str(request.POST['MobileNumber']),
                'Message':otp,
                'key':'c75b3f60f069786831f1004ebf18d6e1a854b2f9Vnz45WZIlTFwZK9MstuhIijX6',
            })
            print(resp.json())
            subject="Charan it reg otp"
            email_message=otp
            from_mail=settings.EMAIL_HOST_USER
            to_list=[request.POST['EmailId']]
            send_mail(subject,email_message,from_mail,to_list,fail_silently=False)
        return render(request,'otpinput.html')
class otpver(View):
    def post(self,request):
        Sotp=request.session['otp']
        Rotp=request.POST['t1']
        if Sotp==Rotp:
            rmf=Regmodelform(request.session['details'])
            rmf.save()
            return HttpResponse('registration success')
        else:
            return HttpResponse('registration failed')
class LoginView(View):
    def post(self,request):
        lf=Loginform(request.POST)
        if lf.is_valid():
            res=Reg.objects.filter(UserName=lf.cleaned_data['UserName'],
                                   Password=lf.cleaned_data['Password']),
        if res:
            return HttpResponse('login success')
        else:
            return HttpResponse('login failed')
