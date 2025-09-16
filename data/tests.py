from django.db import models


class Owner(models.Model):
    username = models.CharField(max_length=100, unique=True)


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        unique_together = ('name', 'github')


class Repository(models.Model):
    name = models.CharField(max_length=100)
    # date
    createdAt = models.DateTimeField()
    # relationship
    owner = models.ForeignKey("Owner", models.CASCADE, "repositories")

    class Meta:
        indexes = [
            models.Index(fields=['createdAt']),
            models.Index(fields=['name']),
        ]
        unique_together = ('owner', 'name')


class RepositoryLanguage(models.Model):
    repository = models.ForeignKey("Repository", on_delete=models.CASCADE, related_name="repository_languages")
    language = models.ForeignKey("Language", on_delete=models.CASCADE)
    code_size = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("repository", "language")
