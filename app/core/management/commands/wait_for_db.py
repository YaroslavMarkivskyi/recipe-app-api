"""
Django management command to wait for the database to become available.

This command attempts to connect
to the database and waits until it is available.
It is useful for ensuring that the database
is ready before running other commands
or deploying the application.

Dependencies:
- psycopg2 (for PostgreSQL database connection)
- django.db.utils.OperationalError (Django database error)

Usage:
    Run this command using: `python manage.py wait_for_db`
"""

import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django management command to wait for the database to be available."""

    def handle(self, *args, **options):
        """Handle the command execution."""
        self.stdout.write("Waiting for database...")
        db_up = False

        while not db_up:
            try:
                # Check the database connection
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                # Log the unavailability and wait before retrying
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
