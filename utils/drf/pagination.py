from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class DemoPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 1000

    page_query_description = """
    page 參數代表頁碼。page 值來請求對應的數據頁。  
    範例: 
    - `page=1` 表示請求第一頁的數據
    - `page=2` 表示請求第二頁的數據，依此類推
    """
    page_size_query_description = """
    size 參數定義了每一頁顯示的數據項目數量。  
    範例: 
    - `?page=2&size=20`，這表示請求第二頁的數據，並且每頁展示 20 項數據
    """

    def paginate_queryset(self, queryset, request, view=None):
        if "page" not in request.query_params:
            return None
        return super().paginate_queryset(queryset, request, view=None)

    def get_paginated_response(self, data):
        """
        格式修正為模仿Rapid7官方分頁回應
        {"page": {
            "size": <目前所使用一頁顯示筆數>,
            "totalPages": <總頁數>,
            "totalResources": <總資料筆數>
        }}
        """
        totalResources = self.page.paginator.count
        size = self.get_page_size(self.request)

        quotient, remainder = divmod(totalResources, size)
        totalPages = quotient + 1 if remainder > 0 else quotient
        return Response(
            {
                "page": {
                    "size": size,
                    "totalPages": totalPages,
                    "totalResources": totalResources,
                },
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "page": {
                    "type": "object",
                    "properties": {
                        "size": {
                            "type": "integer",
                            "description": "目前所使用一頁顯示筆數",
                        },
                        "totalPages": {
                            "type": "integer",
                            "description": "總頁數",
                        },
                        "totalResources": {
                            "type": "integer",
                            "description": "總資料筆數",
                        },
                    },
                    "description": "分頁資訊",
                },
                "result": schema,
            },
        }
