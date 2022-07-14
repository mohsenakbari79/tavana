from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from Auth.models import AuthDevice
from Devices.amqp import PMI
# dj rest auth config email 
from allauth.account.views import ConfirmEmailView
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import redirect


@csrf_exempt
def auth_device(request):
    if 'username' in request.POST and 'password' in request.POST:
        token = request.POST.get('username',"")
        mac_device  = request.POST.get('password',"")
        if  str(token) == "shire" and mac_device =="shire":
            return HttpResponse("allow administrator")
        auth_device=AuthDevice.objects.get_or_create(token=token)[0]
        PMI.add_queue(token)
        if auth_device.mac_addres==None:
            auth_device.mac_addres=mac_device
            auth_device.save()
            return HttpResponse("allow")
        else:
            if auth_device.mac_addres==mac_device:
                return HttpResponse("allow")
            else:
                return HttpResponse("deny")

@csrf_exempt
def vhost(request):
    try:
        if 'username' in request.POST:
            tags= request.POST.get('tags',"")
            if tags == "administrator":
                return HttpResponse("allow")
            token = request.POST.get('username',"")
            user = AuthDevice.objects.filter(pk=token).exists()
            
            return HttpResponse("allow")
        return HttpResponse("deny")
    except Exception as e:
        return HttpResponse("deny")
    

@csrf_exempt
def resource(request):
    pass
    # print(":) ******************************* :( ")
    return HttpResponse("allow")

@csrf_exempt
def topic(request):
    pass
    # print(":) ******************************* :( ")
    return HttpResponse("allow")


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            self.object = None
        user = get_user_model().objects.get(email=self.object.email_address.email)
        print("***************\n***************\n***************\n***************\n***************\n")
        print(user.EMAIL_FIELD)
        print("***************\n***************\n***************\n***************\n***************\n")
        print(user.emailaddress_set)
        print("***************\n***************\n***************\n***************\n***************\n")
        print(user.get_email_field_name)
        print("***************\n***************\n***************\n***************\n***************\n")
        print(user.email_user)
        
        redirect_url = reverse('auth:rest_user_details')
        return redirect(redirect_url)