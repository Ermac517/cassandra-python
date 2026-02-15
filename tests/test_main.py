"""Tests for main module."""

import unittest
from unittest.mock import Mock, patch, mock_open, MagicMock
import sys
import os
from pathlib import Path
import yaml

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from cassandra_python.main import load_config, main


class TestLoadConfig(unittest.TestCase):
    """Test cases for load_config function."""

    def test_load_config_success(self):
        """Test successfully loading configuration."""
        # Sample config data
        config_data = {
            'cassandra': {
                'hosts': ['localhost', '127.0.0.1'],
                'port': 9042,
                'keyspace': 'test_db'
            },
            'logging': {
                'level': 'INFO'
            }
        }

        # Mock yaml content
        yaml_content = yaml.dump(config_data)
        
        with patch('builtins.open', mock_open(read_data=yaml_content)):
            with patch('pathlib.Path.exists', return_value=True):
                config = load_config('/fake/path/config.yaml')
        
        self.assertEqual(config['cassandra']['hosts'], ['localhost', '127.0.0.1'])
        self.assertEqual(config['cassandra']['port'], 9042)
        self.assertEqual(config['cassandra']['keyspace'], 'test_db')

    def test_load_config_file_not_found(self):
        """Test loading config when file doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError) as context:
                load_config('/fake/path/config.yaml')
            
            self.assertIn('Configuration file not found', str(context.exception))

    def test_load_config_default_path(self):
        """Test loading config with default path."""
        config_data = {
            'cassandra': {
                'hosts': ['localhost'],
                'port': 9042,
                'keyspace': 'demo'
            }
        }
        
        yaml_content = yaml.dump(config_data)
        
        with patch('builtins.open', mock_open(read_data=yaml_content)):
            with patch('pathlib.Path.exists', return_value=True):
                config = load_config()
        
        self.assertIn('cassandra', config)
        self.assertEqual(config['cassandra']['keyspace'], 'demo')

    def test_load_config_invalid_yaml(self):
        """Test loading config with invalid YAML."""
        invalid_yaml = "{ invalid: yaml: content:"
        
        with patch('builtins.open', mock_open(read_data=invalid_yaml)):
            with patch('pathlib.Path.exists', return_value=True):
                with self.assertRaises(yaml.YAMLError):
                    load_config('/fake/path/config.yaml')


class TestMain(unittest.TestCase):
    """Test cases for main function."""

    @patch('cassandra_python.main.load_config')
    @patch('cassandra_python.main.CassandraConnection')
    @patch('cassandra_python.main.CassandraTable')
    def test_main_success(self, mock_table_class, mock_connection_class, mock_load_config):
        """Test main function successful execution."""
        # Setup mocks
        mock_config = {
            'cassandra': {
                'hosts': ['localhost'],
                'port': 9042,
                'keyspace': 'demo'
            }
        }
        mock_load_config.return_value = mock_config
        
        mock_conn = Mock()
        mock_session = Mock()
        mock_conn.connect.return_value = mock_session
        mock_connection_class.return_value = mock_conn

        # Mock table
        mock_table = Mock()
        mock_table.query_data.return_value = [{"id": "1", "name": "John", "age": 30}]
        mock_table_class.return_value = mock_table

        # Run main
        main()

        # Assertions
        mock_load_config.assert_called_once()
        mock_connection_class.assert_called_once_with(
            hosts=['localhost'],
            port=9042
        )
        mock_conn.connect.assert_called_once_with(keyspace='demo')
        mock_table_class.assert_called_once_with(mock_session, 'demo', 'users')
        mock_table.create_table.assert_called_once()
        mock_table.insert_data.assert_called_once()
        mock_table.query_data.assert_called_once_with('age > 25')
        mock_conn.disconnect.assert_called_once()

    @patch('cassandra_python.main.load_config')
    @patch('cassandra_python.main.CassandraConnection')
    @patch('cassandra_python.main.CassandraTable')
    def test_main_with_custom_config(self, mock_table_class, mock_connection_class, mock_load_config):
        """Test main function with custom configuration values."""
        # Setup mocks with custom values
        mock_config = {
            'cassandra': {
                'hosts': ['node1.example.com', 'node2.example.com'],
                'port': 9043,
                'keyspace': 'production'
            }
        }
        mock_load_config.return_value = mock_config
        
        mock_conn = Mock()
        mock_session = Mock()
        mock_conn.connect.return_value = mock_session
        mock_connection_class.return_value = mock_conn

        # Mock table
        mock_table = Mock()
        mock_table.query_data.return_value = []
        mock_table_class.return_value = mock_table

        # Run main
        main()

        # Assertions
        mock_connection_class.assert_called_once_with(
            hosts=['node1.example.com', 'node2.example.com'],
            port=9043
        )
        mock_conn.connect.assert_called_once_with(keyspace='production')
        mock_table_class.assert_called_once_with(mock_session, 'production', 'users')

    @patch('cassandra_python.main.load_config')
    @patch('cassandra_python.main.CassandraConnection')
    @patch('cassandra_python.main.CassandraTable')
    def test_main_with_defaults(self, mock_table_class, mock_connection_class, mock_load_config):
        """Test main function uses defaults when config values are missing."""
        # Setup mocks with empty cassandra config
        mock_config = {'cassandra': {}}
        mock_load_config.return_value = mock_config
        
        mock_conn = Mock()
        mock_session = Mock()
        mock_conn.connect.return_value = mock_session
        mock_connection_class.return_value = mock_conn

        # Mock table
        mock_table = Mock()
        mock_table.query_data.return_value = []
        mock_table_class.return_value = mock_table

        # Run main
        main()

        # Assertions - should use default values
        mock_connection_class.assert_called_once_with(
            hosts=['localhost'],
            port=9042
        )
        mock_conn.connect.assert_called_once_with(keyspace='demo')

    @patch('cassandra_python.main.load_config')
    @patch('cassandra_python.main.CassandraConnection')
    def test_main_connection_error(self, mock_connection_class, mock_load_config):
        """Test main function handles connection errors."""
        # Setup mocks
        mock_config = {
            'cassandra': {
                'hosts': ['localhost'],
                'port': 9042,
                'keyspace': 'demo'
            }
        }
        mock_load_config.return_value = mock_config
        
        mock_conn = Mock()
        mock_conn.connect.side_effect = Exception("Connection failed")
        mock_connection_class.return_value = mock_conn

        # Run main should raise exception
        with self.assertRaises(Exception) as context:
            main()
        
        self.assertIn("Connection failed", str(context.exception))


if __name__ == "__main__":
    unittest.main()
