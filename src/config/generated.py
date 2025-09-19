"""
Generated configuration module.
This file is auto-generated from config.toml - DO NOT EDIT MANUALLY.

To regenerate: uv run generate-configs
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, ValidationInfo


# Subject-specific configuration classes
class DatabaseConfig(BaseSettings):
    """Configuration for database related settings."""
    database_url: str  # Main database connection URL
    database_pool_size: int = 10  # Database connection pool size
    database_timeout: int = 30  # Database connection timeout in seconds

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore"
    )


class RedisConfig(BaseSettings):
    """Configuration for redis related settings."""
    redis_url: str  # Redis connection URL for caching
    redis_ttl: int = 3600  # Default TTL for Redis cache entries in seconds

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore"
    )


class AuthConfig(BaseSettings):
    """Configuration for auth related settings."""
    jwt_secret: str  # Secret key for JWT token signing
    jwt_expiry: int = 86400  # JWT token expiry time in seconds

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore"
    )


class LoggingConfig(BaseSettings):
    """Configuration for logging related settings."""
    log_level: str = "INFO"  # Application log level
    log_format: str = "json"  # Log format (json or text)

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore"
    )


class HttpConfig(BaseSettings):
    """Configuration for http related settings."""
    api_host: str = "0.0.0.0"  # HTTP server host
    api_port: int = 8000  # HTTP server port

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore"
    )


class MessagingConfig(BaseSettings):
    """Configuration for messaging related settings."""
    queue_url: str  # Message queue connection URL
    queue_timeout: int = 60  # Message queue timeout in seconds

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore"
    )


class TelemetryConfig(BaseSettings):
    """Configuration for telemetry related settings."""
    use_otl: bool = False  # Enable OpenTelemetry tracing
    otl_endpoint: Optional[str] = None  # OpenTelemetry endpoint URL
    otl_service_name: Optional[str] = None  # Service name for OpenTelemetry (optional)
    trace_sample_rate: Optional[float] = None  # Trace sampling rate between 0.0 and 1.0

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore"
    )

    # Conditional field validators
    @field_validator('otl_endpoint')
    @classmethod
    def validate_otl_endpoint(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validate otl_endpoint based on conditional requirements."""
        condition_met = str(info.data.get('use_otl', '')).lower() == 'true'

        if condition_met and v is None:
            raise ValueError('OTL_ENDPOINT is required when USE_OTL=true')

        return v


class FeaturesConfig(BaseSettings):
    """Configuration for features related settings."""
    enable_rate_limiting: bool = False  # Enable API rate limiting
    rate_limit_per_minute: Optional[int] = None  # Rate limit requests per minute
    rate_limit_redis_url: Optional[str] = None  # Redis URL for rate limiting (uses main Redis if not specified)

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore"
    )

    # Conditional field validators
    @field_validator('rate_limit_per_minute')
    @classmethod
    def validate_rate_limit_per_minute(cls, v: Optional[int], info: ValidationInfo) -> Optional[int]:
        """Validate rate_limit_per_minute based on conditional requirements."""
        condition_met = str(info.data.get('enable_rate_limiting', '')).lower() == 'true'

        if condition_met and v is None:
            raise ValueError('RATE_LIMIT_PER_MINUTE is required when ENABLE_RATE_LIMITING=true')

        return v



# Module-level cached instances
_database_config: Optional[DatabaseConfig] = None
_redis_config: Optional[RedisConfig] = None
_auth_config: Optional[AuthConfig] = None
_logging_config: Optional[LoggingConfig] = None
_http_config: Optional[HttpConfig] = None
_messaging_config: Optional[MessagingConfig] = None
_telemetry_config: Optional[TelemetryConfig] = None
_features_config: Optional[FeaturesConfig] = None

# Module-level getter functions for direct import
def database_config() -> DatabaseConfig:
    """Get database configuration. Lazy-loaded and cached."""
    global _database_config
    if _database_config is None:
        _database_config = DatabaseConfig()
    return _database_config

def redis_config() -> RedisConfig:
    """Get redis configuration. Lazy-loaded and cached."""
    global _redis_config
    if _redis_config is None:
        _redis_config = RedisConfig()
    return _redis_config

def auth_config() -> AuthConfig:
    """Get auth configuration. Lazy-loaded and cached."""
    global _auth_config
    if _auth_config is None:
        _auth_config = AuthConfig()
    return _auth_config

def logging_config() -> LoggingConfig:
    """Get logging configuration. Lazy-loaded and cached."""
    global _logging_config
    if _logging_config is None:
        _logging_config = LoggingConfig()
    return _logging_config

def http_config() -> HttpConfig:
    """Get http configuration. Lazy-loaded and cached."""
    global _http_config
    if _http_config is None:
        _http_config = HttpConfig()
    return _http_config

def messaging_config() -> MessagingConfig:
    """Get messaging configuration. Lazy-loaded and cached."""
    global _messaging_config
    if _messaging_config is None:
        _messaging_config = MessagingConfig()
    return _messaging_config

def telemetry_config() -> TelemetryConfig:
    """Get telemetry configuration. Lazy-loaded and cached."""
    global _telemetry_config
    if _telemetry_config is None:
        _telemetry_config = TelemetryConfig()
    return _telemetry_config

