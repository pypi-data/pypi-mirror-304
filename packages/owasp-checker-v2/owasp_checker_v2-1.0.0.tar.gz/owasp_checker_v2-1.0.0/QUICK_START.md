# OWASP Checker v2 Quick Start Guide

Get started with OWASP Checker v2 in minutes!

## Installation

1. Install the package:
```bash
pip install owasp_checker_v2
```

2. Install OWASP ZAP (if not already installed):
   - Download from: https://www.zaproxy.org/download/
   - Start ZAP and note the proxy address (default: http://localhost:8080)

## Basic Usage

1. Simple vulnerability scan:
```python
from owasp_checker_v2 import OWASPChecker

# Initialize the checker
checker = OWASPChecker()

# Run a full check
results = checker.run_full_check('http://example.com')

# Print vulnerabilities
for vuln in results['vulnerabilities']:
    print(f"- {vuln['name']} (Risk Score: {vuln['risk_score']})")
```

2. Check dependencies:
```python
from owasp_checker_v2 import DependencyChecker

checker = DependencyChecker()
vulnerabilities = checker.check_requirements('requirements.txt')
```

3. Get threat intelligence:
```python
from owasp_checker_v2 import ThreatIntelligenceChecker

checker = ThreatIntelligenceChecker('your_virustotal_api_key')
enriched_vulns = checker.enrich_vulnerability_data(vulnerabilities)
```

## Common Use Cases

1. CI/CD Integration:
```python
from owasp_checker_v2 import OWASPChecker

def security_check():
    checker = OWASPChecker()
    results = checker.run_full_check('http://your-staging-app.com')
    high_risk_vulns = [v for v in results['vulnerabilities'] if v['risk_score'] > 7.5]
    if high_risk_vulns:
        raise Exception("High risk vulnerabilities detected!")
```

2. Custom Vulnerability Types:
```python
from owasp_checker_v2 import OWASPTopTenScanner

scanner = OWASPTopTenScanner()
results = scanner.scan_url('http://example.com', vulnerability_types=['xss', 'sql_injection'])
```

## Next Steps

- Read the [User Guide](USER_GUIDE.md) for detailed information
- Check the [API Reference](API_REFERENCE.md) for complete documentation
- See [examples/advanced_examples.py](examples/advanced_examples.py) for more use cases

## Troubleshooting

1. ZAP Connection Issues:
   - Ensure ZAP is running
   - Check if the proxy address is correct
   - Verify firewall settings

2. API Key Issues:
   - Verify NVD API key is valid
   - Check VirusTotal API key permissions

3. Dependency Scanning Issues:
   - Ensure dependency file format is correct
   - Check internet connectivity for NVD access

For more help, please check the [User Guide](USER_GUIDE.md) or open an issue on GitHub.
