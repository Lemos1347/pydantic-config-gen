#!/usr/bin/env python3
"""
Example: Optional and Conditional Configuration Variables.

This demonstrates the new optional and conditional configuration features:
- Optional variables that can be None/missing
- Conditional variables that are only required when certain conditions are met
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import telemetry_config, features_config


def demo_telemetry_config():
    """Demonstrate telemetry configuration with optional and conditional variables."""
    print("🔧 Telemetry Configuration Demo:")
    print("=" * 50)

    try:
        config = telemetry_config()

        print(f"🔍 USE_OTL (feature flag): {config.use_otl}")
        print(f"📊 OTL_ENDPOINT (conditional): {config.otl_endpoint}")
        print(f"🏷️  OTL_SERVICE_NAME (optional): {config.otl_service_name}")
        print(f"📈 TRACE_SAMPLE_RATE (optional): {config.trace_sample_rate}")

        # Demonstrate conditional logic
        if config.use_otl:
            print("✅ OpenTelemetry is ENABLED")
            if config.otl_endpoint:
                print(f"   📡 Tracing to: {config.otl_endpoint}")
                if config.otl_service_name:
                    print(f"   🏷️  Service name: {config.otl_service_name}")
                if config.trace_sample_rate:
                    print(f"   📈 Sample rate: {config.trace_sample_rate}")
            else:
                print("   ❌ ERROR: OTL_ENDPOINT should be set when USE_OTL=true!")
        else:
            print("❌ OpenTelemetry is DISABLED")
            print("   💡 OTL_ENDPOINT is not required")

    except Exception as e:
        print(f"❌ Configuration error: {e}")

    print()


def demo_features_config():
    """Demonstrate features configuration with conditional requirements."""
    print("🔧 Features Configuration Demo:")
    print("=" * 50)

    try:
        config = features_config()

        print(f"🚦 ENABLE_RATE_LIMITING: {config.enable_rate_limiting}")
        print(f"⏱️  RATE_LIMIT_PER_MINUTE: {config.rate_limit_per_minute}")
        print(f"📦 RATE_LIMIT_REDIS_URL: {config.rate_limit_redis_url}")

        # Demonstrate conditional logic
        if config.enable_rate_limiting:
            print("✅ Rate limiting is ENABLED")
            if config.rate_limit_per_minute:
                print(f"   ⏱️  Limit: {config.rate_limit_per_minute} requests/minute")
            if config.rate_limit_redis_url:
                print(f"   📦 Using dedicated Redis: {config.rate_limit_redis_url}")
            else:
                print("   📦 Using main Redis instance for rate limiting")
        else:
            print("❌ Rate limiting is DISABLED")
            print("   💡 RATE_LIMIT_PER_MINUTE is not required")

    except Exception as e:
        print(f"❌ Configuration error: {e}")

    print()


def main():
    """Demonstrate optional and conditional configuration patterns."""
    print("=== Optional & Conditional Configuration Demo ===")
    print()

    print("💡 This example shows:")
    print("   • Optional variables (can be None)")
    print("   • Conditional variables (required only when conditions are met)")
    print("   • Runtime validation of conditional requirements")
    print()

    demo_telemetry_config()
    demo_features_config()

    print("✅ Demo complete!")
    print()
    print("🎯 Key insights:")
    print("   • Optional variables use Optional[T] type annotations")
    print("   • Conditional variables are validated based on other field values")
    print("   • Pydantic validators ensure conditional requirements are met")
    print("   • Configuration fails fast if conditional requirements are violated")


if __name__ == "__main__":
    main()