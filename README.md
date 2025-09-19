# Python Configuration System

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg?1ogo=python&logoColor=white)](https://www.python.org/downloads/release/python-3120/)
[![uv - package manager](https://img.shields.io/badge/uv-%F0%9F%93%A6%20package--manager-6e40c9?1ogo=astral&logoColor=white)](https://github.com/astral-sh/uv)

A Python configuration management system inspired by Cartesi's TOML-based approach. This system generates type-safe Pydantic configuration classes from a single TOML definition file, organized by logical domains (subjects) rather than individual services.

## Key Features

- **Single Source of Truth**: All configuration defined in one `config.toml` file
- **Subject-Based Organization**: Configuration grouped by logical domains (database, redis, auth, etc.)
- **Application Scoping**: Each application only sees the configuration subjects it needs
- **Direct Imports**: Services can directly import configuration without dependency injection
- **Fail-Fast Validation**: Application startup validation ensures all required environment variables are present
- **Type Safety**: Generated Pydantic models provide runtime validation and type hints
- **Optional & Conditional Variables**: Support for optional and conditionally required environment variables
- **No Service Explosion**: Avoids creating configuration classes for every individual service

## Quick Start

### 1. Install Dependencies

```bash
uv sync --frozen
```

### 2. Define Configuration

Create a `config.toml` file:

```toml
[database.DATABASE_URL]
type = "str"
description = "Main database connection URL"
applications = ["user-service", "order-service"]

[redis.REDIS_URL]
type = "str"
description = "Redis connection URL for caching"
applications = ["user-service", "notification-service"]

[auth.JWT_SECRET]
type = "str"
description = "Secret key for JWT token signing"
applications = ["user-service", "api-gateway"]

# Optional and conditional variables
[telemetry.USE_OTL]
type = "bool"
default = "false"
description = "Enable OpenTelemetry tracing"
applications = ["user-service", "api-gateway"]

[telemetry.OTL_ENDPOINT]
type = "str"
description = "OpenTelemetry endpoint URL"
required_when = "USE_OTL=true"  # Only required when USE_OTL is enabled
applications = ["user-service", "api-gateway"]

[telemetry.OTL_SERVICE_NAME]
type = "Optional[str]"  # Explicitly optional
description = "Service name for OpenTelemetry"
applications = ["user-service", "api-gateway"]
```

### 3. Generate Configuration Classes

```bash
uv run generate-configs
```

### 4. Use in Your Application

**Startup validation (fail-fast):**

```python
from config import validate_app_config

def main():
    # Validate all required env vars at startup
    validate_app_config("user-service")

    # Start your application...
```

**Direct imports in services:**

```python
from config import database_config, redis_config

class UserRepository:
    def __init__(self):
        db_config = database_config()
        self.db_url = db_config.database_url

class CacheService:
    def __init__(self):
        redis_cfg = redis_config()
        self.redis_url = redis_cfg.redis_url
```

## Architecture

### Configuration Definition (`config.toml`)

The TOML file organizes configuration by subjects (logical domains):

```toml
[database.DATABASE_URL]           # Subject: database, Variable: DATABASE_URL
type = "str"                      # Python type
description = "..."               # Documentation
applications = ["app1", "app2"]   # Which apps need this

[database.DATABASE_POOL_SIZE]
type = "int"
default = "10"                    # Optional default value
applications = ["app1", "app2"]

[redis.REDIS_URL]                 # Subject: redis
type = "str"
applications = ["app1", "app3"]
```

### Generated Code Structure

The generator creates:

1. **Subject Configuration Classes** (e.g., `DatabaseConfig`, `RedisConfig`)
2. **Module-level getter functions** (e.g., `database_config()`, `redis_config()`)
3. **Application validation function** (`validate_app_config(app_name)`)
4. **Application-specific configuration classes** (e.g., `UserServiceConfig`)

### Usage Patterns

#### Pattern 1: Direct Subject Import (Recommended)

```python
from config import database_config, redis_config

class MyService:
    def __init__(self):
        # Each service imports only what it needs
        db = database_config()
        redis = redis_config()
```

#### Pattern 2: Application Configuration

```python
from config import get_user_service_config

class MyApplication:
    def __init__(self):
        # Get all configs for this application
        config = get_user_service_config()
        db_url = config.database.database_url
        redis_url = config.redis.redis_url
```

#### Pattern 3: Startup Validation

```python
from config import validate_app_config

def main():
    # Validate at startup - fails fast if env vars missing
    validate_app_config("user-service")

    # Now all subsequent config access is guaranteed to work
    start_services()
```

## Configuration Subjects

The system organizes configuration into logical subjects:

- **`database`**: Database connection settings
- **`redis`**: Cache configuration
- **`auth`**: Authentication/authorization settings
- **`logging`**: Application logging configuration
- **`http`**: HTTP server settings
- **`messaging`**: Message queue configuration

Each subject becomes a separate Pydantic configuration class.

## Optional and Conditional Variables

The system supports two types of flexible configuration:

### 1. Optional Variables

Variables that can be `None` or missing entirely:

```toml
[telemetry.OTL_SERVICE_NAME]
type = "Optional[str]"  # Can be None
description = "Service name for OpenTelemetry"
applications = ["user-service"]
```

Generated code:

```python
class TelemetryConfig(BaseSettings):
    otl_service_name: Optional[str] = None
```

### 2. Conditional Variables

Variables that are only required when certain conditions are met:

```toml
[telemetry.USE_OTL]
type = "bool"
default = "false"
description = "Enable OpenTelemetry"
applications = ["user-service"]

[telemetry.OTL_ENDPOINT]
type = "str"
description = "OpenTelemetry endpoint URL"
required_when = "USE_OTL=true"  # Only required when USE_OTL is true
applications = ["user-service"]
```

Generated code:

```python
class TelemetryConfig(BaseSettings):
    use_otl: bool = False
    otl_endpoint: Optional[str] = None  # Optional by default

    @field_validator('otl_endpoint')
    @classmethod
    def validate_otl_endpoint(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        if info.data.get('use_otl', False) and v is None:
            raise ValueError('OTL_ENDPOINT is required when USE_OTL=true')
        return v
```

### Usage Pattern

```python
from config import telemetry_config

def setup_telemetry():
    config = telemetry_config()

    if config.use_otl:
        # otl_endpoint is guaranteed to be present when use_otl is True
        setup_opentelemetry(config.otl_endpoint)

        # Optional variables can still be None
        if config.otl_service_name:
            set_service_name(config.otl_service_name)
```

## Examples

Run the provided examples to see the system in action:

```bash
# Set some environment variables
export DATABASE_URL=postgresql://localhost/test
export REDIS_URL=redis://localhost
export JWT_SECRET=test-secret
export QUEUE_URL=amqp://localhost

# Test direct imports in services
PYTHONPATH=src uv run python examples/usecase_example.py

# Test startup validation
PYTHONPATH=src uv run python examples/startup_validation.py user-service

# Test application configurations
PYTHONPATH=src uv run python examples/application_config_example.py

# Test optional and conditional configurations
PYTHONPATH=src uv run python examples/conditional_config_example.py

# Test conditional validation with telemetry enabled
export USE_OTL=true
export OTL_ENDPOINT=http://jaeger:14268/api/traces
PYTHONPATH=src uv run python examples/conditional_config_example.py

# Test failure case (missing required env var)
unset JWT_SECRET
PYTHONPATH=src uv run python examples/startup_validation.py api-gateway
```

## Commands

- **`uv run generate-configs`**: Generate configuration classes from `config.toml`
- **`uv run generate-configs --config custom.toml --output custom_config.py`**: Use custom files

## Benefits

1. **Maintainable**: Configuration organized by logical domains, not individual services
2. **Fail-Fast**: Missing environment variables detected at startup, not runtime
3. **Type-Safe**: Pydantic provides runtime validation and IDE support
4. **Direct Access**: Services import configuration directly without dependency injection
5. **Scoped**: Each application only sees the configuration subjects it needs
6. **Single Source**: All configuration definitions in one TOML file
7. **Generated**: Reduces boilerplate and ensures consistency

## Project Structure

```
    config.toml                    # Configuration definitions
    src/config/
        __init__.py                # Public API
        parser.py                  # TOML parser
        generator.py               # Code generator
        generated.py               # Generated config classes
        templates/
            config.py.j2           # Jinja2 template
    scripts/
        generate_configs.py        # CLI script
    examples/                      # Usage examples
```

## Comparison with Traditional Approaches

### Traditional pydantic-settings (Single Class)

```python
class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret: str
    # All services see all variables
```

### This System (Subject-Based)

```python
# Each subject is separate
class DatabaseConfig(BaseSettings):
    database_url: str

class RedisConfig(BaseSettings):
    redis_url: str

# Services import only what they need
from config import database_config  # Only database vars
```

### Benefits of Subject-Based Approach

1. **Clear Dependencies**: Easy to see which services need which configuration
2. **Reduced Coupling**: Services only depend on their required configuration subjects
3. **Better Testing**: Mock only the configuration subjects your service uses
4. **Maintainable**: Adding new configuration doesn't affect unrelated services
5. **Discoverable**: `from config import ` shows available configuration subjects

## Inspired by Cartesi

This system is inspired by [Cartesi's rollups-node configuration approach](https://github.com/cartesi/rollups-node), which uses:

- TOML-based configuration definitions with metadata
- Code generation for type-safe configuration access
- Application-specific configuration scoping
- Fail-fast validation patterns

The Python implementation adapts these concepts using Pydantic and modern Python tooling.
