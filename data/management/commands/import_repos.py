from django.core.management.base import BaseCommand
from django.db import transaction
import json
from django.utils.dateparse import parse_datetime
from pathlib import Path
from tqdm import tqdm
from django.core.exceptions import ValidationError
from data.models import Repository, Owner, RepositoryLanguage, Language


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        file_path = Path(options['file_path'])

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, 'r') as f:
            repos = json.load(f)

        total = len(repos)
        self.stdout.write(total)

        for repo in tqdm(repos):
            with transaction.atomic():
                try:
                    owner, _ = Owner.objects.get_or_create(name=repo.get('owner', ''))

                    created_at = parse_datetime(repo.get('createdAt')) if repo.get('createdAt') else None
                    repository, created = Repository.objects.get_or_create(
                        owner=owner,
                        name=repo.get('name', ''),
                        defaults={'createdAt': created_at}
                    )
                    repository.full_clean()

                    for lang in repo.get('languages', []):
                        language, _ = Language.objects.get_or_create(name=lang.get('name', ''))
                        language.full_clean()

                        repo_lang, _ = RepositoryLanguage.objects.get_or_create(
                            repository=repository,
                            language=language,
                            defaults={'code_size': lang.get('size', 0)}
                        )
                        if not _:
                            repo_lang.code_size = lang.get('size', 0)
                            repo_lang.full_clean()
                            repo_lang.save()

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f'Validation error for repo {repo.get("name", "")}: {e}'))
                    continue

        self.stdout.write(self.style.SUCCESS(f'Loaded {total} repositories'))