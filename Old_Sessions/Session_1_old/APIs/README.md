# FastAPI Parameter Passing & Authentication Examples

A comprehensive FastAPI application demonstrating different ways to pass parameters and implement authentication.

## 📋 Features

### Parameter Passing Methods
1. **Query Parameters** - Pass data in URL query string
2. **Request Body** - Pass data in JSON body
3. **Headers** - Pass data in HTTP headers

### Authentication Methods
1. **API Key (Header)** - `X-API-Key` header
2. **API Key (Query)** - `api_key` query parameter
3. **Bearer Token** - OAuth 2.0 style authentication
4. **Basic Auth** - Username:Password authentication

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### 3. Test the API

**Option A: Run the test script**
```bash
python test_api.py
```

**Option B: Use the interactive documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📖 API Endpoints

### Parameter Passing Examples

#### 1. Query Parameters
```bash
# GET request with query parameters
curl "http://localhost:8000/sum/query?num1=5&num2=10"

# Response
{
  "result": 15.0,
  "method": "query_parameters"
}
```

#### 2. Request Body
```bash
# POST request with JSON body
curl -X POST "http://localhost:8000/sum/body" \
  -H "Content-Type: application/json" \
  -d '{"num1": 30, "num2": 12}'

# Response
{
  "result": 42.0,
  "method": "request_body"
}
```

#### 3. Headers
```bash
# GET request with custom headers
curl "http://localhost:8000/sum/header" \
  -H "X-Num1: 7.5" \
  -H "X-Num2: 2.5"

# Response
{
  "result": 10.0,
  "method": "header_parameters"
}
```

### Authentication Examples

#### 1. API Key in Header
```bash
curl "http://localhost:8000/auth/api-key-header?num1=100&num2=50" \
  -H "X-API-Key: my-secret-api-key-123"

# Response
{
  "result": 150.0,
  "auth_method": "api_key_header",
  "authenticated": true
}
```

**Invalid API Key:**
```bash
curl "http://localhost:8000/auth/api-key-header?num1=100&num2=50" \
  -H "X-API-Key: invalid-key"

# Response (401 Unauthorized)
{
  "detail": "Invalid or missing API Key"
}
```

#### 2. API Key in Query
```bash
curl "http://localhost:8000/auth/api-key-query?num1=80&num2=20&api_key=my-secret-api-key-123"

# Response
{
  "result": 100.0,
  "auth_method": "api_key_query",
  "authenticated": true
}
```

#### 3. Bearer Token (OAuth 2.0)
```bash
curl -X POST "http://localhost:8000/auth/bearer" \
  -H "Authorization: Bearer valid-bearer-token-xyz" \
  -H "Content-Type: application/json" \
  -d '{"num1": 45, "num2": 55}'

# Response
{
  "result": 100.0,
  "auth_method": "bearer_token",
  "authenticated": true
}
```

#### 4. Basic Authentication
```bash
# Using username:password
curl -X POST "http://localhost:8000/auth/basic" \
  -u admin:secret123 \
  -H "Content-Type: application/json" \
  -d '{"num1": 33, "num2": 67}'

# Response
{
  "result": 100.0,
  "auth_method": "basic_auth",
  "username": "admin",
  "authenticated": true
}
```

**Manual Basic Auth Header:**
```bash
# Base64 encode "admin:secret123" = "YWRtaW46c2VjcmV0MTIz"
curl -X POST "http://localhost:8000/auth/basic" \
  -H "Authorization: Basic YWRtaW46c2VjcmV0MTIz" \
  -H "Content-Type: application/json" \
  -d '{"num1": 33, "num2": 67}'
```

### Combined Example

```bash
# Demonstrates body + query + header + authentication
curl -X POST "http://localhost:8000/combined/all-methods?multiplier=2.5" \
  -H "X-API-Key: my-secret-api-key-123" \
  -H "X-Operation: sum" \
  -H "Content-Type: application/json" \
  -d '{"num1": 10, "num2": 20}'

# Response
{
  "result": 75.0,      # (10 + 20) * 2.5
  "operation": "sum",
  "multiplier": 2.5,
  "authenticated": true
}
```

