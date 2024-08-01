from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import AirlineViewSet, AircraftViewSet

router = DefaultRouter()
router.register(r'airline', AirlineViewSet)
router.register(r'aircraft', AircraftViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^airline/(?P<pk>[^/.]+)$', AirlineViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy', 'post': 'custom_post'}), name='airline-detail-no-slash'),
    re_path(r'^aircraft/(?P<pk>[^/.]+)$', AircraftViewSet.as_view({'patch': 'partial_update', 'get': 'retrieve', 'delete': 'destroy'}), name='aircraft-detail-no-slash'),
]
