"""
Connection module for Apache Cassandra.
Handles cluster connection and session management.
"""

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import logging

logger = logging.getLogger(__name__)


class CassandraConnection:
    """Class to manage Cassandra cluster connection and session."""

    def __init__(self, hosts, port=9042, username=None, password=None):
        """
        Initialize Cassandra connection.

        Args:
            hosts (list): List of Cassandra node addresses
            port (int): Cassandra port (default: 9042)
            username (str): Username for authentication (optional)
            password (str): Password for authentication (optional)
        """
        self.hosts = hosts
        self.port = port
        self.username = username
        self.password = password
        self.cluster = None
        self.session = None

    def connect(self, keyspace=None):
        """
        Establish connection to Cassandra cluster.

        Args:
            keyspace (str): Keyspace to connect to (optional)

        Returns:
            session: Active Cassandra session
        """
        try:
            auth_provider = None
            if self.username and self.password:
                auth_provider = PlainTextAuthProvider(
                    username=self.username, password=self.password
                )

            self.cluster = Cluster(
                contact_points=self.hosts, port=self.port, auth_provider=auth_provider
            )
            self.session = self.cluster.connect(keyspace)
            logger.info(f"Connected to Cassandra cluster at {self.hosts}")
            return self.session
        except Exception as e:
            logger.error(f"Failed to connect to Cassandra: {str(e)}")
            raise

    def disconnect(self):
        """Close connection to Cassandra cluster."""
        if self.session:
            self.session.shutdown()
        if self.cluster:
            self.cluster.shutdown()
        logger.info("Disconnected from Cassandra cluster")

    def get_session(self):
        """
        Get active session.

        Returns:
            session: Active Cassandra session
        """
        return self.session
