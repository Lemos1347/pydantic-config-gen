"""
TOML parser for configuration definitions.

Parses the config.toml file and structures the data for code generation.
"""

import toml
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ConfigVariable:
    """Represents a single configuration variable."""
    name: str
    type: str
    description: str
    applications: List[str]
    default: Optional[str] = None
    subject: str = ""
    required_when: Optional[str] = None
    is_optional: bool = False

    def __post_init__(self):
        """Process type and set optional flag."""
        # Check if type is Optional[T] or T | None
        if self.type.startswith('Optional[') and self.type.endswith(']'):
            self.is_optional = True
            # Extract the inner type from Optional[T]
            self.type = self.type[9:-1]  # Remove 'Optional[' and ']'
        elif ' | None' in self.type:
            self.is_optional = True
            # Extract the type before ' | None'
            self.type = self.type.replace(' | None', '')
        elif self.type.endswith(' | None'):
            self.is_optional = True
            self.type = self.type[:-7]  # Remove ' | None'


@dataclass
class SubjectConfig:
    """Represents all variables for a specific subject (database, redis, etc.)."""
    name: str
    variables: List[ConfigVariable]


@dataclass
class ApplicationConfig:
    """Represents configuration needed by a specific application."""
    name: str
    subjects: List[str]


@dataclass
class ParsedConfig:
    """Complete parsed configuration data."""
    subjects: Dict[str, SubjectConfig]
    applications: Dict[str, ApplicationConfig]
    variables: List[ConfigVariable]


def parse_toml_file(file_path: str) -> ParsedConfig:
    """
    Parse the TOML configuration file and return structured data.

    Args:
        file_path: Path to the config.toml file

    Returns:
        ParsedConfig object with structured configuration data
    """
    with open(file_path, 'r') as f:
        data = toml.load(f)

    variables = []
    subjects = {}
    applications = {}

    # Parse each section and variable
    for subject_name, subject_vars in data.items():
        subject_variables = []

        for var_name, var_config in subject_vars.items():
            # The variable name should be just the TOML key, not prefixed with subject
            # Since the TOML key already includes the prefix like "DATABASE_URL"
            full_var_name = var_name.upper()

            variable = ConfigVariable(
                name=full_var_name,
                type=var_config['type'],
                description=var_config.get('description', ''),
                applications=var_config.get('applications', []),
                default=var_config.get('default'),
                subject=subject_name.upper(),
                required_when=var_config.get('required_when')
            )

            variables.append(variable)
            subject_variables.append(variable)

        # Create subject config
        subjects[subject_name.upper()] = SubjectConfig(
            name=subject_name.upper(),
            variables=subject_variables
        )

    # Build application configs
    all_apps = set()
    for var in variables:
        all_apps.update(var.applications)

    for app_name in all_apps:
        app_subjects = set()
        for var in variables:
            if app_name in var.applications:
                app_subjects.add(var.subject)

        applications[app_name] = ApplicationConfig(
            name=app_name,
            subjects=sorted(list(app_subjects))
        )

    return ParsedConfig(
        subjects=subjects,
        applications=applications,
        variables=variables
    )


def get_python_type(config_type: str, is_optional: bool = False) -> str:
    """Convert config type to Python type annotation."""
    type_mapping = {
        'str': 'str',
        'int': 'int',
        'float': 'float',
        'bool': 'bool'
    }
    base_type = type_mapping.get(config_type, 'str')

    if is_optional:
        return f'Optional[{base_type}]'
    return base_type


def get_pydantic_field_definition(variable: ConfigVariable) -> str:
    """Generate Pydantic field definition for a variable."""
    python_type = get_python_type(variable.type, variable.is_optional)

    if variable.default is not None:
        if variable.type == 'str':
            return f'{variable.name.lower()}: {python_type} = "{variable.default}"'
        else:
            return f'{variable.name.lower()}: {python_type} = {variable.default}'
    elif variable.is_optional:
        return f'{variable.name.lower()}: {python_type} = None'
    else:
        return f'{variable.name.lower()}: {python_type}'


def snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to CamelCase."""
    components = snake_str.split('_')
    return ''.join(word.capitalize() for word in components)


def get_property_name(subject: str) -> str:
    """Get the property name for a subject (e.g., 'DATABASE' -> 'database_config')."""
    return f"{subject.lower()}_config"


def get_class_name(subject: str) -> str:
    """Get the class name for a subject (e.g., 'DATABASE' -> 'DatabaseConfig')."""
    return f"{snake_to_camel(subject.lower())}Config"


def parse_required_when_condition(condition: str) -> tuple[str, str]:
    """
    Parse a required_when condition like 'USE_OTL=true' into (field_name, expected_value).

    Returns:
        tuple: (field_name, expected_value)
    """
    if '=' not in condition:
        raise ValueError(f"Invalid required_when condition: {condition}")

    field_name, expected_value = condition.split('=', 1)
    return field_name.strip().lower(), expected_value.strip()


def has_conditional_variables(variables: List[ConfigVariable]) -> bool:
    """Check if any variables have conditional requirements."""
    return any(var.required_when for var in variables)