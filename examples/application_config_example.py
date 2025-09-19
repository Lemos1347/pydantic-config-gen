#!/usr/bin/env python3
"""
Example: Application-specific configuration classes.

This demonstrates using the generated application config classes
for cases where you want all configs for an app in one object.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import (
    get_user_service_config,
    get_api_gateway_config,
    get_order_service_config,
    get_notification_service_config
)


def demo_user_service_config():
    """Demo the user-service application configuration."""
    print("🔧 User Service Configuration:")

    try:
        config = get_user_service_config()

        # Access different subject configs
        print(f"  📊 Database URL: {config.database.database_url}")
        print(f"  🏊 Pool Size: {config.database.database_pool_size}")
        print(f"  📦 Redis URL: {config.redis.redis_url}")
        print(f"  🔐 JWT Expiry: {config.auth.jwt_expiry}s")
        print(f"  📝 Log Level: {config.logging.log_level}")
        print(f"  🌐 API Host: {config.http.api_host}:{config.http.api_port}")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    print()


def demo_api_gateway_config():
    """Demo the api-gateway application configuration."""
    print("🔧 API Gateway Configuration:")

    try:
        config = get_api_gateway_config()

        # API Gateway only needs auth, http, and logging
        print(f"  🔐 JWT Secret: {'***' if config.auth.jwt_secret else 'NOT SET'}")
        print(f"  🌐 API Host: {config.http.api_host}:{config.http.api_port}")
        print(f"  📝 Log Format: {config.logging.log_format}")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    print()


def demo_order_service_config():
    """Demo the order-service application configuration."""
    print("🔧 Order Service Configuration:")

    try:
        config = get_order_service_config()

        # Order service needs database, logging, and messaging
        print(f"  📊 Database URL: {config.database.database_url}")
        print(f"  📝 Log Level: {config.logging.log_level}")
        print(f"  📬 Queue URL: {config.messaging.queue_url}")
        print(f"  ⏱️  Queue Timeout: {config.messaging.queue_timeout}s")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    print()


def demo_notification_service_config():
    """Demo the notification-service application configuration."""
    print("🔧 Notification Service Configuration:")

    try:
        config = get_notification_service_config()

        # Notification service needs database, logging, messaging, and redis
        print(f"  📊 Database URL: {config.database.database_url}")
        print(f"  📦 Redis TTL: {config.redis.redis_ttl}s")
        print(f"  📬 Queue URL: {config.messaging.queue_url}")
        print(f"  📝 Log Format: {config.logging.log_format}")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    print()


def main():
    """Demonstrate application-specific configuration classes."""
    print("=== Application Configuration Demo ===")
    print("Each application gets only the configuration subjects it needs:")
    print()

    demo_user_service_config()
    demo_api_gateway_config()
    demo_order_service_config()
    demo_notification_service_config()

    print("✅ Demo complete!")
    print("🎯 Key insights:")
    print("   • Each app only sees the config subjects it needs")
    print("   • Configuration is organized by logical domains (database, redis, etc.)")
    print("   • Type-safe access through Pydantic models")
    print("   • Environment variables are loaded and validated automatically")


if __name__ == "__main__":
    main()