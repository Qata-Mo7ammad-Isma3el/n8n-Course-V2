from fastapi import FastAPI, Header, Query, Body, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBearer, APIKeyHeader, OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
import secrets


#> Example Public URL
#! cloudflared tunnel --url http://localhost:8000

#> https://assign-enters-lives-necessarily.trycloudflare.com 

app = FastAPI(title="FastAPI Parameter & Auth Examples")

# Security schemes
security_basic = HTTPBasic()
security_bearer = HTTPBearer()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

# Mock credentials (In production, use proper database and hashing)
VALID_API_KEYS = {"my-secret-api-key-123", "another-valid-key-456"}
VALID_BEARER_TOKEN = "valid-bearer-token-xyz"
VALID_USERNAME = "admin"
VALID_PASSWORD = "secret123"

# Pydantic models
class SumRequest(BaseModel):
    num1: float
    num2: float

class SumResponse(BaseModel):
    result: float
    method: str


# ============== AUTHENTICATION DEPENDENCY FUNCTIONS ==============

def verify_api_key_header(api_key: Optional[str] = Depends(api_key_header)):
    """Verify API key passed in header"""
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return api_key

def verify_api_key_query(api_key: str = Query(..., description="API key for authentication")):
    """Verify API key passed in query parameter"""
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key

def verify_bearer_token(credentials: HTTPBearer = Depends(security_bearer)):
    """Verify Bearer token (OAuth 2.0 style)"""
    if credentials.credentials != VALID_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

def verify_basic_auth(credentials: HTTPBasic = Depends(security_basic)):
    """Verify Basic Authentication"""
    correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# ============== ENDPOINTS: DIFFERENT PARAMETER PASSING METHODS ==============

@app.get("/")
def read_root():
    """Root endpoint with API documentation"""
    return {
        "message": "FastAPI Parameter & Auth Examples",
        "endpoints": {
            "parameter_passing": [
                "GET /sum/query - Pass numbers in query parameters",
                "POST /sum/body - Pass numbers in request body",
                "GET /sum/header - Pass numbers in headers"
            ],
            "authentication": [
                "GET /auth/api-key-header - API key in header (X-API-Key)",
                "GET /auth/api-key-query - API key in query parameter",
                "GET /auth/bearer - Bearer token authentication",
                "GET /auth/basic - Basic authentication (username:password)"
            ]
        },
        "credentials": {
            "api_key": "my-secret-api-key-123",
            "bearer_token": "valid-bearer-token-xyz",
            "username": "admin",
            "password": "secret123"
        }
    }


# 1. QUERY PARAMETERS
@app.get("/sum/query", response_model=SumResponse)
def sum_query_params(
    num1: float = Query(..., description="First number"),
    num2: float = Query(..., description="Second number")
):
    """
    Sum two numbers passed as query parameters.
    
    Example: /sum/query?num1=5&num2=10
    """
    return SumResponse(result=num1 + num2, method="query_parameters")

# class SumResponse(BaseModel):
#     result: float
#     method: str
# 2. REQUEST BODY
@app.post("/sum/body", response_model=SumResponse)
def sum_body_params(request: SumRequest = Body(...)):
    """
    Sum two numbers passed in request body.
    
    Example body: {"num1": 5, "num2": 10}
    """
    return SumResponse(result=request.num1 + request.num2, method="request_body")


# 3. HEADER PARAMETERS
@app.get("/sum/header", response_model=SumResponse)
def sum_header_params(
    x_num1: float = Header(..., description="First number in header"),
    x_num2: float = Header(..., description="Second number in header")
):
    """
    Sum two numbers passed in headers.
    
    Headers: X-Num1: 5, X-Num2: 10
    """
    return SumResponse(result=x_num1 + x_num2, method="header_parameters")


# ============== ENDPOINTS: AUTHENTICATION METHODS ==============

# 1. API KEY IN HEADER
@app.get("/auth/api-key-header")
def api_key_header_auth(
    num1: float = Query(...),
    num2: float = Query(...),
    api_key: str = Depends(verify_api_key_header)
):
    """
    Protected endpoint using API key in header.
    
    Header: X-API-Key: my-secret-api-key-123
    Query: ?num1=5&num2=10
    """
    return {
        "result": num1 + num2,
        "auth_method": "api_key_header",
        "authenticated": True
    }


# 2. API KEY IN QUERY
@app.get("/auth/api-key-query")
def api_key_query_auth(
    num1: float = Query(...),
    num2: float = Query(...),
    api_key: str = Depends(verify_api_key_query)
):
    """
    Protected endpoint using API key in query parameter.
    
    Example: /auth/api-key-query?num1=5&num2=10&api_key=my-secret-api-key-123
    """
    return {
        "result": num1 + num2,
        "auth_method": "api_key_query",
        "authenticated": True
    }


# 3. BEARER TOKEN (OAuth 2.0)
@app.post("/auth/bearer")
def bearer_token_auth(
    request: SumRequest,
    token: str = Depends(verify_bearer_token)
):
    """
    Protected endpoint using Bearer token.
    
    Header: Authorization: Bearer valid-bearer-token-xyz
    Body: {"num1": 5, "num2": 10}
    """
    return {
        "result": request.num1 + request.num2,
        "auth_method": "bearer_token",
        "authenticated": True
    }


# 4. BASIC AUTHENTICATION
@app.post("/auth/basic")
def basic_auth(
    request: SumRequest,
    username: str = Depends(verify_basic_auth)
):
    """
    Protected endpoint using Basic Authentication.
    
    Header: Authorization: Basic base64(username:password)
    Credentials: admin:secret123
    Body: {"num1": 5, "num2": 10}
    """
    return {
        "result": request.num1 + request.num2,
        "auth_method": "basic_auth",
        "username": username,
        "authenticated": True
    }


# ============== COMBINED EXAMPLE ==============

@app.post("/combined/all-methods")
def combined_example(
    # Body
    request: SumRequest,
    # Query
    multiplier: float = Query(1.0, description="Multiply result by this"),
    # Header
    x_operation: str = Header("sum", description="Operation type"),
    # Auth (choose one)
    api_key: str = Depends(verify_api_key_header)
):
    """
    Combined example using body, query, header, and authentication.
    
    - Body: {"num1": 5, "num2": 10}
    - Query: ?multiplier=2
    - Header: X-Operation: sum, X-API-Key: my-secret-api-key-123
    """
    result = request.num1 + request.num2
    result *= multiplier
    
    return {
        "result": result,
        "operation": x_operation,
        "multiplier": multiplier,
        "authenticated": True
    }

