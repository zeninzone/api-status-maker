# Contributing to API Status Maker

Thank you for your interest in contributing to API Status Maker! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots or error messages if applicable

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas (optional)

### Pull Requests

1. **Fork the repository** and clone it locally
2. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** with:
   - A clear title and description
   - Reference to related issues (if any)
   - Screenshots for UI changes

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- virtualenv (recommended)

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/api-status-maker.git
   cd api-status-maker
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd src
   pip install -r requirements.txt
   ```

4. Create a `config.ini` file:
   ```bash
   cp config/config.ini.example config/config.ini
   # Edit config/config.ini with your settings
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small
- Maximum line length: 100 characters (soft limit)

### Code Formatting

We recommend using:
- `black` for code formatting
- `flake8` or `pylint` for linting

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally

Example:
```
Add feature: Support for custom notification channels

- Implemented Slack webhook integration
- Added Discord webhook support
- Updated documentation with examples

Fixes #123
```

### File Structure

- Keep related functionality together
- Use descriptive file and directory names
- Follow the existing project structure

## Testing

Before submitting a PR, please ensure:
- Your code runs without errors
- Existing functionality still works
- New features are tested manually
- No linting errors (if applicable)

## Documentation

- Update the README.md if you add new features
- Add docstrings to new functions/classes
- Update CHANGELOG.md with your changes
- Include examples for new features

## Review Process

1. All PRs require at least one maintainer review
2. Address any feedback or requested changes
3. Maintainers will merge once approved
4. Thank you for your contribution! 🎉

## Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Reach out to maintainers
- Check existing issues and PRs

Thank you for contributing to API Status Maker!

