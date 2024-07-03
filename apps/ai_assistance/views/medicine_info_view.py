from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, inline_serializer

from ..service import AIAssistanceService
from ..serializers.medicine_info_serializer import MedicineInfoRequestSerializer


MEDICINE_INFO_RESPONSE = inline_serializer(
    name="MedicineInfoResponse",
    fields={
        "medicine_info": inline_serializer(
            name="MedicineInfo",
            fields={
                "medicine_name": serializers.CharField(help_text="藥物名稱"),
                "appearance": serializers.CharField(help_text="藥物外觀"),
                "instruction": serializers.CharField(help_text="服用方式"),
                "precaution": serializers.CharField(help_text="注意事項"),
                "side_effect": serializers.CharField(help_text="副作用"),
            },
        ),
        "take_medicine_info": inline_serializer(
            name="TakeMedicineInfo",
            fields={
                "start_date": serializers.CharField(help_text="開始服藥日期"),
                "intreval_days": serializers.IntegerField(help_text="服藥單位天數"),
                "duration": serializers.IntegerField(help_text="幾天的藥量"),
                "medicine_time": serializers.ListField(child=serializers.CharField(), help_text="服藥時間")
            },
        ),
    },

)


class MedicineInfoView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="藥品資訊",
        description="取得藥品的相關資訊",
        request=MedicineInfoRequestSerializer,
        responses={
            200: MEDICINE_INFO_RESPONSE
        },
    )
    def post(self, request):
        serializer = MedicineInfoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prescription = serializer.validated_data.get("prescription")

        ai_assistance_service = AIAssistanceService()
        try:
            success, result = ai_assistance_service.get_medicine_info(prescription)
            if not success:
                return Response({"error": result}, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
