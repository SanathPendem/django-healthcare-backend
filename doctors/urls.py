"""
URL routing for Doctors module using DefaultRouter.
"""

from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet

app_name = 'doctors'

router = DefaultRouter()
router.register('', DoctorViewSet, basename='doctor')

urlpatterns = router.urls
