# OWASP Checker V2 API Reference

This document provides detailed information about the classes and methods available in the OWASP Checker V2 library.

## Table of Contents

- [OWASPChecker](#owaspchecker)
- [OWASPTopTenScanner](#owasptoptenscanner)
- [DependencyChecker](#dependencychecker)
- [ThreatIntelligenceChecker](#threatintelligencechecker)
- [RiskPrioritizer](#riskprioritizer)
- [OWASPScraper](#owaspscraper)

## OWASPChecker

Main class that integrates all components for comprehensive security checking.

### Constructor



- **zap_proxy_address**: OWASP ZAP proxy address
- **nvd_api_key**: Optional NVD API key for dependency checking
- **vt_api_key**: Optional VirusTotal API key for threat intelligence

### Methods

#### scan_url



Scan a URL for vulnerabilities.

- **url**: Target URL to scan
- **vulnerability_types**: Optional list of specific vulnerability types to scan for
- **Returns**: List of detected vulnerabilities

#### check_dependencies



Check dependencies for known vulnerabilities.

- **dependency_file**: Path to dependency file
- **file_type**: Optional type of dependency file (requirements, package.json, pom.xml)
- **Returns**: List of vulnerabilities found in dependencies

#### run_full_check



Run a comprehensive security check.

- **url**: Optional target URL to scan
- **dependency_file**: Optional path to dependency file
- **vulnerability_types**: Optional list of specific vulnerability types to scan for
- **Returns**: Dictionary containing scan results and guidelines

## OWASPTopTenScanner

Handles web vulnerability scanning using OWASP ZAP.

### Constructor



- **zap_proxy_address**: OWASP ZAP proxy address

### Methods

#### scan_url



Scan a URL for OWASP Top Ten vulnerabilities.

- **url**: Target URL to scan
- **vulnerability_types**: Optional list of specific vulnerability types to scan for
- **Returns**: List of detected vulnerabilities

## DependencyChecker

Checks dependencies for known vulnerabilities using NVD API.

### Constructor



- **nvd_api_key**: Optional NVD API key for higher rate limits

### Methods

#### check_dependencies



Check dependencies for known vulnerabilities.

- **dependency_file**: Path to dependency file
- **file_type**: Optional type of dependency file
- **Returns**: List of vulnerabilities found in dependencies

## ThreatIntelligenceChecker

Provides threat intelligence data using VirusTotal API.

### Constructor



- **vt_api_key**: Optional VirusTotal API key

### Methods

#### enrich_vulnerability_data



Enrich vulnerability data with threat intelligence.

- **vulnerabilities**: List of vulnerabilities to enrich
- **Returns**: List of vulnerabilities with added threat intelligence data

## RiskPrioritizer

Handles risk-based vulnerability prioritization.

### Constructor



### Methods

#### prioritize_vulnerabilities



Prioritize vulnerabilities based on risk factors.

- **vulnerabilities**: List of vulnerabilities to prioritize
- **asset_criticality**: Optional criticality level of the scanned asset
- **Returns**: List of vulnerabilities sorted by risk priority

#### get_risk_metrics



Calculate risk metrics for a set of vulnerabilities.

- **vulnerabilities**: List of vulnerabilities
- **Returns**: Dictionary containing risk metrics

## OWASPScraper

Fetches and parses OWASP guidelines and security recommendations.

### Constructor



### Methods

#### fetch_owasp_guidelines



Fetch the latest OWASP guidelines and recommendations.

- **Returns**: Dictionary containing OWASP guidelines and recommendations

## Common Features

All components support the following features:

### Test Mode



Enable test mode to use mock responses instead of real API calls.

### Cache Management



Clear the component's cache.



Update the cache duration.

- **hours**: New cache duration in hours

## Data Structures

### Vulnerability Dictionary



### Guidelines Dictionary



## Error Handling

All methods may raise the following exceptions:

- **ValueError**: Invalid input parameters
- **FileNotFoundError**: Dependency file not found
- **requests.exceptions.RequestException**: Network or API errors
- **json.JSONDecodeError**: Invalid API response
- **Exception**: Other unexpected errors

## Best Practices

1. Always handle exceptions appropriately
2. Use test mode for development and testing
3. Cache results when appropriate
4. Use API keys for better rate limits
5. Follow the principle of least privilege
6. Validate and sanitize all inputs
7. Monitor API usage and rate limits
8. Keep dependencies updated
9. Review scan results for false positives
10. Follow security guidelines for API key management

## Examples

See the [examples/](examples/) directory for complete example scripts.
