from rest_framework.filters import OrderingFilter


class CustomOrderingFilter(OrderingFilter):
    ordering_description = """
    ordering 參數支援 1 ~ 多個欄位，以逗號分隔對回傳資料做排序，預設是正序(由小到大)，欄位前加負號是倒序(由大到小)。  
    範例: 
    - `ordering=fields1,-fields2,fields3,fields4,fields5`
    """
