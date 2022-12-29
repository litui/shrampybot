from django.core.management.base import BaseCommand, CommandError
from django_typomatic import generate_ts
import json


class Command(BaseCommand):
    help = "Generate typescript interfaces for Django models"

    def handle(self, *args, **options):
        generate_ts("../model-ts/all.ts")