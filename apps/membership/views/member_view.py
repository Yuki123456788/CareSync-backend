from rest_framework import viewsets
from ..serializers.member_serializer import MemberSerializer
from ..models import Member
from django_filters import rest_framework as filters
from utils.drf.swagger import swagger_model_viewset_extend_schema


class MemberFilter(filters.FilterSet):
    group_id = filters.NumberFilter(field_name="groups__id")

    class Meta:
        model = Member
        fields = ["group_id"]


@swagger_model_viewset_extend_schema(
    name="成員",
    desc="成員是群組內的基本單位，一個成員可以加入一到多個群組。可以透過 group_id 參數過濾特定群組的成員。",
)
class MemberModelViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()
    filterset_class = MemberFilter
