from django.urls import path
from rest_framework.routers import DefaultRouter
from tickets import api_views

router = DefaultRouter()
router.register('tickets', api_views.TicketModelViewSet, basename='ticket')
urlpatterns = router.urls
