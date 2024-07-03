from django.urls import path

from .views.medical_process_summary_view import MedicalProcessSummaryView
from .views.precaution_detail_view import PrecautionDetailView
from .views.medicine_info_view import MedicineInfoView


urlpatterns = [
    path(
        "medical-process-summary/",
        MedicalProcessSummaryView.as_view(),
        name="medical_process_summary",
    ),
    path(
        "precaution-detail/",
        PrecautionDetailView.as_view(),
        name="precaution_detail",
    ),
    path(
        "medicine-info/",
        MedicineInfoView.as_view(),
        name="medicine_info",
    ),
]
