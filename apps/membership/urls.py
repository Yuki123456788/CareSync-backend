from rest_framework import routers
from .views.member_view import MemberModelViewSet
from .views.group_view import GroupModelViewSet


router = routers.DefaultRouter()
router.register(r"member", MemberModelViewSet, basename="member")
router.register(r"group", GroupModelViewSet, basename="group")

urlpatterns = []
urlpatterns += router.urls
