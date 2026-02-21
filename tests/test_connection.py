"""Tests for Cassandra connection module."""

import unittest
from unittest.mock import Mock, patch, MagicMock
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

    @patch("cassandra_python.connection.Cluster")
    def test_connect_without_keyspace(self, mock_cluster_class):
        """Test connecting to cluster without keyspace."""
        # Setup mock
        mock_cluster = Mock()
        mock_session = Mock()
        mock_cluster.connect.return_value = mock_session
        mock_cluster_class.return_value = mock_cluster

        # Test connection
        conn = CassandraConnection(self.hosts, self.port)
        session = conn.connect()

        # Assertions
        mock_cluster_class.assert_called_once_with(
            contact_points=self.hosts, port=self.port, auth_provider=None
        )
        mock_cluster.connect.assert_called_once_with(None)
        self.assertEqual(session, mock_session)
        self.assertEqual(conn.session, mock_session)
        self.assertEqual(conn.cluster, mock_cluster)

    @patch("cassandra_python.connection.Cluster")
    def test_connect_with_keyspace(self, mock_cluster_class):
        """Test connecting to cluster with keyspace."""
        # Setup mock
        mock_cluster = Mock()
        mock_session = Mock()
        mock_cluster.connect.return_value = mock_session
        mock_cluster_class.return_value = mock_cluster

        # Test connection
        conn = CassandraConnection(self.hosts, self.port)
        session = conn.connect(keyspace="test_keyspace")

        # Assertions
        mock_cluster.connect.assert_called_once_with("test_keyspace")
        self.assertEqual(session, mock_session)

    @patch("cassandra_python.connection.PlainTextAuthProvider")
    @patch("cassandra_python.connection.Cluster")
    def test_connect_with_auth(self, mock_cluster_class, mock_auth_provider_class):
        """Test connecting with authentication."""
        # Setup mocks
        mock_cluster = Mock()
        mock_session = Mock()
        mock_auth_provider = Mock()
        mock_cluster.connect.return_value = mock_session
        mock_cluster_class.return_value = mock_cluster
        mock_auth_provider_class.return_value = mock_auth_provider

        # Test connection with auth
        conn = CassandraConnection(
            self.hosts, self.port, username="test_user", password="test_pass"
        )
        session = conn.connect()

        # Assertions
        mock_auth_provider_class.assert_called_once_with(
            username="test_user", password="test_pass"
        )
        mock_cluster_class.assert_called_once_with(
            contact_points=self.hosts, port=self.port, auth_provider=mock_auth_provider
        )
        self.assertEqual(session, mock_session)

    @patch("cassandra_python.connection.Cluster")
    def test_connect_failure(self, mock_cluster_class):
        """Test connection failure handling."""
        # Setup mock to raise exception
        mock_cluster_class.side_effect = Exception("Connection failed")

        # Test connection failure
        conn = CassandraConnection(self.hosts, self.port)

        with self.assertRaises(Exception) as context:
            conn.connect()

        self.assertIn("Connection failed", str(context.exception))

    def test_disconnect(self):
        """Test disconnecting from cluster."""
        conn = CassandraConnection(self.hosts, self.port)
        conn.session = Mock()
        conn.cluster = Mock()

        conn.disconnect()

        conn.session.shutdown.assert_called_once()
        conn.cluster.shutdown.assert_called_once()

    def test_disconnect_no_active_connection(self):
        """Test disconnect when no active connection exists."""
        conn = CassandraConnection(self.hosts, self.port)
        # Should not raise an error
        conn.disconnect()

    def test_get_session(self):
        """Test getting active session."""
        conn = CassandraConnection(self.hosts, self.port)
        mock_session = Mock()
        conn.session = mock_session

        session = conn.get_session()
        self.assertEqual(session, mock_session)

    def test_get_session_none(self):
        """Test getting session when none is active."""
        conn = CassandraConnection(self.hosts, self.port)
        session = conn.get_session()
        self.assertIsNone(session)


if __name__ == "__main__":
    unittest.main()
