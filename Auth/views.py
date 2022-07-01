from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from Auth.models import AuthDevice
from Devices.amqp import PMI

@csrf_exempt
def auth_device(request):
    if 'username' in request.POST and 'password' in request.POST:
        token = request.POST.get('username',"")
        mac_device  = request.POST.get('password',"")
        if  str(token) == "guest" and mac_device =="guest":
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
            token = request.POST.get('username',"")
            user = Auth.objects.filter(pk=token).exists()
            tags= request.POST.get('tags',"")
            if tags == "administrator":
                return HttpResponse("allow administrator")
            return HttpResponse("allow")
        return HttpResponse("deny")
    except:
        return HttpResponse("deny")
    

@csrf_exempt
def resource(request):
    print("\n\n\n resource test  &***** ",request.post)

    pass
    # print(":) ******************************* :( ")
    # return HttpResponse("allow")

@csrf_exempt
def topic(request):
    print("\n\n\ntopic test  &***** ")
    pass
    # print(":) ******************************* :( ")
    # return HttpResponse("allow")
