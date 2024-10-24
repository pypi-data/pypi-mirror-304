# Changelog

All notable changes to the OWASP Checker V2 library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-25

### Added
- Initial release of OWASP Checker V2
- Core vulnerability scanning functionality using OWASP ZAP
- Dependency vulnerability checking using NVD API
- Threat intelligence integration using VirusTotal API
- Risk-based vulnerability prioritization
- OWASP guidelines and cheat sheets integration
- Command-line interface for easy usage
- Python API for programmatic access
- Comprehensive test suite
- Documentation (Quick Start, User Guide, API Reference)
- Example scripts for basic and advanced usage
- Test mode for development and testing
- Caching system for improved performance
- Support for multiple dependency file formats:
  - Python (requirements.txt)
  - Node.js (package.json)
  - Java (pom.xml)

### Features
- Web application vulnerability scanning
- Dependency vulnerability checking
- Real-time threat intelligence
- Risk prioritization and scoring
- Remediation guidance
- OWASP guidelines integration
- Parallel scanning capabilities
- Comprehensive reporting
- Cache management
- Rate limiting support
- Error handling and logging
- Test mode for development

### Components
- OWASPChecker: Main integration class
- OWASPTopTenScanner: Web vulnerability scanner
- DependencyChecker: Dependency vulnerability checker
- ThreatIntelligenceChecker: Threat intelligence provider
- RiskPrioritizer: Risk-based vulnerability prioritizer
- OWASPScraper: Guidelines and cheat sheets scraper

## [0.2.0] - 2024-01-20

### Added
- Beta release with core functionality
- Basic vulnerability scanning
- Initial dependency checking
- Command-line interface
- Basic documentation

### Changed
- Improved error handling
- Enhanced performance
- Updated documentation

### Fixed
- Various bug fixes
- Performance issues
- Documentation errors

## [0.1.0] - 2024-01-15

### Added
- Alpha release for testing
- Initial project structure
- Basic functionality
- Test framework

[1.0.0]: https://github.com/cline/owasp-checker-v2/releases/tag/v1.0.0
[0.2.0]: https://github.com/cline/owasp-checker-v2/releases/tag/v0.2.0
[0.1.0]: https://github.com/cline/owasp-checker-v2/releases/tag/v0.1.0
