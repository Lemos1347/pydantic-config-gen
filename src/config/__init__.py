"""
Configuration module for multi-application environment variable management.

This module provides:
- Subject-specific configuration access (database_config, redis_config, etc.)
- Application startup validation
- Type-safe configuration management using Pydantic

Usage:
    # At application startup
    from config import validate_app_config
    validate_app_config("user-service")  # Fails fast if env vars missing

    # In usecases/services
    from config import database_config, redis_config

    class UserRepository:
        def __init__(self):
            db_config = database_config()
            self.db_url = db_config.database_url
"""

try:
    from .generated import (
        # Subject-specific configuration functions
        database_config,
        redis_config,
        auth_config,
        logging_config,
        http_config,
        messaging_config,
        telemetry_config,
        features_config,

        # Application validation
        validate_app_config,

        # Application-specific configuration classes
        get_user_service_config,
        get_order_service_config,
        get_notification_service_config,
        get_api_gateway_config,

        # Utility
        AVAILABLE_APPLICATIONS,
        _reset_cache,
    )
except ImportError:
    # Graceful fallback if generated module doesn't exist yet
    def _not_generated(*args, **kwargs):
        raise RuntimeError(
            "Configuration module not generated yet. "
            "Run 'uv run generate-configs' to generate configuration classes."
        )

    database_config = _not_generated
    redis_config = _not_generated
    auth_config = _not_generated
    logging_config = _not_generated
    http_config = _not_generated
    messaging_config = _not_generated
    telemetry_config = _not_generated
    features_config = _not_generated
    validate_app_config = _not_generated
    get_user_service_config = _not_generated
    get_order_service_config = _not_generated
    get_notification_service_config = _not_generated
    get_api_gateway_config = _not_generated
    AVAILABLE_APPLICATIONS = []
    _reset_cache = _not_generated


__all__ = [
    # Subject-specific configurations
    "database_config",
    "redis_config",
    "auth_config",
    "logging_config",
    "http_config",
    "messaging_config",
    "telemetry_config",
    "features_config",

    # Application validation
    "validate_app_config",

    # Application-specific configurations
    "get_user_service_config",
    "get_order_service_config",
    "get_notification_service_config",
    "get_api_gateway_config",

    # Utility
    "AVAILABLE_APPLICATIONS",
]