from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset  = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item)
    if request.method == 'POST':
        serialized_item = MenuItem(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        #serialized_item.validated_data
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
