import os

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from ..service import AIAssistanceService, VALID_FILE_TYPES
from ..serializers.medical_process_summary_serializer import (
    MedicalProcessSummaryRequestSerializer,
    MedicalProcessSummaryResponseSerializer,
)


@extend_schema(
    summary="就醫過程摘要",
    description="取得病患就醫過程的語音檔案摘要",
    request=MedicalProcessSummaryRequestSerializer,
    responses=MedicalProcessSummaryResponseSerializer,
)
class MedicalProcessSummaryView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = MedicalProcessSummaryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        audio_file = serializer.validated_data.get("audio")

        if not audio_file.name.lower().endswith(tuple(VALID_FILE_TYPES)):
            return Response(
                {"error": f"Invalid file type. Supported file types: {', '.join(VALID_FILE_TYPES)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        temp_file_path = os.path.join(settings.TEMP_MEDIA_ROOT, audio_file.name)
        with open(temp_file_path, "wb+") as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)

        ai_assistance_service = AIAssistanceService()
        try:
            transcript_success, transcript = ai_assistance_service.transcript_audio(temp_file_path)
            if not transcript_success:
                return Response({"error": transcript}, status=status.HTTP_400_BAD_REQUEST)
            summary_success, summary = ai_assistance_service.get_audio_summary(transcript)
            if not summary_success:
                return Response({"error": summary}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {
                    "symptom": summary.get("symptom", ""),
                    "precautions": summary.get("precautions", ""),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # 確保檔案被刪除
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
