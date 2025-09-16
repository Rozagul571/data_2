from rest_framework import serializers
from .models import Language, RepositoryLanguage, Repository

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name')

class RepositoryLanguageSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = RepositoryLanguage
        fields = ('language', 'code_size')

class RepositorySerializer(serializers.ModelSerializer):
    languages = RepositoryLanguageSerializer(many=True)

    class Meta:
        model = Repository
        fields = ('id', 'name', 'createdAt', 'owner', 'languages')
