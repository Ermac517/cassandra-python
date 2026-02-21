"""Tests for Cassandra table module."""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from cassandra_python.table import CassandraTable


class TestCassandraTable(unittest.TestCase):
    """Test cases for CassandraTable class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_session = Mock()
        self.keyspace = "test_keyspace"
        self.table_name = "test_table"
        self.table = CassandraTable(self.mock_session, self.keyspace, self.table_name)

    def test_initialization(self):
        """Test CassandraTable initialization."""
        self.assertEqual(self.table.session, self.mock_session)
        self.assertEqual(self.table.keyspace, self.keyspace)
        self.assertEqual(self.table.table_name, self.table_name)

    def test_create_table(self):
        """Test creating a table."""
        schema = "id UUID PRIMARY KEY, name TEXT, age INT"
        self.table.create_table(schema)

        expected_query = (
            f"CREATE TABLE IF NOT EXISTS {self.keyspace}.{self.table_name} ({schema})"
        )
        self.mock_session.execute.assert_called_once_with(expected_query)

    def test_drop_table(self):
        """Test dropping a table."""
        self.table.drop_table()

        expected_query = f"DROP TABLE IF EXISTS {self.keyspace}.{self.table_name}"
        self.mock_session.execute.assert_called_once_with(expected_query)

    def test_insert_data_single_row(self):
        """Test inserting a single row."""
        data = {"id": "123", "name": "John", "age": 30}
        self.table.insert_data(data)

        # Check the query format
        call_args = self.mock_session.execute.call_args
        query = call_args[0][0]
        values = call_args[0][1]

        self.assertIn("INSERT INTO", query)
        self.assertIn(self.keyspace, query)
        self.assertIn(self.table_name, query)
        self.assertIn("id", query)
        self.assertIn("name", query)
        self.assertIn("age", query)
        self.assertEqual(values, ("123", "John", 30))

    def test_insert_data_multiple_columns(self):
        """Test inserting data with various data types."""
        data = {"id": "456", "name": "Jane", "age": 25, "email": "jane@example.com"}
        self.table.insert_data(data)

        call_args = self.mock_session.execute.call_args
        query = call_args[0][0]
        values = call_args[0][1]

        # Verify all columns are in the query
        self.assertIn("id", query)
        self.assertIn("name", query)
        self.assertIn("age", query)
        self.assertIn("email", query)
        # Verify values are passed as tuple
        self.assertEqual(len(values), 4)

    def test_query_data_without_condition(self):
        """Test querying data without any condition."""
        mock_result = [{"id": "123", "name": "John", "age": 30}]
        self.mock_session.execute.return_value = mock_result

        result = self.table.query_data()

        expected_query = f"SELECT * FROM {self.keyspace}.{self.table_name}"
        self.mock_session.execute.assert_called_once_with(expected_query)
        self.assertEqual(result, mock_result)

    def test_query_data_with_condition(self):
        """Test querying data with a WHERE condition."""
        mock_result = [{"id": "123", "name": "John", "age": 30}]
        self.mock_session.execute.return_value = mock_result

        condition = "age > 25"
        result = self.table.query_data(condition)

        expected_query = f"SELECT * FROM {self.keyspace}.{self.table_name} WHERE {condition} ALLOW FILTERING"
        self.mock_session.execute.assert_called_once_with(expected_query)
        self.assertEqual(result, mock_result)

    def test_query_data_with_complex_condition(self):
        """Test querying data with a complex WHERE condition."""
        mock_result = [{"id": "123", "name": "John", "age": 30}]
        self.mock_session.execute.return_value = mock_result

        condition = "age > 25 AND name = 'John'"
        result = self.table.query_data(condition)

        expected_query = f"SELECT * FROM {self.keyspace}.{self.table_name} WHERE {condition} ALLOW FILTERING"
        self.mock_session.execute.assert_called_once_with(expected_query)

    def test_query_data_empty_result(self):
        """Test querying data that returns no results."""
        self.mock_session.execute.return_value = []

        result = self.table.query_data("age > 100")

        self.assertEqual(result, [])
        self.mock_session.execute.assert_called_once()

    def test_create_table_with_complex_schema(self):
        """Test creating a table with a complex schema."""
        schema = "id UUID PRIMARY KEY, name TEXT, age INT, created_at TIMESTAMP, tags SET<TEXT>"
        self.table.create_table(schema)

        expected_query = (
            f"CREATE TABLE IF NOT EXISTS {self.keyspace}.{self.table_name} ({schema})"
        )
        self.mock_session.execute.assert_called_once_with(expected_query)

    def test_insert_data_empty_dict(self):
        """Test inserting empty data dictionary."""
        data = {}
        self.table.insert_data(data)

        call_args = self.mock_session.execute.call_args
        query = call_args[0][0]
        values = call_args[0][1]

        self.assertIn("INSERT INTO", query)
        self.assertEqual(values, ())

    def test_table_with_different_keyspace_and_name(self):
        """Test table with different keyspace and table names."""
        keyspace = "my_keyspace"
        table_name = "my_table"
        table = CassandraTable(self.mock_session, keyspace, table_name)

        table.drop_table()

        expected_query = f"DROP TABLE IF EXISTS {keyspace}.{table_name}"
        self.mock_session.execute.assert_called_once_with(expected_query)

    def test_query_data_with_limit(self):
        """Test querying data with a LIMIT condition."""
        mock_result = [{"id": "1", "name": "User1"}, {"id": "2", "name": "User2"}]
        self.mock_session.execute.return_value = mock_result

        condition = "age > 20 LIMIT 10"
        result = self.table.query_data(condition)

        expected_query = f"SELECT * FROM {self.keyspace}.{self.table_name} WHERE {condition} ALLOW FILTERING"
        self.mock_session.execute.assert_called_once_with(expected_query)


if __name__ == "__main__":
    unittest.main()
