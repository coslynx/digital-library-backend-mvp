"""
This file initializes the test module for the Digital Library Management Platform.

This module serves as the central entry point for running all tests for the
backend MVP. It is responsible for importing and organizing tests for different
components of the application.

This file is designed to be extensible, allowing for easy addition of new
tests as the MVP evolves. It utilizes the `pytest` framework for running tests
and adheres to the established coding conventions and standards of the project.

Data Flow:
    - Imports tests for different modules, including API routes, controllers, services,
      and database models.
    - Provides a unified interface for running tests using `pytest`.

Key Components:
    - `pytest` framework is used for test execution.

Integration with Other Components:
    - Imports test modules from `tests/api/v1`, `tests/infrastructure/database`,
      and `tests/utils`.

Testing and Quality Assurance:
    - Includes unit tests for individual functions and components.
    - Includes integration tests for verifying the overall functionality of the
      application.
    - Uses mocking techniques to isolate components for independent testing.
    - Adheres to established linting and code formatting rules.
"""
import pytest

from tests.api.v1 import routes
from tests.api.v1 import controllers
from tests.api.v1 import services
from tests.api.v1 import schemas
from tests.infrastructure.database import models
from tests.utils import auth