## 🔑 Test Credentials

```python
API_KEY = "my-secret-api-key-123"
BEARER_TOKEN = "valid-bearer-token-xyz"
USERNAME = "admin"
PASSWORD = "secret123"
```

## 📚 Python Client Examples

### Using `requests` library

```python
import requests
import base64

BASE_URL = "http://localhost:8000"

# 1. Query Parameters
response = requests.get(f"{BASE_URL}/sum/query", params={"num1": 5, "num2": 10})
print(response.json())

# 2. Request Body
response = requests.post(f"{BASE_URL}/sum/body", json={"num1": 30, "num2": 12})
print(response.json())

# 3. Headers
headers = {"X-Num1": "7.5", "X-Num2": "2.5"}
response = requests.get(f"{BASE_URL}/sum/header", headers=headers)
print(response.json())

# 4. API Key in Header
headers = {"X-API-Key": "my-secret-api-key-123"}
params = {"num1": 100, "num2": 50}
response = requests.get(f"{BASE_URL}/auth/api-key-header", headers=headers, params=params)
print(response.json())

# 5. API Key in Query
params = {"num1": 80, "num2": 20, "api_key": "my-secret-api-key-123"}
response = requests.get(f"{BASE_URL}/auth/api-key-query", params=params)
print(response.json())

# 6. Bearer Token
headers = {"Authorization": "Bearer valid-bearer-token-xyz"}
data = {"num1": 45, "num2": 55}
response = requests.post(f"{BASE_URL}/auth/bearer", headers=headers, json=data)
print(response.json())

# 7. Basic Auth
response = requests.post(
    f"{BASE_URL}/auth/basic",
    json={"num1": 33, "num2": 67},
    auth=("admin", "secret123")
)
print(response.json())

# 8. Combined
headers = {
    "X-API-Key": "my-secret-api-key-123",
    "X-Operation": "sum"
}
params = {"multiplier": 2.5}
data = {"num1": 10, "num2": 20}
response = requests.post(
    f"{BASE_URL}/combined/all-methods",
    headers=headers,
    params=params,
    json=data
)
print(response.json())
```

## 🏗️ Project Structure

```
.
├── main.py              # FastAPI application
├── test_api.py          # Automated test script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔒 Security Notes

⚠️ **Important**: This is for educational purposes only!

In production:
- **Never** hardcode credentials
- Use environment variables for secrets
- Hash passwords (use `passlib` with bcrypt)
- Use proper OAuth 2.0 flows
- Implement rate limiting
- Use HTTPS only
- Store API keys in a database
- Implement token expiration
- Add logging and monitoring

## 📝 Key Concepts

### Dependency Injection
FastAPI uses dependency injection for:
- Authentication verification
- Shared logic
- Database connections
- Configuration

```python
def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401)
    return api_key

@app.get("/protected")
def protected_route(api_key: str = Depends(verify_api_key)):
    return {"message": "Access granted"}
```

### Pydantic Models
Used for request/response validation:

```python
class SumRequest(BaseModel):
    num1: float
    num2: float
```

Benefits:
- Automatic validation
- Type checking
- Auto-generated documentation
- Serialization/deserialization

## 🎯 Use Cases

1. **Query Parameters**: Simple filtering, pagination, sorting
2. **Request Body**: Creating/updating resources, complex data
3. **Headers**: Authentication, content negotiation, metadata
4. **API Key**: Simple API access control
5. **Bearer Token**: OAuth 2.0, JWT authentication
6. **Basic Auth**: Legacy systems, simple services

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use a different port
uvicorn main:app --port 8001
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Authentication fails
- Check credentials match exactly
- Verify header names (case-sensitive)
- Check for extra spaces in tokens

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [HTTP Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication)

## License

MIT License - feel free to use for learning and projects!