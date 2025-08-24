from django.urls import path, include
from .views import CategoryListView, ServiceListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('services/', ServiceListView.as_view(), name='services'),
]

"""

"""