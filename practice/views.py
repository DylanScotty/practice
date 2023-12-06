from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

# Market CRUD functions (SRP)
@api_view(['GET', 'POST'])
def market_list(request):
  if request.method == 'GET':
    return get_market_list(request)
  elif request.method == 'POST':
    return create_market(request)

def get_market_list(request):
  markets = Market.objects.all()
  serializer = MarketSerializer(markets, many=True)
  return Response(serializer.data)

def create_market(request):
  serializer = MarketSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def market_details(request, market_id):
  market = get_market_object(market_id)

  if request.method == 'GET':
    return get_market_details(market)
  elif request.method == 'PUT':
    return update_market(market, request.data)
  elif request.method == 'DELETE':
    return delete_market(market)

def get_market_object(market_id):
  try:
    return Market.objects.get(pk=market_id)
  except Market.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

def get_market_details(market):
  serializer = MarketSerializer(market)
  return Response(serializer.data)

def update_market(market, data):
  market_data = MarketSerializer(market, data=data)
  if market_data.is_valid():
    market_data.save()
    return Response(market_data.data)
  return Response(market_data.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_market(market):
  market.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)