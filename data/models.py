from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Repository(models.Model):
    name = models.CharField(max_length=100)
    # date
    createdAt = models.DateTimeField(null=True, blank=True)
    # relationship
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="repositories")
    languages = models.ManyToManyField(Language, through='RepositoryLanguage')

    class Meta:
        unique_together = ('owner', 'name')

class RepositoryLanguage(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    code_size = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ("repository", "language")