from rest_framework import serializers


class MedicineInfoRequestSerializer(serializers.Serializer):
    prescription = serializers.CharField(help_text="處方內容")
