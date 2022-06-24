from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from Auth.models import AuthDevice

@csrf_exempt
def auth_device(request):
    return HttpResponse("allow administrator")
    return HttpResponse("allow")
    if 'username' in request.GET and 'password' in request.GET:
        mac_device = request.GET.get('username',"")
        token = request.GET.get('password',"")
        auth_device=AuthDevice.objects.get_or_create(token=token)
        if auth_device.mac_addres==None:
            auth_device.mac_addres=mac_device
            auth_device.save()
            return HttpResponse("allow")
        else:
            if auth_device.mac_addres==mac_device:
                return HttpResponse("allow")
            else:
                return HttpResponse("deny")
    #     if username == 'admin':
    #         return HttpResponse("allow administrator")

    #     if username == 'someuser':
    #         return HttpResponse("allow")
    #     user = authenticate(username=username, password=password)
    #     if user:
    #         if user.is_superuser:
    #             return HttpResponse("allow administrator")
    #         else:
    #             return HttpResponse("allow management")
    # return HttpResponse("deny")

@csrf_exempt
def vhost(request):
    # print(":) ******************************* :( ")
    return HttpResponse("allow")

@csrf_exempt
def resource(request):
    # print(":) ******************************* :( ")
    return HttpResponse("allow")

@csrf_exempt
def topic(request):
    # print(":) ******************************* :( ")
    return HttpResponse("allow")
