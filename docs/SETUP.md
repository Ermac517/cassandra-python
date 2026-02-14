# Setup Guide

## Prerequisites

- Python 3.8 or higher
- Apache Cassandra 4.0 or higher

## Installation

### 1. Clone the repository
```bash
cd /path/to/cassandra-python
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Cassandra connection
Edit `config/config.yaml` with your Cassandra cluster details:
```yaml
cassandra:
  hosts:
    - your-cassandra-host
  port: 9042
  keyspace: your_keyspace
```

## Running Tests

```bash
pytest                    # Run all tests
pytest -v               # Verbose output
pytest --cov           # With coverage report
```

## Project Structure

```
cassandra-python/
├── src/
│   └── cassandra_python/       # Main package
│       ├── __init__.py
│       └── connection.py       # Cassandra connection module
├── tests/                      # Test suite
│       └── test_connection.py
├── config/                     # Configuration files
│       └── config.yaml
├── queries/                    # SQL queries
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project configuration
├── .gitignore                 # Git ignore rules
└── README.md                  # Project README
```

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `pytest`
4. Format code: `black src/ tests/`
5. Run linter: `flake8 src/ tests/`
6. Commit and push your changes

## Resources

- [Cassandra Python Driver Documentation](https://docs.datastax.com/en/developer/python-driver/3.29/index.html)
- [Apache Cassandra Documentation](https://cassandra.apache.org/doc/)
