#!/usr/bin/env python3
"""
CLI script to generate configuration code from TOML file.

Usage:
    uv run generate-configs
    uv run generate-configs --config custom.toml --output src/custom_config.py
"""

import sys
import os
from pathlib import Path

# Add src to Python path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.generator import main

if __name__ == "__main__":
    main()