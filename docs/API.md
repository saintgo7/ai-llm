# API Documentation

## REST API Server (Port 5000)

### Endpoints

#### 1. Get All Tasks
**GET** `/api/tasks`

Get all tasks with optional filtering.

**Query Parameters:**
- `status` (optional): Filter by status (`completed` or `pending`)

**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Example Task",
      "description": "Task description",
      "completed": false,
      "created_at": "2025-11-17T10:00:00",
      "updated_at": "2025-11-17T10:00:00"
    }
  ],
  "count": 1,
  "total": 1
}
```

**Example:**
```bash
curl http://localhost:5000/api/tasks
curl http://localhost:5000/api/tasks?status=completed
```

---

#### 2. Get Task by ID
**GET** `/api/tasks/{id}`

Get a specific task by ID.

**Path Parameters:**
- `id` (integer): Task ID

**Response:**
```json
{
  "id": 1,
  "title": "Example Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2025-11-17T10:00:00",
  "updated_at": "2025-11-17T10:00:00"
}
```

**Example:**
```bash
curl http://localhost:5000/api/tasks/1
```

---

#### 3. Create Task
**POST** `/api/tasks`

Create a new task.

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "completed": false
}
```

**Validation:**
- `title`: Required, max 200 characters
- `description`: Optional, max 1000 characters
- `completed`: Optional, boolean

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2025-11-17T10:00:00",
  "updated_at": "2025-11-17T10:00:00"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"My Task","description":"Do something"}'
```

---

#### 4. Update Task
**PUT** `/api/tasks/{id}`

Update an existing task.

**Path Parameters:**
- `id` (integer): Task ID

**Request Body:**
```json
{
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true,
  "created_at": "2025-11-17T10:00:00",
  "updated_at": "2025-11-17T10:30:00"
}
```

**Example:**
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

---

#### 5. Delete Task
**DELETE** `/api/tasks/{id}`

Delete a task.

**Path Parameters:**
- `id` (integer): Task ID

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```

---

#### 6. Health Check
**GET** `/api/health`

Check API server health.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-17T10:00:00",
  "tasks_count": 5
}
```

**Example:**
```bash
curl http://localhost:5000/api/health
```

---

## JWT Authentication API (Port 5001)

### Endpoints

#### 1. Login
**POST** `/api/login`

Authenticate and get JWT token.

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "username": "admin",
  "role": "admin",
  "email": "admin@example.com"
}
```

**Test Credentials:**
- Username: `admin`, Password: `admin123` (Role: admin)
- Username: `user`, Password: `user123` (Role: user)

**Example:**
```bash
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

#### 2. Protected Route
**GET** `/api/protected`

Access protected resource (requires authentication).

**Headers:**
- `Authorization`: Bearer {token}

**Response:**
```json
{
  "message": "This is a protected route",
  "user": "admin",
  "role": "admin",
  "timestamp": "2025-11-17T10:00:00"
}
```

**Example:**
```bash
TOKEN="your-jwt-token-here"
curl http://localhost:5001/api/protected \
  -H "Authorization: Bearer $TOKEN"
```

---

#### 3. Admin Route
**GET** `/api/admin`

Access admin-only resource (requires admin role).

**Headers:**
- `Authorization`: Bearer {token}

**Response:**
```json
{
  "message": "This is an admin-only route",
  "user": "admin",
  "role": "admin",
  "users_count": 2
}
```

**Example:**
```bash
TOKEN="your-admin-jwt-token"
curl http://localhost:5001/api/admin \
  -H "Authorization: Bearer $TOKEN"
```

---

#### 4. Verify Token
**GET** `/api/verify`

Verify JWT token validity.

**Headers:**
- `Authorization`: Bearer {token}

**Response:**
```json
{
  "valid": true,
  "user": "admin",
  "role": "admin",
  "expires_at": "2025-11-18T10:00:00"
}
```

**Example:**
```bash
TOKEN="your-jwt-token-here"
curl http://localhost:5001/api/verify \
  -H "Authorization: Bearer $TOKEN"
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Title is required and cannot be empty"
}
```

### 401 Unauthorized
```json
{
  "message": "Token is missing"
}
```

### 403 Forbidden
```json
{
  "message": "Admin access required"
}
```

### 404 Not Found
```json
{
  "error": "Task not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Complete Workflow Example

### 1. Start Servers with Docker
```bash
docker-compose up -d
```

### 2. Login and Get Token
```bash
TOKEN=$(curl -s -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.token')

echo "Token: $TOKEN"
```

### 3. Create a Task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete API documentation",
    "description": "Write comprehensive API docs",
    "completed": false
  }'
```

### 4. Get All Tasks
```bash
curl http://localhost:5000/api/tasks | jq
```

### 5. Access Protected Route
```bash
curl http://localhost:5001/api/protected \
  -H "Authorization: Bearer $TOKEN" | jq
```

### 6. Update Task
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 7. Health Check
```bash
curl http://localhost:5000/api/health | jq
```

---

## Rate Limiting

Rate limiting is configured via environment variables:
- `ENABLE_RATE_LIMITING`: Enable/disable rate limiting
- `MAX_REQUESTS_PER_MINUTE`: Maximum requests per minute per IP

---

## Security

### Password Hashing
All passwords are hashed using SHA-256 before storage.

### JWT Tokens
- Tokens expire after 24 hours (configurable)
- Use HS256 algorithm for signing
- Include user role for authorization

### Input Validation
- All inputs are validated and sanitized
- SQL injection protection with parameterized queries
- XSS prevention with proper escaping

---

## Logging

All API requests are logged with the following information:
- Timestamp
- HTTP method and endpoint
- Request status
- User information (if authenticated)
- Error details (if any)

Log level can be configured via `LOG_LEVEL` environment variable.
