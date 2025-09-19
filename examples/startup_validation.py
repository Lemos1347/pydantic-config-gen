#!/usr/bin/env python3
"""
Example: Application startup with configuration validation.

This demonstrates how to validate all required environment variables
at application startup, ensuring fail-fast behavior.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import validate_app_config, AVAILABLE_APPLICATIONS


def start_user_service():
    """Example startup for user-service application."""
    print("🚀 Starting user-service...")

    try:
        # Validate all required configs at startup
        # This will fail fast if any environment variables are missing
        validate_app_config("user-service")
        print("✅ All configuration validated successfully!")

        # Your application startup code would go here
        print("🎯 User service started successfully")

    except Exception as e:
        print(f"❌ Failed to start user-service: {e}")
        sys.exit(1)


def start_api_gateway():
    """Example startup for api-gateway application."""
    print("🚀 Starting api-gateway...")

    try:
        validate_app_config("api-gateway")
        print("✅ All configuration validated successfully!")
        print("🎯 API Gateway started successfully")

    except Exception as e:
        print(f"❌ Failed to start api-gateway: {e}")
        sys.exit(1)


def main():
    """Main entry point to demonstrate different application startups."""
    print("=== Configuration System Demo ===")
    print(f"Available applications: {AVAILABLE_APPLICATIONS}")
    print()

    if len(sys.argv) < 2:
        print("Usage: python startup_validation.py <app-name>")
        print(f"Available apps: {', '.join(AVAILABLE_APPLICATIONS)}")
        sys.exit(1)

    app_name = sys.argv[1]

    if app_name == "user-service":
        start_user_service()
    elif app_name == "api-gateway":
        start_api_gateway()
    elif app_name in AVAILABLE_APPLICATIONS:
        print(f"🚀 Starting {app_name}...")
        try:
            validate_app_config(app_name)
            print("✅ All configuration validated successfully!")
            print(f"🎯 {app_name} started successfully")
        except Exception as e:
            print(f"❌ Failed to start {app_name}: {e}")
            sys.exit(1)
    else:
        print(f"❌ Unknown application: {app_name}")
        print(f"Available apps: {', '.join(AVAILABLE_APPLICATIONS)}")
        sys.exit(1)


if __name__ == "__main__":
    main()