from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import ExtractYear
from .models import RepositoryLanguage

class LanguageReportView(APIView):
    def get(self, request):
        stats = (
            RepositoryLanguage.objects
            .values('language__name', year=ExtractYear('repository__createdAt'))
            .annotate(repo_count=Count('repository', distinct=True))
            .order_by('year', '-repo_count')
        )

        result = {}
        for stat in stats:
            year = stat['year']
            if year not in result:
                result[year] = []
            if len(result[year]) < 5:
                result[year].append({
                    'language': stat['language__name'],
                    'repo_count': stat['repo_count']
                })

        return Response(result)