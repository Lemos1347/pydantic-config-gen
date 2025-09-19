"""
Configuration code generator.

Reads config.toml and generates Python configuration classes using Jinja2 templates.
"""

import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .parser import (
    parse_toml_file, get_python_type, get_class_name, get_property_name,
    snake_to_camel, parse_required_when_condition, has_conditional_variables,
    format_model_config_settings
)


def generate_config_code(config_file: str = "config.toml", output_file: str = None) -> None:
    """
    Generate configuration code from TOML file.

    Args:
        config_file: Path to the configuration TOML file
        output_file: Path to output the generated Python file
    """
    # Default output file location
    if output_file is None:
        output_file = "src/config/generated.py"

    # Parse the configuration file
    parsed_config = parse_toml_file(config_file)

    # Setup Jinja2 environment
    template_dir = Path(__file__).parent / "templates"
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Add custom functions to template environment
    env.globals.update({
        'get_python_type': get_python_type,
        'get_class_name': get_class_name,
        'get_property_name': get_property_name,
        'snake_to_camel': snake_to_camel,
        'parse_required_when_condition': parse_required_when_condition,
        'has_conditional_variables': has_conditional_variables,
        'format_model_config_settings': format_model_config_settings,
    })

    # Load template
    template = env.get_template("config.py.j2")

    # Render template with parsed data
    rendered_code = template.render(
        subjects=parsed_config.subjects,
        applications=parsed_config.applications,
        variables=parsed_config.variables,
        model_config_settings=parsed_config.model_config_settings
    )

    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write generated code
    with open(output_file, 'w') as f:
        f.write(rendered_code)

    print(f"Generated configuration code written to: {output_file}")


def main():
    """Main entry point for the generator."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate configuration code from TOML file")
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Path to configuration TOML file (default: config.toml)"
    )
    parser.add_argument(
        "--output",
        default="src/config/generated.py",
        help="Output file path (default: src/config/generated.py)"
    )

    args = parser.parse_args()

    generate_config_code(args.config, args.output)


if __name__ == "__main__":
    main()