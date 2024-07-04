from rest_framework import serializers


class MedicalProcessSummaryRequestSerializer(serializers.Serializer):
    audio = serializers.FileField(help_text="病患就醫過程的語音檔案")


class MedicalProcessSummaryResponseSerializer(serializers.Serializer):
    symptom = serializers.CharField(help_text="病患症狀的說明")
    precautions = serializers.CharField(help_text="針對這個症狀平常需要注意的事項")
