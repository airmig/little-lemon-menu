from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view() ,name='api view'),
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='single item')
]