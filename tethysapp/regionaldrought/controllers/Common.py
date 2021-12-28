import datetime
import xml.etree.ElementTree as ET
import traceback
import requests
import ast
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response


def SliceFromCatalog(url, data_ext, startDate, endDate,periodicity):

    '''
    Args:
        url: catalog url
        data_ext: file extension
        startDate: start date for slice
        endDate: end date for slice

    Returns: list of sliced
    '''

    # html = parse(url).getroot()
    # list = []
    # for count in html.cssselect('a'):
    #     l = count.text_content()
    #     list.append(l)

    tree = ET.fromstring(requests.get(url).text)
    list = []

    for c in tree.iter():
        l = c.get('name')
        list.append(l)

    new = [x for x in list if (x is None) == False]
    new_list = []
    for l in filter(lambda x: x.endswith(data_ext), new):
        new_list.append(l)

    final = []

    if(startDate[-9]=='-' and endDate[-9]=='-'):
        startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d-%H-%M')
        endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d-%H-%M')
    elif(startDate[-9]=='-'):
        startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d-%H-%M')
        endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    elif(endDate[-9]=='-'):
        startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d-%H-%M')
    else:
        startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')

    if periodicity=='dekad':
        for i in range(len(new_list)):
            fileName=new_list[i]
            x = datetime.datetime.strptime(fileName[-11:-3], '%Y%m%d')
            if (x >= startDate and x < endDate):
                final.append(fileName)
    elif (periodicity=='monthly'):
        for i in range(len(new_list)):
            fileName=new_list[i]
            x = datetime.datetime.strptime(fileName[-9:-3], '%Y%m')
            if (x >= startDate and x < endDate):
                final.append(fileName)
    elif (periodicity=='quartly'):
        for i in range(len(new_list)):
            fileName=new_list[i]
            x = datetime.datetime.strptime(fileName[-13:-7], '%Y%m')
            if (x >= startDate and x < endDate):
                final.append(fileName)
    final.sort()
    return final

def SlicedFromCatalog(request):
    print("ddd")
    url = request.GET.get('url')
    data_ext = request.GET.get('data_ext')
    endDate = request.GET.get('endDate')
    startDate = request.GET.get('startDate')
    periodicity = request.GET.get('periodicity')
    data={}
    try:
        data["data"]=SliceFromCatalog(url, data_ext, startDate, endDate,periodicity)
        data["status"]=200
    except:
        data["status"]=500
        data["error"]='internal Server error'
        traceback.print_exc()
    return JsonResponse(data)

