from django.shortcuts import render, get_object_or_404, get_list_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from prediction.models import TbInfo, TbDistrict
from .serializers import InfoSerializer, DistrictSerializer, PredictSerializer

from django.http import JsonResponse

# Create your views here.
@api_view(['GET'])
def main(requests):
    districts = get_list_or_404(TbDistrict)
    serializer = DistrictSerializer(districts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def predict_info(requests, districtid):
    infos = get_list_or_404(TbInfo, districtid=districtid)
    serializer = PredictSerializer(infos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def ranking_option(requests, ordertype):

    result = []
    info = TbInfo.objects.all()

    for i in range(0,25,1):
        obj = info.filter(districtid=i)
        last_obj = obj.last()
        rate = round((last_obj.predictprice - last_obj.price) / last_obj.price * 100, 2)
        # 통계 신호등
        # 청색
        if rate > 0:
            light = 2
        # 황색
        elif rate == 0:
            light = 0
        # 적색
        # rate < 0
        else:
            light = 1

        result.append([i, last_obj.districtname.districtname, rate, last_obj.price, last_obj.predictprice, light])
    
    return JsonResponse({'data':sorted(result, key=lambda x : x[2] * (1 if ordertype else -1))}, safe=False, json_dumps_params={'ensure_ascii':False}) 

@api_view(['GET'])
def ranking_info(requests, districtid):
    infos = get_list_or_404(TbInfo, districtid=districtid)[108:119] # 2022-01-01 ~ 2022-11-01
    serializer = InfoSerializer(infos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


