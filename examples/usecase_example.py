#!/usr/bin/env python3
"""
Example: Usecase/Service direct config imports.

This demonstrates how usecases and services can directly import
configuration without needing to receive it as parameters.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Direct imports from config module - this is the key pattern!
from config import database_config, redis_config, auth_config, logging_config


class UserRepository:
    """Example usecase that needs database configuration."""

    def __init__(self):
        # Direct import - guaranteed to work if startup validation passed
        db_config = database_config()
        self.db_url = db_config.database_url
        self.pool_size = db_config.database_pool_size
        self.timeout = db_config.database_timeout

    def get_user(self, user_id: str):
        print(f"🔍 Connecting to database: {self.db_url}")
        print(f"🏊 Using pool size: {self.pool_size}")
        print(f"⏱️  Timeout: {self.timeout}s")
        return f"User {user_id} from database"


class CacheService:
    """Example service that needs redis configuration."""

    def __init__(self):
        redis_cfg = redis_config()
        self.redis_url = redis_cfg.redis_url
        self.ttl = redis_cfg.redis_ttl

    def get_cached_data(self, key: str):
        print(f"📦 Connecting to Redis: {self.redis_url}")
        print(f"⏰ Default TTL: {self.ttl}s")
        return f"Cached data for {key}"


class AuthService:
    """Example service that needs auth configuration."""

    def __init__(self):
        auth_cfg = auth_config()
        self.jwt_secret = auth_cfg.jwt_secret
        self.jwt_expiry = auth_cfg.jwt_expiry

    def create_token(self, user_id: str):
        print(f"🔐 Creating JWT token (expiry: {self.jwt_expiry}s)")
        # In real code, you'd use the jwt_secret here
        return f"jwt-token-for-{user_id}"


class LoggerService:
    """Example service that needs logging configuration."""

    def __init__(self):
        log_cfg = logging_config()
        self.log_level = log_cfg.log_level
        self.log_format = log_cfg.log_format

    def log_message(self, message: str):
        print(f"📝 [{self.log_level}] ({self.log_format}) {message}")


def main():
    """
    Demonstrate direct config imports in usecases/services.

    Note: In a real application, startup validation should be called first!
    """
    print("=== Usecase/Service Configuration Demo ===")
    print()

    try:
        # Create services - they'll directly import their needed configs
        print("🏗️  Creating UserRepository...")
        user_repo = UserRepository()
        user = user_repo.get_user("123")
        print(f"Result: {user}")
        print()

        print("🏗️  Creating CacheService...")
        cache = CacheService()
        cached_data = cache.get_cached_data("user:123")
        print(f"Result: {cached_data}")
        print()

        print("🏗️  Creating AuthService...")
        auth = AuthService()
        token = auth.create_token("123")
        print(f"Result: {token}")
        print()

        print("🏗️  Creating LoggerService...")
        logger = LoggerService()
        logger.log_message("Service initialized successfully")
        print()

        print("✅ All services created and configured successfully!")
        print("🎯 Key insight: Each service imported only the config it needed")

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Hint: Make sure to set environment variables or call validate_app_config() first")
        sys.exit(1)


if __name__ == "__main__":
    main()