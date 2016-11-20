#-*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from models import Korzip
import json

# /korzip/search?keyword=아남타워
def search(request):
    result = {}
    keyword = request.GET.get('keyword', '')
    if keyword == '' or Korzip.objects.count == 0:
        result["status"] = False
        return HttpResponse(json.dumps(result), mimetype="application/json")
    
    data = Korzip.objects.filter(Q(dong__contains=keyword) | Q(bldg__contains=keyword)).order_by('seq')
    result["status"] = True
    result["data"] = []
    for d in data:
        address = "%s %s %s" % (d.sido, d.gungu, d.dong)
        if d.ri:
            address += " %s" % (d.ri)
        if d.bldg:
            address += " %s" % (d.bldg)
        if d.bunji:
            address += " %s" % (d.bunji)

        item = {}
        item["zipcode"] = d.zipcode
        item["address"] = address
        result["data"].append(item)
    result["count"] = len(result["data"])

    return HttpResponse(json.dumps(result), mimetype="application/json")

def test(request):
    return render_to_response('korzip/test.html')