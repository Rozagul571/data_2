from django.urls import path
from .views import LanguageReportView

urlpatterns = [
    path('language-report/', LanguageReportView.as_view(), name='language-report'),
]