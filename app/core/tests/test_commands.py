"""
Tests for custom Django management commands.

This module contains test cases for verifying
the behavior of custom management commands.
Specifically, it tests the `wait_for_db` command
to ensure it correctly handles scenarios
where the database is either available or unavailable.

Dependencies:
- unittest.mock.patch
- psycopg2.OperationalError
- django.core.management.call_command
- django.db.utils.OperationalError
- django.test.SimpleTestCase
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Tests for custom Django management commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test the `wait_for_db` command when the database is available."""
        patched_check.return_value = True

        call_command("wait_for_db")

        # Ensure the `check` method was called once with the correct arguments
        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test the `wait_for_db` command handling
        delays due to OperationalError."""
        # Simulate a sequence where the database
        # is unavailable initially but becomes available later
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        # Verify that the `check` method
        # was called the expected number of times
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
