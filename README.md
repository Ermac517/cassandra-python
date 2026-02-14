# cassandra-python

This project is dedicated to testing Python Cassandra API methods and their interactions with Apache Cassandra database. It provides examples and test cases for various Cassandra operations using the Python driver.

## Requirements

- Python 3.8 or higher
- cassandra-driver installed
- Docker (for running Cassandra in a container)

This project is specifically designed to work with Cassandra 4+ to take advantage of the latest features and improvements in the Cassandra ecosystem.

## Quick Start - Running Cassandra with Docker

### Prerequisites
- Docker installed on your system ([Install Docker](https://docs.docker.com/get-docker/))

### 1. Pull the Cassandra Image

```bash
docker pull cassandra:latest
```

Or specify a specific version:
```bash
docker pull cassandra:4.1
```

### 2. Run Cassandra Container

**Basic (Single Node)**
```bash
docker run --name cassandra -p 9042:9042 -e CASSANDRA_RACK=RAC1 -e CASSANDRA_DC=DC1 -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -d cassandra:latest
```

**With Data Persistence**
```bash
docker run --name cassandra \
  -p 9042:9042 \
  -e CASSANDRA_RACK=RAC1 \
  -e CASSANDRA_DC=DC1 \
  -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch \
  -v cassandra_data:/var/lib/cassandra \
  -d cassandra:latest
```

**With Custom Network (for multi-container setup)**
```bash
docker network create cassandra-network

docker run --name cassandra \
  --network cassandra-network \
  -p 9042:9042 \
  -e CASSANDRA_RACK=RAC1 \
  -e CASSANDRA_DC=DC1 \
  -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch \
  -v cassandra_data:/var/lib/cassandra \
  -d cassandra:latest
```

### 3. Verify Cassandra is Running

Check container status:
```bash
docker ps | grep cassandra
```

Wait for Cassandra to be ready (~30 seconds):
```bash
docker logs cassandra | grep -i "state jump to NORMAL"
```

Connect using cqlsh:
```bash
docker exec -it cassandra cqlsh
```

### 4. Set Up Python Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python -m cassandra_python.main
```

Or use the shortcut:
```bash
./venv/bin/python -m cassandra_python.main
```

### Useful Docker Commands

Stop Cassandra:
```bash
docker stop cassandra
```

Start Cassandra:
```bash
docker start cassandra
```

Remove Cassandra container:
```bash
docker rm cassandra
```

Remove data volume:
```bash
docker volume rm cassandra_data
```

View logs:
```bash
docker logs -f cassandra
```

## Running Tests

```bash
pytest                    # Run all tests
pytest -v               # Verbose output
pytest --cov           # With coverage report
```

## Project Structure

See [SETUP.md](docs/SETUP.md) for detailed project structure and development workflow.