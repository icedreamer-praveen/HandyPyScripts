from cryptography.fernet import Fernet
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate a new Fernet key'

    def handle(self, *args, **kwargs):
        """
        The function generates an encryption/decryption key and prints it to the console.
        """
        key = Fernet.generate_key()
        self.stdout.write(self.style.SUCCESS(f'Your encrypt/decrypt key: {key.decode()}'))
