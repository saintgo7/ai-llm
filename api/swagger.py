"""
OpenAPI/Swagger Documentation
"""
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'

def setup_swagger(app):
    """Flask 앱에 Swagger UI 설정"""

    # Swagger UI blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "AI-LLM API Documentation",
            'docExpansion': 'list',
            'defaultModelsExpandDepth': 3
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Swagger JSON specification
    @app.route('/api/swagger.json')
    def swagger_json():
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "AI-LLM API",
                "description": "Comprehensive API for AI-LLM programming examples",
                "version": "2.0.0",
                "contact": {
                    "name": "API Support",
                    "email": "support@ai-llm.com"
                }
            },
            "servers": [
                {"url": "http://localhost:5000", "description": "Development server"},
                {"url": "https://api.ai-llm.com", "description": "Production server"}
            ],
            "tags": [
                {"name": "tasks", "description": "Task management endpoints"},
                {"name": "auth", "description": "Authentication endpoints"},
                {"name": "health", "description": "Health check endpoints"}
            ],
            "paths": {
                "/api/v1/tasks": {
                    "get": {
                        "tags": ["tasks"],
                        "summary": "Get all tasks",
                        "description": "Retrieve list of all tasks with optional filtering",
                        "parameters": [
                            {
                                "name": "status",
                                "in": "query",
                                "schema": {"type": "string", "enum": ["completed", "pending"]},
                                "description": "Filter by task status"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "version": {"type": "string"},
                                                "tasks": {"type": "array", "items": {"$ref": "#/components/schemas/Task"}},
                                                "count": {"type": "integer"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "post": {
                        "tags": ["tasks"],
                        "summary": "Create new task",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/TaskInput"}
                                }
                            }
                        },
                        "responses": {
                            "201": {
                                "description": "Task created",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Task"}
                                    }
                                }
                            },
                            "400": {"description": "Invalid input"}
                        }
                    }
                },
                "/api/v2/tasks": {
                    "get": {
                        "tags": ["tasks"],
                        "summary": "Get all tasks (v2 with pagination)",
                        "parameters": [
                            {"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}},
                            {"name": "per_page", "in": "query", "schema": {"type": "integer", "default": 10}},
                            {"name": "status", "in": "query", "schema": {"type": "string"}},
                            {"name": "priority", "in": "query", "schema": {"type": "string"}},
                            {"name": "tag", "in": "query", "schema": {"type": "string"}}
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful response with pagination"
                            }
                        }
                    }
                },
                "/api/health": {
                    "get": {
                        "tags": ["health"],
                        "summary": "Health check",
                        "responses": {
                            "200": {
                                "description": "Service is healthy"
                            }
                        }
                    }
                },
                "/api/login": {
                    "post": {
                        "tags": ["auth"],
                        "summary": "User login",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "username": {"type": "string"},
                                            "password": {"type": "string"}
                                        },
                                        "required": ["username", "password"]
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Login successful",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "token": {"type": "string"},
                                                "username": {"type": "string"},
                                                "role": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            },
                            "401": {"description": "Invalid credentials"}
                        }
                    }
                }
            },
            "components": {
                "schemas": {
                    "Task": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "completed": {"type": "boolean"},
                            "created_at": {"type": "string", "format": "date-time"}
                        }
                    },
                    "TaskInput": {
                        "type": "object",
                        "required": ["title"],
                        "properties": {
                            "title": {"type": "string", "maxLength": 200},
                            "description": {"type": "string", "maxLength": 1000},
                            "completed": {"type": "boolean", "default": False}
                        }
                    },
                    "TaskV2": {
                        "allOf": [
                            {"$ref": "#/components/schemas/Task"},
                            {
                                "type": "object",
                                "properties": {
                                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"]},
                                    "tags": {"type": "array", "items": {"type": "string"}},
                                    "due_date": {"type": "string", "format": "date"},
                                    "assignee": {"type": "string"}
                                }
                            }
                        ]
                    }
                },
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }

    return app