def features_config() -> FeaturesConfig:
    """Get features configuration. Lazy-loaded and cached."""
    global _features_config
    if _features_config is None:
        _features_config = FeaturesConfig()
    return _features_config


# Application validation function
def validate_app_config(app_name: str) -> None:
    """
    Validate that all configuration needed by an application is available.

    This should be called at application startup to fail fast if any
    required environment variables are missing.

    Args:
        app_name: Name of the application to validate

    Raises:
        ValidationError: If any required configuration is missing or invalid
    """
    if app_name == "user-service":
        # Force loading of all configs needed by user-service
        _ = auth_config()
        _ = database_config()
        _ = http_config()
        _ = logging_config()
        _ = redis_config()
        _ = telemetry_config()
        return
    if app_name == "api-gateway":
        # Force loading of all configs needed by api-gateway
        _ = auth_config()
        _ = features_config()
        _ = http_config()
        _ = logging_config()
        _ = telemetry_config()
        return
    if app_name == "order-service":
        # Force loading of all configs needed by order-service
        _ = database_config()
        _ = logging_config()
        _ = messaging_config()
        return
    if app_name == "notification-service":
        # Force loading of all configs needed by notification-service
        _ = database_config()
        _ = logging_config()
        _ = messaging_config()
        _ = redis_config()
        return

    raise ValueError(f"Unknown application: {app_name}")


# Available applications
AVAILABLE_APPLICATIONS = [
    "user-service",
    "api-gateway",
    "order-service",
    "notification-service",
]


# Reset function for testing
def _reset_cache() -> None:
    """Reset all cached configurations. Used for testing."""
    global _database_config
    _database_config = None
    global _redis_config
    _redis_config = None
    global _auth_config
    _auth_config = None
    global _logging_config
    _logging_config = None
    global _http_config
    _http_config = None
    global _messaging_config
    _messaging_config = None
    global _telemetry_config
    _telemetry_config = None
    global _features_config
    _features_config = None


# Application-specific configuration classes
class UserServiceConfig:
    """Configuration container for user-service application."""

    def __init__(self):
        # Load all required configs for this application
        self.auth = auth_config()
        self.database = database_config()
        self.http = http_config()
        self.logging = logging_config()
        self.redis = redis_config()
        self.telemetry = telemetry_config()

    @property
    def auth_config(self) -> AuthConfig:
        """Get auth configuration."""
        return self.auth
    @property
    def database_config(self) -> DatabaseConfig:
        """Get database configuration."""
        return self.database
    @property
    def http_config(self) -> HttpConfig:
        """Get http configuration."""
        return self.http
    @property
    def logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return self.logging
    @property
    def redis_config(self) -> RedisConfig:
        """Get redis configuration."""
        return self.redis
    @property
    def telemetry_config(self) -> TelemetryConfig:
        """Get telemetry configuration."""
        return self.telemetry


def get_user_service_config() -> UserServiceConfig:
    """Get complete configuration for user-service application."""
    return UserServiceConfig()

class ApiGatewayConfig:
    """Configuration container for api-gateway application."""

    def __init__(self):
        # Load all required configs for this application
        self.auth = auth_config()
        self.features = features_config()
        self.http = http_config()
        self.logging = logging_config()
        self.telemetry = telemetry_config()

    @property
    def auth_config(self) -> AuthConfig:
        """Get auth configuration."""
        return self.auth
    @property
    def features_config(self) -> FeaturesConfig:
        """Get features configuration."""
        return self.features
    @property
    def http_config(self) -> HttpConfig:
        """Get http configuration."""
        return self.http
    @property
    def logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return self.logging
    @property
    def telemetry_config(self) -> TelemetryConfig:
        """Get telemetry configuration."""
        return self.telemetry


def get_api_gateway_config() -> ApiGatewayConfig:
    """Get complete configuration for api-gateway application."""
    return ApiGatewayConfig()

class OrderServiceConfig:
    """Configuration container for order-service application."""

    def __init__(self):
        # Load all required configs for this application
        self.database = database_config()
        self.logging = logging_config()
        self.messaging = messaging_config()

    @property
    def database_config(self) -> DatabaseConfig:
        """Get database configuration."""
        return self.database
    @property
    def logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return self.logging
    @property
    def messaging_config(self) -> MessagingConfig:
        """Get messaging configuration."""
        return self.messaging


def get_order_service_config() -> OrderServiceConfig:
    """Get complete configuration for order-service application."""
    return OrderServiceConfig()

class NotificationServiceConfig:
    """Configuration container for notification-service application."""

    def __init__(self):
        # Load all required configs for this application
        self.database = database_config()
        self.logging = logging_config()
        self.messaging = messaging_config()
        self.redis = redis_config()

    @property
    def database_config(self) -> DatabaseConfig:
        """Get database configuration."""
        return self.database
    @property
    def logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return self.logging
    @property
    def messaging_config(self) -> MessagingConfig:
        """Get messaging configuration."""
        return self.messaging
    @property
    def redis_config(self) -> RedisConfig:
        """Get redis configuration."""
        return self.redis


def get_notification_service_config() -> NotificationServiceConfig:
    """Get complete configuration for notification-service application."""
    return NotificationServiceConfig()

