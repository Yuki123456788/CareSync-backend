from rest_framework import serializers


class PrecautionDetailRequestSerializer(serializers.Serializer):
    precaution = serializers.CharField(help_text="注意事項內容")


class PrecautionDetailResponseSerializer(serializers.Serializer):
    description = serializers.CharField(help_text="注意事項詳細說明")
    situation_judgment = serializers.CharField(help_text="注意事項情境判斷")
    steps = serializers.ListField(child=serializers.CharField(), help_text="注意事項具體實踐步驟")
