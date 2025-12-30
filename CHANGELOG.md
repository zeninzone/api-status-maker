# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial open source release
- Real-time API health monitoring
- Response time tracking and statistics
- Historical data visualization with interactive charts
- Multiple theme support (Light, Dark, Blue, Purple)
- REST API endpoint for status data
- Docker containerization support
- Kubernetes deployment manifests
- SQLite database with Flask-Migrate for schema management
- AJAX-based real-time updates (no page refresh)
- Mobile-responsive design
- API URL masking for security
- Uptime percentage calculation
- Status change notifications (email support)
- Custom status page themes
- Configurable default theme via config.ini

### Changed
- Migrated from JSON file storage to SQLite database
- Replaced page refresh with AJAX updates for better UX
- Improved error handling for NoneType values
- Enhanced chart visualization with color-coded status responses

### Fixed
- Fixed scheduler initialization issues
- Fixed import path inconsistencies
- Fixed database migration workflow
- Fixed theme persistence in database
- Fixed mobile responsiveness issues
- Fixed chart rendering on detail pages

## [1.0.0] - 2024-12-XX

### Added
- Initial release of API Status Maker
- Core monitoring functionality
- Web dashboard interface
- Configuration management via config.ini
- Docker support
- Kubernetes deployment support

---

## Version History

- **1.0.0**: Initial stable release

---

## Types of Changes

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

