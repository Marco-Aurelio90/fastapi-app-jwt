# Changelog

Tutti i cambiamenti significativi a questo progetto saranno documentati in questo file.

## [Unreleased]

## [1.1.0] - 2024-07-27

### Added
- Added support for `JWT_SECRET` and `TOKEN_TYPE` environment variable to mitigate hardcoded password string and harcoded password funcarg vulnerability.

### Changed
- Moved hardcoded password value from source code to environment variables

### Fixed
- Fixed hardcoded password string and harcoded password funcargs vulnerability in `services.py`.
