from rest_framework import viewsets
from ..serializers.group_serializer import GroupSerializer
from ..models import Group
from django_filters import rest_framework as filters
from utils.drf.swagger import swagger_model_viewset_extend_schema


class GroupFilter(filters.FilterSet):
    member_id = filters.NumberFilter(field_name="members__id")

    class Meta:
        model = Group
        fields = ["member_id"]


@swagger_model_viewset_extend_schema(
    name="群組",
    desc="群組內可以有多位成員，同個群組的成員可以看到和編輯彼此的資料。可以透過 member_id 參數取得成員所在的所有群組。",
)
class GroupModelViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    filterset_class = GroupFilter
