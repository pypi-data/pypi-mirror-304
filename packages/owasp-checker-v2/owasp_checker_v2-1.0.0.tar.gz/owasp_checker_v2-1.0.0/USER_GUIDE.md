# OWASP Checker V2 User Guide

This guide provides comprehensive documentation for using the OWASP Checker V2 library effectively.

## Author

**ABidi Bassem**  
Email: abidi.bassem@me.com  
GitHub: [abidi-bassem](https://github.com/abidi-bassem)

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

## Installation

### Prerequisites

- Python 3.8 or higher
- OWASP ZAP (for web vulnerability scanning)
- API keys (optional but recommended):
  - NVD API key for dependency checking
  - VirusTotal API key for threat intelligence

### Installation Methods

1. Install from PyPI:
```bash
pip install owasp-checker-v2
```

2. Install from source:
```bash
git clone https://github.com/abidi-bassem/owasp-checker-v2.git
cd owasp-checker-v2
pip install -e .
```

### Verifying Installation

```bash
# Check installation
owasp-checker --version

# Run test mode
owasp-checker --url http://example.com --test-mode
```

## Configuration

### API Keys

1. Environment Variables:
```bash
export NVD_API_KEY='your-nvd-api-key'
export VT_API_KEY='your-vt-api-key'
export OWASP_ZAP_PROXY='http://localhost:8080'
```

2. Direct Configuration:
```python
checker = OWASPChecker(
    nvd_api_key='your-nvd-api-key',
    vt_api_key='your-vt-api-key',
    zap_proxy_address='http://localhost:8080'
)
```

### Cache Settings

```python
# Update cache duration
checker.update_cache_duration(hours=24)

# Clear cache
checker.clear_cache()
```

## Basic Usage

### Command Line Interface

1. Basic URL Scan:
```bash
owasp-checker --url http://example.com
```

2. Dependency Check:
```bash
owasp-checker --dependencies requirements.txt
```

3. Full Security Check:
```bash
owasp-checker --url http://example.com --dependencies requirements.txt
```

4. Output Options:
```bash
# JSON output
owasp-checker --url http://example.com --output json

# Save to file
owasp-checker --url http://example.com --output-file report.txt
```

### Python API

1. URL Scanning:
```python
from owasp_checker_v2 import OWASPChecker

checker = OWASPChecker()
results = checker.scan_url('http://example.com')
```

2. Dependency Checking:
```python
results = checker.check_dependencies('requirements.txt')
```

3. Full Security Check:
```python
results = checker.run_full_check(
    url='http://example.com',
    dependency_file='requirements.txt'
)
```

## Advanced Features

### Custom Vulnerability Types

```python
# Scan for specific vulnerabilities
results = checker.scan_url(
    'http://example.com',
    vulnerability_types=[
        'sql_injection',
        'xss',
        'csrf',
        'file_inclusion',
        'authentication_bypass'
    ]
)
```

### Risk Prioritization

```python
# Get risk metrics
metrics = checker.risk_prioritizer.get_risk_metrics(results)

print(f"Total Vulnerabilities: {metrics['total_vulnerabilities']}")
print(f"Risk Levels: {metrics['risk_levels']}")
print(f"Average Risk Score: {metrics['average_risk_score']}")
```

### Threat Intelligence

```python
# Enrich vulnerability data
enriched = checker.threat_intelligence.enrich_vulnerability_data(results)

for vuln in enriched:
    print(f"Vulnerability: {vuln['name']}")
    print(f"Exploitation Risk: {vuln['exploitation_risk']}")
    print(f"Active Exploits: {vuln['active_exploits']}")
```

### OWASP Guidelines

```python
# Fetch guidelines
guidelines = checker.owasp_scraper.fetch_owasp_guidelines()

# Print Top Ten categories
for category, description in guidelines['OWASP Top Ten'].items():
    print(f"\n{category}:")
    print(description)
```

## Best Practices

### Security

1. API Key Management:
   - Store API keys securely
   - Use environment variables
   - Rotate keys regularly
   - Follow the principle of least privilege

2. Scanning Best Practices:
   - Start with test mode
   - Validate target URLs
   - Respect rate limits
   - Monitor API usage

3. Dependency Management:
   - Keep dependencies updated
   - Regular security checks
   - Follow version pinning best practices
   - Monitor security advisories

### Performance

1. Caching:
   - Enable caching for repeated scans
   - Set appropriate cache duration
   - Clear cache when needed
   - Monitor cache size

2. Rate Limiting:
   - Implement backoff strategies
   - Batch requests when possible
   - Monitor API quotas
   - Handle rate limit errors

### Integration

1. CI/CD Integration:
   - Automate security checks
   - Set appropriate thresholds
   - Configure notifications
   - Track security metrics

2. Error Handling:
   - Implement proper error handling
   - Log errors appropriately
   - Provide meaningful error messages
   - Handle edge cases

## Troubleshooting

### Common Issues

1. Connection Issues:
   - Check ZAP proxy connection
   - Verify API key validity
   - Check network connectivity
   - Validate target URLs

2. API Errors:
   - Check rate limits
   - Verify API key permissions
   - Monitor API quotas
   - Handle timeouts

3. Dependency Issues:
   - Check file formats
   - Validate dependency versions
   - Handle parsing errors
   - Monitor file access

### Error Messages

1. ZAP Connection:
```
Error: Could not connect to ZAP proxy at http://localhost:8080
Solution: Ensure ZAP is running and accessible
```

2. API Key:
```
Error: Invalid API key or insufficient permissions
Solution: Check API key validity and permissions
```

3. Rate Limit:
```
Error: API rate limit exceeded
Solution: Implement backoff strategy or reduce request frequency
```

## FAQ

### General Questions

Q: How often should I run security checks?
A: Regular checks are recommended, especially before deployments and after dependency updates.

Q: What's the difference between test mode and normal mode?
A: Test mode uses mock responses for development and testing, while normal mode performs actual scans.

### API Usage

Q: How do I get API keys?
A: Visit the respective provider websites:
- NVD: https://nvd.nist.gov/developers/request-an-api-key
- VirusTotal: https://www.virustotal.com/gui/join-us

Q: What are the API rate limits?
A: Rate limits vary by provider and API key type. Check the provider documentation for details.

### Integration

Q: How do I integrate with CI/CD?
A: Use the CLI interface in your pipeline scripts and set appropriate exit codes.

Q: Can I use custom vulnerability rules?
A: Yes, you can extend the scanner with custom rules. See the API reference for details.

### Support

For additional help:
- GitHub Issues: Report bugs and feature requests
- Documentation: Read the full documentation
- Community: Join the discussion forum
- Email: abidi.bassem@me.com for security-related issues
