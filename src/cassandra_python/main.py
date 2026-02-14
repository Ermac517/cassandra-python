"""
Main module for Cassandra Python project.
Example usage of Cassandra connection and operations.
"""

import logging
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cassandra_python.connection import CassandraConnection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the application."""
    logger.info("Starting Cassandra Python application")

    # Example: Initialize connection
    conn = CassandraConnection(
         hosts=['localhost'],
         port=9042
    )
    session = conn.connect(keyspace='demo')
     
    logger.info("Connected successfully")
     
    conn.disconnect()
    logger.info("Disconnected")


if __name__ == "__main__":
    main()
