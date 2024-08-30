from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.filters import OrderingFilter, SearchFilter

from django.core.paginator import Paginator,EmptyPage
# Create your views here.

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['price', 'title', 'category']
    search_fields=['title']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Access query parameters
        category = self.request.query_params.get('category')
        price = self.request.query_params.get('price')
        #search = self.request.query_params.get('search')
        if category:
            queryset = queryset.filter(category__title=category)
        if price:
            queryset = queryset.filter(price__lte=price)
        #if search:
        #    queryset = queryset.filter(title__icontains=search)
        return queryset

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset  = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if ordering:
            # orderlist = ordering.split(',')
            # items = items.order_by(orderlist)
            items = items.order_by(ordering)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item)
    if request.method == 'POST':
        serialized_item = MenuItem(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        #serialized_item.validated_data
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
