# API Agent

**API Agent** is an AI Assistant that allows users to upload API specs, normalize them, define scenarios, and automatically generate Q&A Agents capable of calling real-time APIs to answer user questions.

## Features

### 1. API Setup

* Upload and parse OpenAPI 3.x specifications
* Automatically detect issues and missing descriptions
* AI suggestions for improving API documentation
* Chat interface to refine the API spec

### 2. Scenario Setup

* Define Q&A scenarios
* AI automatically suggests scenarios from API semantics
* Mapping entities → API parameters
* Response templates using Jinja2

### 3. Agent Creation

* Finalize and create Q&A Agent
* Supports multiple authentication methods
* Mock API mode for testing

### 4. Q&A Chat

* Scenario matching with AI
* Entity extraction from user queries
* Real-time API execution
* Template rendering for responses

## Architecture

```
api-agent/
├── core/           # Core application logic
│   └── app.py      # Main APIAgentApp class
├── models/         # Pydantic models
│   └── schemas.py  # All data models
├── services/       # Business logic services
│   ├── openapi_parser.py   # OpenAPI parsing
│   ├── ai_service.py       # Claude AI integration
│   ├── session_manager.py  # Session & storage
│   ├── api_executor.py     # API call execution
│   └── template_renderer.py # Jinja2 templates
├── agents/         # Q&A Agent implementation
│   └── qa_agent.py
├── api/            # FastAPI routes
│   └── routes.py
├── streamlit_app.py  # Demo UI
├── main.py         # Entry point
└── requirements.txt
```

## Installation

```bash
# Clone/copy the project
cd api-agent

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### Run Streamlit Demo

```bash
# Set API key
export OPENAI_API_KEY="your-api-key"

# Run demo
streamlit run streamlit_app.py
```

### Run FastAPI Server

```bash
# Set API key
export OPENAI_API_KEY="your-api-key"

# Run API server
python main.py api

# Or with uvicorn directly
uvicorn api.routes:app --reload
```

## API Endpoints

### Sessions

* `POST /sessions` - Create new session
* `GET /sessions` - List sessions
* `GET /sessions/{id}` - Get session details

### API Spec

* `POST /sessions/{id}/api-spec` - Upload API spec
* `GET /sessions/{id}/api-spec` - Get parsed API spec
* `POST /sessions/{id}/api-spec/refine` - Refine with AI

### Scenarios

* `GET /sessions/{id}/scenarios` - List scenarios
* `POST /sessions/{id}/scenarios` - Create scenario
* `POST /sessions/{id}/scenarios/suggest` - Get AI suggestions
* `PUT /sessions/{id}/scenarios/{scenario_id}` - Update scenario
* `DELETE /sessions/{id}/scenarios/{scenario_id}` - Delete scenario

### Agents

* `POST /sessions/{id}/finalize` - Create agent
* `GET /agents` - List agents
* `GET /agents/{id}` - Get agent details
* `POST /agents/{id}/chat` - Chat with agent

## Example Workflow

### 1. Upload API Spec

```python
import httpx

# Create session
response = httpx.post("http://localhost:8167/sessions")
session_id = response.json()["session_id"]

# Upload spec
with open("openapi.yaml") as f:
    content = f.read()

response = httpx.post(
    f"http://localhost:8167/sessions/{session_id}/api-spec",
    data={"content": content, "format": "yaml"}
)
print(response.json())
```

### 2. Define Scenario

```python
scenario = {
    "name": "Get Product Info",
    "description": "Get information about a product",
    "sample_questions": [
        "Thông tin sản phẩm XYZ?",
        "Giá của sản phẩm ABC là bao nhiêu?"
    ],
    "required_entities": ["product_id"],
    "api_mapping": {
        "endpoint_path": "/products/{productId}",
        "method": "GET",
        "parameter_mappings": [
            {"entity_name": "product_id", "api_parameter": "productId"}
        ]
    },
    "response_template": "**{{ name }}**\n- Price: {{ price | format_currency }}\n- Stock: {{ stock }}"
}

response = httpx.post(
    f"http://localhost:8167/sessions/{session_id}/scenarios",
    json=scenario
)
```

### 3. Create Agent

```python
response = httpx.post(
    f"http://localhost:8167/sessions/{session_id}/finalize",
    json={
        "name": "E-Commerce Agent",
        "use_mock_api": True  # For testing
    }
)
agent_id = response.json()["agent_id"]
```

### 4. Chat with Agent

```python
response = httpx.post(
    f"http://localhost:8167/agents/{agent_id}/chat",
    json={"question": "Thông tin sản phẩm Laptop Pro?"}
)
print(response.json()["answer"])
```

## Response Templates

Templates use Jinja2 syntax with custom filters:

```jinja2
**{{ name }}**
- Price: {{ price | format_currency }}
- Discount: {{ discount | format_number(2) }}%
- Date: {{ created_at | format_date('%d/%m/%Y') }}
- Description: {{ description | truncate_text(100) }}
```

### Available Filters

* `format_number(decimal_places)` - Format number with separators
* `format_currency(currency='VND')` - Format as currency
* `format_date(format)` - Format date string
* `truncate_text(length)` - Truncate with ellipsis
* `json_pretty(indent)` - Pretty print JSON

## Authentication

Supported auth types:

```python
# Bearer Token
auth_config = {
    "type": "bearer",
    "token": "your-token"
}

# API Key
auth_config = {
    "type": "api_key",
    "key_name": "X-API-Key",
    "key_value": "your-key",
    "key_location": "header"
}

# Basic Auth
auth_config = {
    "type": "basic",
    "username": "user",
    "password": "pass"
}
```

## Development

```bash
# Install dev dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

## License

MIT License
