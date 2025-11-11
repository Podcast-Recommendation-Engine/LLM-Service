# LLM Service

A concurrent data enrichment pipeline that processes text chunks using Large Language Models via gRPC communication.

## Overview

This service implements a distributed architecture for processing and enriching text data through semantic analysis. The system breaks down large text documents into manageable chunks, processes them concurrently using LLM models, and aggregates the results into comprehensive metadata.

## Features

- **Concurrent Processing**: Parallel chunk processing for improved performance
- **gRPC Communication**: Efficient client-server communication protocol
- **Docker Support**: Complete containerized deployment
- **Configurable Pipeline**: Flexible configuration for different use cases
- **Multi-stage Processing**: Bronze, Silver, and Gold data layers
- **LLM Integration**: Seamless integration with Ollama for text analysis

## Architecture

The system consists of three main components:

1. **gRPC Server**: Handles LLM requests and responses
2. **Processing Pipeline**: Manages data flow and chunk processing
3. **Ollama Service**: Provides LLM capabilities for text analysis

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.13 or higher (for local development)
- Ollama service

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Podcast-Recommendation-Engine/LLM-Service.git
cd LLM-Service
```

2. Set up environment variables:
```bash
cp .env.dev .env
```

3. Create required data directories:
```bash
mkdir -p data/bronze data/silver data/gold
```

4. Start the services using Docker Compose:
```bash
cd docker
docker-compose up --build -d
```

5. Pull the required Ollama model:
```bash
ollama pull llama3.2:3b
```

6. Run the application:
```bash
python src/main.py
```

## Configuration

The application uses environment variables for configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_HOST` | Ollama service host | localhost |
| `OLLAMA_PORT` | Service port | 50051 |
| `CHUNK_SIZE` | Text chunk size for processing | 2000 |
| `MAX_TOKENS` | Maximum tokens per LLM request | 2000 |
| `OVERLAP_SENTENCES` | Sentence overlap between chunks | 20 |
| `MODEL_NAME` | LLM model to use | llama3.2:3b |
| `MAX_WORKERS` | Maximum concurrent workers | 4 |

## Usage

### Processing Text Data

1. Place your input text file in the `data/bronze/` directory
2. Run the pipeline to process the data
3. Results will be available in:
   - `data/silver/`: Intermediate processing results
   - `data/gold/`: Final aggregated metadata

### API Endpoints

The gRPC service provides two main endpoints:

- **GenerateChunk**: Processes individual text chunks
- **AggregateChunks**: Combines chunk metadata into final results

## Data Processing Pipeline

1. **Bronze Layer**: Raw input data (transcript.txt)
2. **Silver Layer**: Processed chunks and intermediate results
3. **Gold Layer**: Final aggregated episode metadata


### Viewing Logs

```bash
# View all service logs (from docker directory)
cd docker
docker-compose logs -f

# View specific service logs
docker logs -f llm-grpc-server
docker logs -f ollama
```

## Development

### Protocol Buffers

The service uses Protocol Buffers for gRPC communication. The proto files are automatically compiled during the Docker build process.


## Performance Considerations

- Adjust `MAX_WORKERS` based on available resources
- Optimize `CHUNK_SIZE` for your specific use case
- Consider using larger LLM models for better results
- Monitor memory usage during concurrent processing

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure Ollama service is running
2. **DNS Resolution**: Check container names in Docker environment
3. **Out of Memory**: Reduce `MAX_WORKERS` or `CHUNK_SIZE`
4. **Slow Processing**: Consider using a more powerful LLM model

### Debug Mode

Enable detailed logging by viewing container logs:

```bash
docker logs -f llm-grpc-server
```

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue in the repository.
