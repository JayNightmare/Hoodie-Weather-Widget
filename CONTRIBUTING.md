# Contributing to Hoodie Weather Widget

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/hoodie-weather-widget.git
   cd hoodie-weather-widget
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # Install development dependencies
   pip install pytest pytest-cov flake8 black isort mypy safety bandit
   ```

4. **Run tests**:
   ```bash
   python -m pytest
   ```

## Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run these before submitting:

```bash
# Format code
black .
isort .

# Lint
flake8 .

# Type check
mypy src/ --ignore-missing-imports
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Include both unit tests and integration tests where appropriate

## Bug Reports

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/hoodie-weather-widget/issues).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature has already been requested
2. Clearly describe the feature and its benefits
3. Consider the scope and complexity
4. Be open to discussion and feedback

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Don't hesitate to ask! You can reach out by opening an issue or discussion on GitHub.
