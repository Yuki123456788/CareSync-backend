from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins


AUTO_FIELD_INFO = {
    "list": {
        "viewset_class": mixins.ListModelMixin,
        "summary": "取得所有",
    },
    "create": {
        "viewset_class": mixins.CreateModelMixin,
        "summary": "新增",
    },
    "retrieve": {
        "viewset_class": mixins.RetrieveModelMixin,
        "summary": "取得單一",
    },
    "update": {
        "viewset_class": mixins.UpdateModelMixin,
        "summary": "更新",
    },
    "partial_update": {
        "viewset_class": mixins.UpdateModelMixin,
        "summary": "部份更新",
    },
    "destroy": {
        "viewset_class": mixins.DestroyModelMixin,
        "summary": "刪除",
    },
}


def swagger_model_viewset_extend_schema(name: str, desc=None, auth=None):
    def decorator(model_viewset_clz):
        for method, info in AUTO_FIELD_INFO.items():
            if issubclass(model_viewset_clz, info["viewset_class"]):
                decorator = extend_schema_view(
                    **{
                        method: extend_schema(
                            auth=[{"JWT": []}] if auth is None else auth,
                            summary=f"{name} - {info['summary']}",
                            description=desc,
                        )
                    }
                )
                model_viewset_clz = decorator(model_viewset_clz)

        return model_viewset_clz

    return decorator
