# Enhanced OWASP Top Ten Compliance Checker Library (owasp_checker_v2)

This Python library provides an advanced tool for automating the detection of web application, API, and dependency vulnerabilities based on the OWASP Top Ten. It integrates additional OWASP guidelines, modular scanning options, threat intelligence, and prioritization mechanisms.

## Features

- Modular OWASP Top Ten Vulnerability Scanner
- NVD API Integration for Dependency Vulnerability Checking
- Real-Time Threat Intelligence Integration
- Risk-Based Vulnerability Prioritization
- OWASP Guidelines Scraper for Real-Time Updates
- Security Headers and Configuration Checker
- Injection Attack Simulation Module
- Remediation Suggestions and Reporting
- CI/CD Integration for Automated Security Checks

## Installation

You can install the owasp_checker_v2 library using pip:

```
pip install owasp_checker_v2
```

## Usage

### Command Line Interface

You can use the owasp_checker_v2 library from the command line:

```
owasp_checker <url_to_scan> [--dependency-file <path_to_file>] [--dependency-file-type <file_type>] [--zap-proxy <proxy_address>] [--nvd-api-key <api_key>] [--vt-api-key <api_key>]
```

### Python API

You can also use the library in your Python code:

```python
from owasp_checker_v2 import OWASPChecker

checker = OWASPChecker()
results = checker.run_full_check('http://example.com', 'requirements.txt', 'requirements')

print("Vulnerabilities:")
for vuln in results['vulnerabilities']:
    print(f"- {vuln['name']} (Risk Score: {vuln['risk_score']})")

print("\nOWASP Guidelines:")
for guideline_type, guidelines in results['guidelines'].items():
    print(f"\n{guideline_type}:")
    for key, value in guidelines.items():
        print(f"- {key}: {value}")
```

## Documentation

For more detailed information on how to use the library, please refer to the [User Guide](USER_GUIDE.md).

## Changelog

We maintain a changelog to keep track of all notable changes to this project. You can find it in the [CHANGELOG.md](CHANGELOG.md) file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Make sure to read the [Contributing Guidelines](CONTRIBUTING.md) first.

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OWASP for their invaluable work in web application security
- The open-source community for their continuous support and contributions
