# Amazon Product Search MCP Server

An MCP (Model Context Protocol) server that provides AI-powered Amazon product search and recommendations using FastMCP.

## Features

- 🔍 Smart product search with Amazon API
- 🤖 AI-powered product recommendations using Hugging Face
- 💰 Price range filtering
- 📋 Feature-based matching
- 🎯 Tailored recommendations for Small/Medium Enterprises

## Installation

1. Clone this repository and navigate to the project directory
2. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

## Server Setup

### Running the MCP Server

```bash
# Activate your virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the server
python main.py
```

The server exposes one main tool:
- `getdata`: Search Amazon products with AI recommendations

## Client Options

We provide multiple client implementations to interact with your MCP server:

### 1. Python Interactive Client (`client.py`)

A full-featured Python client with examples and interactive mode.

```bash
python client.py
```

Features:
- Pre-built examples (laptops, smartphones)
- Interactive search mode
- Real-time communication with MCP server

### 2. Command Line Interface (`cli_client.py`)

Quick command-line searches for automation and scripting.

```bash
# Basic search
python cli_client.py "laptop"

# With features and price range
python cli_client.py "laptop" --features "8GB RAM, SSD storage" --min-price 30000 --max-price 80000

# Smartphone search
python cli_client.py "smartphone" --features "good camera, 5G" --min-price 15000 --max-price 50000
```

Arguments:
- `product`: Product to search for (required)
- `--features`, `-f`: Specific features to look for
- `--min-price`, `-min`: Minimum price in rupees
- `--max-price`, `-max`: Maximum price in rupees

### 3. Web Interface (`web_client.py`)

A beautiful web interface with REST API backend.

```bash
# Install additional dependencies
pip install fastapi uvicorn

# Run the web server
python web_client.py
```

Then open http://localhost:8000 in your browser for a user-friendly interface.

API Endpoints:
- `GET /`: Web interface
- `POST /search`: REST API for product search
- `GET /health`: Health check

### 4. MCP CLI Integration

You can also use the MCP CLI to interact with your server:

```bash
# Install MCP CLI if not already installed
pip install mcp

# Connect to your server
mcp connect stdio -- python main.py
```

## Usage Examples

### Example 1: Laptop Search
```json
{
    "product": "laptop",
    "specific_features": "8GB RAM, SSD storage, good for programming",
    "min_price": 30000,
    "max_price": 80000
}
```

### Example 2: Smartphone Search
```json
{
    "product": "smartphone",
    "specific_features": "good camera, long battery life, 5G support",
    "min_price": 15000,
    "max_price": 50000
}
```

### Example 3: Budget Headphones
```json
{
    "product": "wireless headphones",
    "specific_features": "noise cancellation, comfortable",
    "min_price": 1000,
    "max_price": 5000
}
```

## Configuration

### API Keys Required

Make sure you have:
1. **Hugging Face API Token**: Update `HF_API_TOKEN` in `server/buy.py`
2. **RapidAPI Key**: Update the `x-rapidapi-key` in `server/buy.py`

### Customization

You can customize the AI recommendation prompt in the `decision_agent` function in `server/buy.py`.

## Integration with Claude Desktop

To use this MCP server with Claude Desktop, add this configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "amazon-search": {
      "command": "python",
      "args": ["path/to/your/main.py"],
      "env": {}
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the correct virtual environment
2. **API failures**: Check your API keys and internet connection
3. **Connection issues**: Ensure the MCP server is running before starting clients

### Error Messages

- "No result": Usually indicates API issues or no products found
- "Connection refused": MCP server is not running
- "Tool not found": Server initialization issue

## Development

### Adding New Features

1. Add new tools in `server/buy.py` using the `@mcp.tool()` decorator
2. Update client code to use new tools
3. Test with the interactive client first

### Testing

```bash
# Test the server directly
python -c "from server.buy import mcp; print('Server loads successfully')"

# Test with the interactive client
python client.py
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│   MCP Server    │◄──►│  External APIs  │
│  (Your Choice)  │    │   (FastMCP)     │    │ (Amazon/HF AI)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
       │                        │                        │
       ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  • client.py    │    │ • Tool: getdata │    │ • Amazon Search │
│  • cli_client   │    │ • AI Agent      │    │ • HuggingFace   │
│  • web_client   │    │ • FastMCP       │    │ • Recommendations│
│  • Claude       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## License

This project is open source. Please ensure you comply with the terms of service of the APIs used (Amazon, RapidAPI, Hugging Face).

