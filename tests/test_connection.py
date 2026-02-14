"""Tests for Cassandra connection module."""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from cassandra_python.connection import CassandraConnection


class TestCassandraConnection(unittest.TestCase):
    """Test cases for CassandraConnection class."""

    def setUp(self):
        """Set up test fixtures."""
        self.hosts = ["localhost"]
        self.port = 9042

    def test_initialization(self):
        """Test connection object initialization."""
        conn = CassandraConnection(self.hosts, self.port)
        self.assertEqual(conn.hosts, self.hosts)
        self.assertEqual(conn.port, self.port)
        self.assertIsNone(conn.cluster)
        self.assertIsNone(conn.session)

    def test_initialization_with_auth(self):
        """Test connection initialization with authentication."""
        conn = CassandraConnection(
            self.hosts, self.port, username="user", password="pass"
        )
        self.assertEqual(conn.username, "user")
        self.assertEqual(conn.password, "pass")


if __name__ == "__main__":
    unittest.main()
