"""
URL routing for Mappings module using DefaultRouter.
"""

from rest_framework.routers import DefaultRouter
from .views import MappingViewSet

app_name = 'mappings'

router = DefaultRouter()
router.register('', MappingViewSet, basename='mapping')

urlpatterns = router.urls
