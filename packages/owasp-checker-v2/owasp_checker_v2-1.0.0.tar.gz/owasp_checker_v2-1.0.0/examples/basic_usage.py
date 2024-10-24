#!/usr/bin/env python3
"""
Basic usage examples for the OWASP Checker V2 library.
"""

import os
import json
from datetime import datetime
from owasp_checker_v2 import OWASPChecker

def print_header(message):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f" {message}")
    print("=" * 80)

def scan_web_application():
    """Example: Scanning a web application"""
    print_header("Web Application Scan")
    
    # Initialize checker
    checker = OWASPChecker()
    checker.enable_test_mode()  # For demonstration purposes
    
    # Scan URL for vulnerabilities
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
    
    # Print results
    print(f"Found {len(results)} vulnerabilities:")
    for vuln in results:
        print(f"\nVulnerability: {vuln['name']}")
        print(f"Risk Level: {vuln['risk']}")
        print(f"CVSS Score: {vuln['cvss_score']}")
        print(f"Description: {vuln['description']}")
        print(f"Solution: {vuln['solution']}")

def check_project_dependencies():
    """Example: Checking project dependencies"""
    print_header("Dependency Check")
    
    # Create sample requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write("""
django==3.1.0
requests==2.25.0
flask==1.1.2
sqlalchemy==1.3.23
""".strip())
    
    try:
        # Initialize checker
        checker = OWASPChecker()
        checker.enable_test_mode()  # For demonstration purposes
        
        # Check dependencies
        results = checker.check_dependencies('requirements.txt')
        
        # Print results
        print(f"Found {len(results)} vulnerable dependencies:")
        for vuln in results:
            print(f"\nPackage: {vuln['name']} {vuln['version']}")
            print(f"CVE: {vuln['cve_id']}")
            print(f"CVSS Score: {vuln['cvss_score']}")
            print(f"Description: {vuln['description']}")
            print(f"Solution: {vuln['solution']}")
    
    finally:
        # Clean up
        if os.path.exists('requirements.txt'):
            os.remove('requirements.txt')

def get_threat_intelligence():
    """Example: Getting threat intelligence data"""
    print_header("Threat Intelligence")
    
    # Initialize checker
    checker = OWASPChecker()
    checker.enable_test_mode()  # For demonstration purposes
    
    # Get vulnerabilities
    vulns = checker.scan_url('http://example.com')
    
    # Enrich with threat intelligence
    enriched = checker.threat_intelligence.enrich_vulnerability_data(vulns)
    
    # Print results
    print("Threat Intelligence Data:")
    for vuln in enriched:
        print(f"\nVulnerability: {vuln['name']}")
        print(f"Exploitation Risk: {vuln['exploitation_risk']}")
        print(f"Active Exploits: {vuln['active_exploits']}")
        print(f"Last Seen: {vuln['last_seen']}")
        print(f"Detection Ratio: {vuln['detection_ratio']}")

def analyze_risk_metrics():
    """Example: Analyzing risk metrics"""
    print_header("Risk Analysis")
    
    # Initialize checker
    checker = OWASPChecker()
    checker.enable_test_mode()  # For demonstration purposes
    
    # Get vulnerabilities
    vulns = checker.scan_url('http://example.com')
    
    # Get risk metrics
    metrics = checker.risk_prioritizer.get_risk_metrics(vulns)
    
    # Print metrics
    print("Risk Metrics:")
    print(f"Total Vulnerabilities: {metrics['total_vulnerabilities']}")
    print("\nRisk Levels:")
    for level, count in metrics['risk_levels'].items():
        print(f"  {level}: {count}")
    print(f"\nAverage Risk Score: {metrics['average_risk_score']:.2f}")
    print(f"Highest Risk Score: {metrics['highest_risk_score']}")
    print(f"Active Exploits: {metrics['active_exploits_count']}")

def get_remediation_guidance():
    """Example: Getting remediation guidance"""
    print_header("Remediation Guidance")
    
    # Initialize checker
    checker = OWASPChecker()
    checker.enable_test_mode()  # For demonstration purposes
    
    # Get vulnerabilities
    vulns = checker.scan_url('http://example.com')
    
    # Get remediation steps for each vulnerability
    for vuln in vulns:
        remediation = checker.get_remediation_steps(vuln)
        
        print(f"\nRemediation for {remediation['vulnerability']['name']}:")
        print("\nSteps:")
        for step in remediation['steps']:
            print(f"- {step}")
        
        print("\nReferences:")
        for ref in remediation['references']:
            print(f"- {ref}")
        
        print("\nOWASP Guidelines:")
        for category, guide in remediation['guidelines'].items():
            print(f"\n{category}:")
            print(guide)

def save_scan_report():
    """Example: Saving scan results to a file"""
    print_header("Scan Report")
    
    # Initialize checker
    checker = OWASPChecker()
    checker.enable_test_mode()  # For demonstration purposes
    
    # Run full security check
    results = checker.run_full_check(
        url='http://example.com',
        dependency_file='requirements.txt',
        vulnerability_types=['sql_injection', 'xss', 'csrf']
    )
    
    # Add metadata
    report = {
        'scan_time': datetime.now().isoformat(),
        'results': results
    }
    
    # Save as JSON
    with open('security_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("Report saved to security_report.json")

def main():
    """Run all examples"""
    try:
        scan_web_application()
        check_project_dependencies()
        get_threat_intelligence()
        analyze_risk_metrics()
        get_remediation_guidance()
        save_scan_report()
    
    finally:
        # Clean up
        if os.path.exists('security_report.json'):
            os.remove('security_report.json')

if __name__ == '__main__':
    main()
