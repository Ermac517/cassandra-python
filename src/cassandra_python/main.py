"""
Main module for Cassandra Python project.
Example usage of Cassandra connection and operations.
"""

import logging
import os
import sys
from pathlib import Path
from uuid import UUID

import yaml

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cassandra_python.connection import CassandraConnection
from cassandra_python.table import CassandraTable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config(config_path: str = None) -> dict:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to config.yaml. If None, uses default relative path.

    Returns:
        Dictionary containing configuration.
    """
    if config_path is None:
        # Default to config.yaml in the project root
        config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    logger.info(f"Configuration loaded from {config_path}")
    return config


def main():
    """Main entry point for the application."""
    logger.info("Starting Cassandra Python application")

    # Load configuration from YAML
    config = load_config()
    cassandra_config = config.get("cassandra", {})

    # Extract configuration values
    hosts = cassandra_config.get("hosts", ["localhost"])
    port = cassandra_config.get("port", 9042)
    keyspace = cassandra_config.get("keyspace", "demo")

    # Example: Initialize connection
    conn = CassandraConnection(hosts=hosts, port=port)
    session = conn.connect(keyspace=keyspace)

    logger.info("Connected successfully")

    # Example: Table operations
    table = CassandraTable(session, keyspace, "users")
    table.create_table("id UUID PRIMARY KEY, name TEXT, age INT")
    # Convert UUID string to UUID object
    table.insert_data(
        {
            "id": UUID("123e4567-e89b-12d3-a456-426614174000"),
            "name": "John Doe",
            "age": 30,
        }
    )
    result = table.query_data("age > 25")
    for row in result:
        logger.info(f"Row: {row}")

    conn.disconnect()
    logger.info("Disconnected")


if __name__ == "__main__":
    main()
