import os

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from ..service import AIAssistanceService
from ..serializers.precaution_detail_serializer import (
    PrecautionDetailRequestSerializer,
    PrecautionDetailResponseSerializer,
)


class PrecautionDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="注意事項詳細說明",
        description="取得注意事項的詳細說明",
        request=PrecautionDetailRequestSerializer,
        responses=PrecautionDetailResponseSerializer,
    )
    def post(self, request):
        serializer = PrecautionDetailRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        precaution = serializer.validated_data.get("precaution")

        ai_assistance_service = AIAssistanceService()
        try:
            success, result = ai_assistance_service.get_precaution_detail(precaution)
            if not success:
                return Response({"error": result}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {
                    "description": result.get("description", ""),
                    "situation_judgment": result.get("situation_judgment", ""),
                    "steps": result.get("steps", []),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
