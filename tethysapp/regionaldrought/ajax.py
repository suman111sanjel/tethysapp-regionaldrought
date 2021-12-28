from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import os,hashlib
import json
import requests
import ast
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response

# HOSTADDRESS = 'http://192.168.11.242:8002/'

HOSTADDRESS = 'http://110.44.114.244:8001/'
# HOSTADDRESS = 'http://192.168.10.74:8002/'

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def get_spatialaverage(request):
    # for public tethys
    url = HOSTADDRESS+'getSpatialAverageForecast/'
    csrf = '70ea40c68fa50a3d0bde25847ade8bbe56499d0a'

    # dd=request.POST.get('params')
    dd= request.body.decode("utf-8")

    requestURL = request.build_absolute_uri()
    combineURLAndParam = dd + requestURL

    base_folder = os.path.dirname(os.path.realpath(__file__))
    reqhash = hashlib.sha224(combineURLAndParam.encode('utf-8')).hexdigest()
    cachefile = os.path.join(base_folder,'workspaces','app_workspace','Cache',reqhash+'.json')
    if (not os.path.exists(cachefile)):
        aa=json.loads(dd)
        curparams=json.dumps(aa)
        params = {"params": curparams}
        response = requests.post(url,data = params, headers = {'Authorization': 'Token '+csrf} ).json()
        if ((not 'error' in response.keys())):
            with open(cachefile, "w") as f:
                json.dump(response, f)

        return JsonResponse(response,safe=False)
    else:
        with open(cachefile) as f:
            data = json.load(f)
            return JsonResponse(data,safe=False)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def get_spatialaveragecurrent(request):

    # for public tethys
    url = HOSTADDRESS+'getspatialaveragecurrent/'
    csrf = '70ea40c68fa50a3d0bde25847ade8bbe56499d0a'

    param=request.body.decode("utf-8")
    dd= ast.literal_eval(request.body.decode("utf-8"))

    base_folder = os.path.dirname(os.path.realpath(__file__))
    requestURL = request.build_absolute_uri()
    combineURLAndParam = param + requestURL

    reqhash = hashlib.sha224(combineURLAndParam.encode('utf-8')).hexdigest()
    cachefile = os.path.join(base_folder,'workspaces','app_workspace','Cache',reqhash+'.json')
    if (not os.path.exists(cachefile)):
        responseObj=requests.post(url,data = dd, headers = {'Authorization': 'Token '+csrf} )
        response = responseObj.json()
        if ((not 'error' in response.keys())):
            with open(cachefile, "w") as f:
                json.dump(response, f)

        return Response(response)
    else:
        with open(cachefile) as f:
            data = json.load(f)
            return Response(data)